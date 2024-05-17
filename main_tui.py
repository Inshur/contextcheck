import json
from pathlib import Path

from rich import box, print
from rich.live import Live
from rich.pretty import Pretty
from rich.syntax import Syntax
from rich.table import Table, Text

from contextcheck.executors.executor import Executor
from contextcheck.models.models import TestScenario

ts = TestScenario.from_yaml(Path("tests/scenario_tg_2.yaml"))
# ts = TestScenario.from_yaml(Path("tests/scenario_cc_prompt_llm.yml"))
executor = Executor(ts)


table = Table(show_lines=True)
table.add_column("Request")
table.add_column("Response")
table.add_column("Valid")

print(ts.config)


with Live(table, refresh_per_second=4):  # update 4 times a second to feel fluid
    for tsr in executor.run():
        table.add_row(
            Pretty(tsr.request),
            Pretty(tsr.response),
            "[green]OK",
        )
