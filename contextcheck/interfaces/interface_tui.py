from pydantic import BaseModel
from rich import print
from rich.console import Group
from rich.panel import Panel
from rich.pretty import Pretty
from rich.text import Text


class InterfaceTUI(BaseModel):

    # def model_post_init(self, ctx) -> None:
    #     self._console: Console = Console()

    def request_callback(self, request: BaseModel) -> None:
        g = Group(
            Text("🎈 Request:", style="bold red"),
            Pretty(request),
        )
        print(Panel(g, width=80))

    def response_callback(self, response: BaseModel) -> None:
        g = Group(
            Text("💬 Response:", style="bold red"),
            Pretty(response),
        )
        print(Panel(g, width=80))

    def assertion_callback(self, assertion: BaseModel) -> None:
        g = Group(
            Text("🧐 Assertion:", style="bold red"),
            Pretty(assertion),
        )
        print(Panel(g, width=80))

    def finish_callback(self, test_scenario: BaseModel) -> None:
        pass
