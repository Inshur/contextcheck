from typing import Any

from loguru import logger
from pydantic import BaseModel


class InterfaceBase(BaseModel):
    """UI should "know" what to do with a given object."""

    def __call__(self, obj: Any) -> Any:
        logger.info(obj)

    @staticmethod
    def summary(obj: Any, **kwargs: Any) -> Any:
        logger.info(obj)
