"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from argparse import ArgumentParser

from pydantic import Field
from pydantic_settings import BaseSettings, CliSettingsSource, CliSubCommand

from pyasyncproxy.model.cmd.CmdStart import CmdStart
from pyasyncproxy.model.cmd.CmdStop import CmdStop


class CmdRoot(BaseSettings):
    """root."""

    def __init__(self, _cli_settings_source: CliSettingsSource[ArgumentParser] | None = None) -> None:
        """Init."""
        super().__init__(_cli_settings_source=_cli_settings_source)

    start: CliSubCommand[CmdStart] = Field(description="start")
    stop: CliSubCommand[CmdStop] = Field(description="stop")
