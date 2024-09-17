"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from enum import StrEnum


class ProxyCheckerEnum(StrEnum):
    """checker type."""

    OK = "ok"
    ERROR = "error"
    OVER = "over"
