from typing import Annotated

from pydantic import BaseModel
from rich import print
from rich.console import Console, Group
from rich.panel import Panel
from rich.text import Text


class InterfaceTUI(BaseModel):

    def model_post_init(self, ctx) -> None:
        self._console: Console = Console()

    def request_callback(self, request: BaseModel) -> None:
        g = Group(
            self._console.render_str("[bold red]🎈 Request:"),
            self._console.render_str(str(request)),
        )
        print(Panel(g, width=80))

    def response_callback(self, response: BaseModel) -> None:
        g = Group(
            self._console.render_str("[bold red]💬 Response:"),
            self._console.render_str(str(response)),
        )
        print(Panel(g, width=80))

    def assertion_callback(self, assertion: BaseModel) -> None:
        g = Group(
            self._console.render_str("[bold red]🧐 Assertion:"),
            self._console.render_str(str(assertion)),
        )
        print(Panel(g, width=80))

    def finish_callback(self, test_scenario: BaseModel) -> None:
        pass
