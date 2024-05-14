from typing import Self

from openai import BaseModel


class ConnectorBase(BaseModel):

    @classmethod
    def from_config_dict(d: dict) -> Self:
        pass
