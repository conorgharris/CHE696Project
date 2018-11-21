#!/usr/bin/env python3

"""
che696project_harris.py
Project Including:
 - reading in numeric data from .txt file
 - calculating elastic (G') and viscous (G") moduli
 - plotting elastic (G') and viscous (G") moduli data
 - plotting viscosity data
"""

from __future__ import print_function
import sys
from argparse import ArgumentParser
import numpy as np
import matplotlib.pyplot as plt
import os
from pylab import *


SUCCESS = 0
INVALID_DATA = 1
IO_ERROR = 2

DEFAULT_DATA_FILE_NAME = 'data/20171015_Harris_Conor_TPU_FreqSweep-0002oexp.txt'


def warning(*objs):
    """Writes a message to stderr."""
    print("WARNING: ", *objs, file=sys.stderr)

def parse_cmdline(argv):
    """
    Returns the parsed argument list and return code.
    `argv` is a list of arguments, or `None` for ``sys.argv[1:]``.
    """
    if argv is None:
        argv = sys.argv[1:]

    # initialize the parser object:
    parser = ArgumentParser(description='Reads in a txt file')
    parser.add_argument("-c", "--txt_data_file", help="The location (directory and file name) of the txt file with "
                                                      "data to analyze",
                        default=DEFAULT_DATA_FILE_NAME)
    args = None
    try:
        args = parser.parse_args(argv)
        args.txt_data = np.loadtxt(DEFAULT_DATA_FILE_NAME, delimiter='\t')
    except IOError as e:
        warning("Problems reading file:", e)
        parser.print_help()
        return args, IO_ERROR
    except ValueError as e:
        warning("Read invalid data:", e)
        parser.print_help()
        return args, INVALID_DATA

    return args, SUCCESS

def data_analysis(data_array):
    """
    Finds the average, min, and max for each row of the given array

    Parameters
    ----------
    data_array : numpy array of patient data (one line per patient, daily measurements) in plasma inflammation units

    Returns
    -------
    data_stats : numpy array
        array with same number of rows as data_array, and columns for average, max, and min values (in that order)
    """

    #temp, time, osc_stress, strain, delta, G_p, G_dp, strain_per, freq, ada_p, ada_dp, ada_complex, rawphase, tan_delta, torque, n_force, mu = data_array
    #base = {1: 'temp',2: 'time',3: 'osc_stress',4: 'strain', 5: 'delta',
    #        6: 'G_p',7: 'G_dp',8: 'strain_per', 9:'freq',10:'ada_p',
    #       11:'ada_dp',12:'ada_complex',13: 'rawphase',14:'tan_delta',
    #       15:'torque',16:'n_force',17:'mu'}


    temp = data_array[:,0]
    osc_stress = data_array[:,2]
    strain = data_array[:,3]
    delta = data_array[:,4]
    freq = data_array[:,8]
    ada_complex = data_array[:,11]

    # G_elastic = np.zeros([data_array.shape, 1])
    # G_viscous = np.zeros([data_array.shape, 1])

    # G_elastic = osc_stress/strain * np.cos(delta)
    # G_viscous = osc_stress/strain * np.sin(delta)

    G_elastic = data_array[:,5]
    G_viscous = data_array[:,6]

    test, test1 = data_array.shape
    data_stats = np.zeros((5,test))

    data_stats[0,:] = temp
    data_stats[1,:] = G_elastic
    data_stats[2,:] = G_viscous
    data_stats[3,:] = ada_complex
    data_stats[4,:] = freq

    return data_stats

def plot_stats(base_f_name, data_stats):
    """
    Makes a plot of the mean, max, and min inflammation per patient
    :param base_f_name: str of base output name (without extension)
    :param data_stats: numpy array with shape (num_patients, num_stats) where num_stats = 3 (mean, max, min)
    :return: saves a png file
    """

    rc('axes', linewidth = 2)
    #G_elastic, G_viscous, ada_complex = temp.shape
    x_axis = data_stats[4,:]
    # red dashes, blue squares and green triangles

    plt.figure()
    plt.loglog(x_axis, data_stats[1,:], 'bo', label = "G'", basex=10)
    plt.loglog(x_axis, data_stats[2,:], 'go', label = 'G"', basex=10)
    # plt.title('Patient Arthritis Data')
    fontsize = 10
    ax = gca()

    for tick in ax.xaxis.get_major_ticks():
        tick.label1.set_fontsize(fontsize)
        tick.label1.set_fontweight('bold')
    for tick in ax.yaxis.get_major_ticks():
        tick.label1.set_fontsize(fontsize)
        tick.label1.set_fontweight('bold')

    plt.xlabel(r'\textbf{f [Hz]}',fontsize = 12, usetex=True)
    plt.ylabel(r"\textbf{Modulus (G', G'') [Pa]",fontsize = 12, usetex=True)
    plt.legend(framealpha=1, frameon=True);
    out_name = base_f_name + "moduli" + ".png"
    plt.savefig(out_name)
    print("Wrote file: {}".format(out_name))

    plt.figure()
    plt.loglog(x_axis, data_stats[3,:], 'bo', label = "G'", basex=10)
    # plt.title('Patient Arthritis Data')
    fontsize = 10
    ax = gca()

    for tick in ax.xaxis.get_major_ticks():
        tick.label1.set_fontsize(fontsize)
        tick.label1.set_fontweight('bold')
    for tick in ax.yaxis.get_major_ticks():
        tick.label1.set_fontsize(fontsize)
        tick.label1.set_fontweight('bold')

    plt.xlabel(r'\textbf{f [Hz]}',fontsize = 12, usetex=True)
    plt.ylabel(r'\textbf{$|n^*| [Pa \cdot s]$}',fontsize = 12, usetex=True)
    #ax.set_xlim(1)
    ax.set_ylim(10,10e2)
    out_name = base_f_name + "viscosity" + ".png"
    plt.savefig(out_name)
    print("Wrote file: {}".format(out_name))


def main(argv=None):
    args, ret = parse_cmdline(argv)
    if ret != SUCCESS:
        return ret
    data_stats = data_analysis(args.txt_data)

    # get the name of the input file without the directory it is in, if one was specified
    base_out_fname = os.path.basename(args.txt_data_file)
    # get the first part of the file name (omit extension) and add the suffix
    base_out_fname = os.path.splitext(base_out_fname)[0] + '_stats'
    # add suffix and extension
    out_fname = base_out_fname + '.txt'
    np.savetxt(out_fname, data_stats, delimiter=' ')
    print("Wrote file: {}".format(out_fname))

    # send the base_out_fname and data to a new function that will plot the data
    plot_stats(base_out_fname, data_stats)
    return SUCCESS  # success

if __name__ == "__main__":
    status = main()
    sys.exit(status)


