"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

import logging
import logging.config
import pathlib
import platform
import queue
import subprocess  # noqa: S404
import sys
import threading
from argparse import ArgumentParser
from typing import ClassVar

import psutil
from pydantic import BaseModel, Field, ValidationInfo, computed_field, field_validator
from pydantic_settings import BaseSettings, CliSettingsSource, CliSubCommand

from pyasyncproxy._version import version

logger = logging.getLogger(__name__)


class ProjectEnv(BaseSettings, env_prefix="PROXY_", env_file=".env", env_file_encoding="utf-8"):
    """project environment variable."""

    app_name: str = Field(default="pyasyncproxy.app:app", description="app name")
    banner_path: pathlib.Path = Field(default=pathlib.Path.cwd() / "banner.txt", description="banner file path")
    banner: str = Field(default="", description="banner")
    debug: bool = Field(default=False, description="debug mode")
    log_path: pathlib.Path = Field(default=pathlib.Path.cwd() / "logging.ini", description="log config path")
    process_keywords: list[str] | None = Field(default=None, description="process keywords")
    project_name: str = Field(default="pyasyncproxy", description="project name")
    start_cmd: list[str] | None = Field(default=None, description="start cmd")

    @computed_field
    def project_banner(self) -> str:
        """Project banner."""
        return f"{self.banner}\n:: {self.project_name} :: v{version}\n"

    @field_validator("banner")
    @classmethod
    def inject_banner(cls, v: str, info: ValidationInfo) -> str:
        """Inject banner."""
        if v:
            return v
        banner_path = info.data.get("banner_path")
        if not banner_path or not isinstance(banner_path, pathlib.Path):
            logger.warning(f"Configuration not supported: {banner_path}")
            return ""
        if not banner_path.exists():
            logger.warning(f"Configuration not found: {banner_path}")
            return ""
        with banner_path.open("r") as f:
            return "".join(f.readlines())


class ProcessManager:
    """Process Manager."""

    PLATFORM: ClassVar[str] = platform.system()

    def __init__(self, app: str | None, env: ProjectEnv, *, cmd: list[str] | None = None) -> None:
        """Init."""
        self._app = app or env.app_name
        self._env = env
        self._signal = self._handle_signal()
        self._start_cmd = cmd or env.start_cmd or []
        self._process_keywords = env.process_keywords or ["python"]

    @property
    def signal(self) -> int:
        """Signal to end the process."""
        return self._signal

    def start(self) -> None:
        """Start process."""
        cmd = " ".join(self._start_cmd)
        print(self._env.banner)  # noqa: T201
        logger.info(f"The {self._app} will be launched through '{cmd}'")
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)  # noqa: S602
        out: queue.Queue[str] = queue.Queue()
        out_thread = threading.Thread(target=lambda: [out.put(_.decode()) for _ in iter(p.stdout.readline, b"")])  # type: ignore[func-returns-value,union-attr]
        out_thread.daemon = True
        out_thread.start()
        timeout = 5.0
        while True:
            try:
                print(out.get(timeout=timeout), end="")  # noqa: T201
                timeout = 1
            except queue.Empty:
                logger.info(f"The {self._app} has been launched")
                break

    def stop(self) -> None:
        """Close process."""
        logger.info(f"The {self._app} will be closed")
        has_closed = False
        for proc in psutil.process_iter():
            if (
                any(_ in proc.name() for _ in self._process_keywords)
                and proc.status() != psutil.STATUS_ZOMBIE
                and self._app in ",".join(proc.cmdline())
            ):
                proc.send_signal(self._signal)
                logger.info(f"The {self._app}:{proc.pid} has been closed")
                has_closed = not has_closed
        if not has_closed:
            logger.warning(f"The {self._app} not found")

    def _handle_signal(self) -> int:
        match self.PLATFORM:
            case "Windows" | "Darwin":
                return 15
            case "Linux":
                return 2
            case _:
                msg = f"Unsupported system environment: ({self.PLATFORM})."
                raise RuntimeError(msg)


class StopEnv(BaseModel):
    """stop."""

    app: str | None = Field(None, description="applications name")


class StartEnv(StopEnv):
    """start."""

    cmd: list[str] | None = Field(None, description="command to launch the application")


class Cli(BaseSettings):
    """runtime environment base class."""

    start: CliSubCommand[StartEnv] = Field(description="start")
    stop: CliSubCommand[StopEnv] = Field(description="stop")

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
