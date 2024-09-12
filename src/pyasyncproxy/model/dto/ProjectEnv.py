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
    forward_url_key: str = Field(default="x-proxy-url", description="proxy url's key in the headers")
    forward_method_key: str = Field(default="x-proxy-method", description="proxy method's key in the headers")
    forward_timeout: str = Field(default="x-proxy-timeout", description="proxy timeout's key in the headers")
    business_id_key: str = Field(default="x-proxy-id", description="business id's key in the headers")
    business_expiry_key: str = Field(default="x-proxy-expiry", description="business expiry's key in the headers")
    exclude_headers: list[str] | None = Field(default=None, description="exclude keys from headers")
    proxy_path: pathlib.Path = Field(default=pathlib.Path.cwd() / "proxy.json", description="proxy config path")
    worker_id: int = Field(default=1, description="worker id")
    data_center_id: int = Field(default=1, description="data center id")
    proxy_auth: dict[str, str] | None = Field(default=None, description="proxy auth")
    forward_retry_key: str = Field(default="x-proxy-retry", description="proxy retry key in the headers")

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
            return cls.default_banner()
        if not banner_path.exists():
            return cls.default_banner()
        with banner_path.open("r") as f:
            return "".join(f.readlines())

    @field_validator("proxy_auth", mode="before")
    @classmethod
    def inject_proxy_auth(cls, v: dict[str, str] | None) -> dict[str, str]:
        """Inject proxy auth."""
        return v if v else {}

    @classmethod
    def default_banner(cls) -> str:
        """Default banner."""
        return r"""
 ____  _  _   __    ___  _  _  _  _  ___  ____  ____  _____  _  _  _  _
(  _ \( \/ ) /__\  / __)( \/ )( \( )/ __)(  _ \(  _ \(  _  )( \/ )( \/ )
 )___/ \  / /(__)\ \__ \ \  /  )  (( (__  )___/ )   / )(_)(  )  (  \  /
(__)   (__)(__)(__)(___/ (__) (_)\_)\___)(__)  (_)\_)(_____)(_/\_) (__)
"""
