"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

import logging
import logging.config
import platform
import queue
import subprocess  # noqa: S404
import threading
from typing import ClassVar

import psutil

from pyasyncproxy.env.ProjectEnv import ProjectEnv

logger = logging.getLogger(__name__)


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
        print(self._env.project_banner)  # noqa: T201
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
                has_closed = True
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
