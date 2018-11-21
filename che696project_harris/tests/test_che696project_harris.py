#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `che696project_harris` package."""


import unittest
from click.testing import CliRunner

from che696project_harris import che696project_harris
from che696project_harris import cli


class TestChe696project_harris(unittest.TestCase):
    """Tests for `che696project_harris` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_something(self):
        """Test something."""

    def test_command_line_interface(self):
        """Test the CLI."""
        runner = CliRunner()
        result = runner.invoke(cli.main)
        assert result.exit_code == 0
        assert 'che696project_harris.cli.main' in result.output
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  Show this message and exit.' in help_result.output
