"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

import logging
import logging.config
import pathlib

from pydantic import Field, ValidationInfo, computed_field, field_validator
from pydantic_settings import BaseSettings

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
