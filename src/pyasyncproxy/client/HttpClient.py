"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from abc import ABC, abstractmethod
from types import TracebackType
from typing import Self

from pyasyncproxy.model.dto.ProxyRequest import ProxyRequest
from pyasyncproxy.model.dto.ProxyResponse import ProxyResponse


class HttpClient(ABC):
    """http client."""

    @abstractmethod
    def __init__(self, proxy_url: str | None = None) -> None:
        """Init."""

    @abstractmethod
    async def request(self, req: ProxyRequest) -> ProxyResponse:
        """Do request."""

    @abstractmethod
    async def __aenter__(self) -> Self:
        """Aenter."""

    @abstractmethod
    async def __aexit__(
        self,
        exc_type: type[BaseException] | None = None,
        exc_val: BaseException | None = None,
        exc_tb: TracebackType | None = None,
    ) -> None:
        """Aexit."""
