"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

import logging
import logging.config

from pyasyncproxy.cli.Cli import Cli
from pyasyncproxy.cli.ProcessManager import ProcessManager
from pyasyncproxy.model.dto.ProjectEnv import ProjectEnv


def main() -> None:
    """The asynchronous network proxy application."""
    project_env = ProjectEnv()
    if project_env.log_path.exists():
        logging.config.fileConfig(project_env.log_path)
    cli = Cli(project_env)
    if cli.stop:
        ProcessManager(cli.stop.app, project_env).stop()
    elif cli.start:
        ProcessManager(cli.start.app, project_env, cmd=cli.start.cmd).start()


if __name__ == "__main__":
    main()
