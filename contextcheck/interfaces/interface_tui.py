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
    test_scenario_filename: str | None = None

    def get_scenario_path(self) -> Path:
        return Path(self.test_scenario_filename or "")

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

    def summary(self, executor: Executor, **kwargs: Any) -> None:
        table = Table(show_lines=True)
        table.add_column("Request")
        table.add_column("Response")
        table.add_column("Asserts")
        table.add_column("Valid")

        for step in executor.test_scenario.steps:
            step_result = ""
            if step.result is None:
                step_result = "[yellow]SKIPPED"
            elif step.result:
                step_result = "[green]OK"
            else:
                step_result = "[red]FAIL"

            table.add_row(
                Pretty(step.request),
                Pretty(step.response),
                Pretty(step.asserts),
                step_result,
            )

        print(table)

        if kwargs.get("aggregate_results", False):
            self.report_results(executor=executor)

    def report_results(self, executor: Executor) -> None:
        scenario_results = self._create_a_summary_report(executor=executor)

        # NOTE: Now we have only binary statistics, but if we were to add "continous assertions"
        # then we'd need to either update this table, or create a separate table for continous results
        # Although we could also add some new overlapping metrics like max, min, median etc.
        table = Table(show_lines=True)
        table.add_column("Metric type")  # LLM Metric, eval etc.
        table.add_column("Metric name")  # Name of the metric e.g. LLM-Metric / qa-reference
        table.add_column("Mean score")
        table.add_column("Test count")

        for key, value in scenario_results.items():
            for key2, value2 in value.items():
                table.add_row(
                    Pretty(key),
                    Pretty(key2),
                    Pretty(value2["mean"]),
                    Pretty(value2["count"]),
                )

        print(table)
