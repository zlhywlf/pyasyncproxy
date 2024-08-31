"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

import sys
from argparse import ArgumentParser

from pydantic_settings import CliSettingsSource

from pyasyncproxy._version import version
from pyasyncproxy.env.ProjectEnv import ProjectEnv
from pyasyncproxy.model.cmd.CmdRoot import CmdRoot


class Cli(CmdRoot):
    """command line interface."""

    def __init__(self, env: ProjectEnv) -> None:
        """Init."""
        if not sys.argv[1:]:
            sys.argv.append("-h")
        super().__init__(_cli_settings_source=self._create_cli_settings_source(env.project_name))

    def _create_cli_settings_source(self, prog: str) -> CliSettingsSource[ArgumentParser]:
        description = "The asynchronous network proxy application."
        arg_parser = ArgumentParser(prog=prog, description=description)
        help_msg = "show this version information and exit"
        arg_parser.add_argument("-V", "--version", action="version", version=version, help=help_msg)
        return CliSettingsSource(
            self.__class__,
            cli_parse_args=True,
            root_parser=arg_parser,
            parse_args_method=lambda parser, args: parser.parse_known_args(args)[0],
        )
