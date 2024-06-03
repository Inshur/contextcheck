from typing import Any

from pydantic import BaseModel
from rich import print
from rich.console import Group, RenderableType
from rich.live import Live
from rich.panel import Panel
from rich.pretty import Pretty
from rich.table import Table
from rich.text import Text

from contextcheck.assertions.assertions import AssertionBase
from contextcheck.models.models import TestStep
from contextcheck.models.request import RequestBase
from contextcheck.models.response import ResponseBase


def _create_panel(text: str, obj: BaseModel) -> RenderableType:
    return Panel(
        Group(
            Text(text, style="bold red"),
            Pretty(obj),
        ),
        width=80,
    )


class InterfaceTUI(BaseModel):

    def __call__(self, obj: BaseModel) -> Any:
        if isinstance(obj, TestStep):
            pass
        elif isinstance(obj, ResponseBase):
            text = "💬 Response:"
        elif isinstance(obj, RequestBase):
            text = "🎈 Request:"
        elif isinstance(obj, AssertionBase):
            text = "🧐 Assertion:"
        else:
            text = "Unknown"
        print(_create_panel(text, obj))
