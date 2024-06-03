import argparse
from pathlib import Path
from typing import Any

from pydantic import BaseModel
from rich import print
from rich.console import Group, RenderableType
from rich.panel import Panel
from rich.pretty import Pretty
from rich.table import Table
from rich.text import Text

from contextcheck.assertions.assertions import AssertionBase
from contextcheck.executors.executor import Executor
from contextcheck.interfaces.interface import InterfaceBase
from contextcheck.models.models import TestScenario, TestStep
from contextcheck.models.request import RequestBase
from contextcheck.models.response import ResponseBase


def _create_panel(text: str, obj: BaseModel, width: int = 80) -> RenderableType:
    return Panel(
        Group(
            Text(text, style="bold red"),
            Pretty(obj),
        ),
        width=width,
    )


class InterfaceTUI(InterfaceBase):
    _test_scenario_filename: str | None = None

    def model_post_init(self, __context: Any) -> None:
        super().model_post_init(__context)
        parser = argparse.ArgumentParser(
            prog="ContextCheck", description="Perform test scenario."
        )
        parser.add_argument("filename")
        args = parser.parse_args()
        self._test_scenario_filename = args.filename
        return

    def get_scenario_path(self) -> Path:
        return Path(self._test_scenario_filename or "")

    def __call__(self, obj: BaseModel) -> Any:
        if isinstance(obj, TestStep):
            print(obj)
            return
        elif isinstance(obj, ResponseBase):
            text = "💬 Response:"
        elif isinstance(obj, RequestBase):
            text = "🎈 Request:"
        elif isinstance(obj, AssertionBase):
            text = "🧐 Assertion:"
        else:
            text = "Unknown"
        print(_create_panel(text, obj))

    @staticmethod
    def summary(executor: Executor):
        table = Table(show_lines=True)
        table.add_column("Request")
        table.add_column("Response")
        table.add_column("Asserts")
        table.add_column("Valid")

        for step in executor.test_scenario.steps:
            table.add_row(
                Pretty(step.request),
                Pretty(step.response),
                Pretty(step.asserts),
                "[green]OK" if step.result else "[red]FAIL",
            )

        print(table)
