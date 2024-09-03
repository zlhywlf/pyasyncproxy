"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

import logging
from collections.abc import Generator
from importlib import import_module
from importlib.resources import files
from importlib.resources.abc import Traversable
from types import ModuleType
from typing import Any

logger = logging.getLogger(__name__)


def get_modules(pkg: str) -> Generator[ModuleType | None, Any, None]:
    """Retrieve all modules from the specified package."""

    def get_module(module_meta: Traversable) -> ModuleType | None:
        """Get module."""
        name, point, suffix = module_meta.name.rpartition(".")
        if not module_meta.is_file() or suffix != "py" or name == "__init__":
            return None
        try:
            return import_module(f"{point}{name}", pkg)
        except ModuleNotFoundError as e:
            logger.warning(f"{pkg}{point}{name}:{e}")
            return None

    return (get_module(module_meta) for module_meta in files(pkg).iterdir())
