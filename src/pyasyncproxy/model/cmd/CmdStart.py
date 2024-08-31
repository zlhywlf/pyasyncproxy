"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from pydantic import Field

from pyasyncproxy.model.cmd.CmdStop import CmdStop


class CmdStart(CmdStop):
    """start."""

    cmd: list[str] | None = Field(None, description="command to launch the application")
