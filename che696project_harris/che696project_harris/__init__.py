#!/usr/bin/env python

"""Top-level package for CHE696 Project."""

__author__ = """Conor Gage Harris"""
__email__ = 'harriscg@umich.edu'
__version__ = '0.1.0'

# Make Python 2 and 3 imports work the same
# Safe to remove with Python 3-only code
from __future__ import absolute_import

# Add imports here
from .che696project_harris import *

# Handle versioneer
from ._version import get_versions
versions = get_versions()
__version__ = versions['version']
__git_revision__ = versions['full-revisionid']
del get_versions, versions

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
