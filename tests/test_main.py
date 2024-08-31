"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

import multiprocessing
import pathlib
import subprocess  # noqa: S404
import sys
import time
from typing import Any, Literal, override

import psutil
import pytest
from pydantic import ValidationInfo
from pydantic_core import CoreConfig

from pyasyncproxy.__main__ import ProcessManager, ProjectEnv, main
from pyasyncproxy._version import version


@pytest.mark.parametrize("arg", ["-V", "--version"])
def test_version(arg: str) -> None:
    """Test version."""
    command = ["python", "-m", "pyasyncproxy", arg]
    result = subprocess.run(command, capture_output=True, text=True)  # noqa: S603
    assert version in result.stdout


@pytest.mark.parametrize("arg", ["-h", "--help"])
def test_help(arg: str) -> None:
    """Test help."""
    command = ["python", "-m", "pyasyncproxy"]
    result_no_arg = subprocess.run(command, capture_output=True, text=True)  # noqa: S603
    command = ["python", "-m", "pyasyncproxy", arg]
    result = subprocess.run(command, capture_output=True, text=True)  # noqa: S603
    assert result.stdout == result_no_arg.stdout


@pytest.mark.parametrize(
    ("banner", "data"), [("banner", None), ("", None), ("", {"banner_path": pathlib.Path.cwd() / "any.txt"})]
)
def test_project_env(banner: str, data: dict[str, Any] | None) -> None:
    """Test project env."""

    class Info(ValidationInfo):
        """validation info."""

        def __init__(self, data: dict[str, Any] | None = None) -> None:
            """Init."""
            self._data = data or {}

        @override
        @property
        def data(self) -> dict[str, Any]:
            return self._data

        @override
        @property
        def context(self) -> Any:
            return None

        @override
        @property
        def config(self) -> CoreConfig | None:
            return None

        @override
        @property
        def mode(self) -> Literal["python", "json"]:
            return "python"

        @override
        @property
        def field_name(self) -> str | None:
            return None

    env = ProjectEnv()
    assert env.debug
    assert version in env.project_banner  # type:ignore[operator]
    assert ProjectEnv.inject_banner(banner, Info(data)) == banner  # type:ignore[call-arg]


def test_start(capsys: pytest.CaptureFixture[str]) -> None:
    """Test start."""
    key = "hello world"
    sys.argv = ["_", "start", "--cmd", "echo", "--cmd", key]
    main()
    assert key in capsys.readouterr().out


def task() -> None:
    """Process task."""
    time.sleep(20)


def test_stop(capsys: pytest.CaptureFixture[str]) -> None:
    """Test stop."""
    multiprocessing.set_start_method("spawn")
    process = multiprocessing.Process(target=task)
    process.start()
    process_info = psutil.Process(process.pid)
    assert process_info.is_running()
    name = "multiprocessing-fork"
    sys.argv = ["_", "stop", "--app", name]
    main()
    assert f"The {name}:{process.pid} has been closed" in capsys.readouterr().out
    name = "not found app"
    sys.argv = ["_", "stop", "--app", name]
    main()
    assert f"The {name} not found" in capsys.readouterr().out


@pytest.mark.parametrize(
    ("arg", "signal"),
    [
        ("Windows", 15),
        ("Linux", 2),
        ("Darwin", 15),
        pytest.param("NOP", -1, marks=pytest.mark.xfail(raises=RuntimeError)),
    ],
)
def test_process_manager(arg: str, signal: int) -> None:
    """Test process manager."""
    ProcessManager.PLATFORM = arg
    manager = ProcessManager("_", ProjectEnv())
    assert manager.signal == signal
