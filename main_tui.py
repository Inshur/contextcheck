from pathlib import Path

from rich import print
from rich.live import Live
from rich.pretty import Pretty
from rich.table import Table

from contextcheck.executors.executor import Executor
from contextcheck.models.models import TestScenario

ts = TestScenario.from_yaml(Path("tests/scenario_tg_qa1.yaml"))
# ts = TestScenario.from_yaml(Path("tests/scenario_cc_prompt_llm.yml"))
# ts = TestScenario.from_yaml(Path("tests/scenario_openai.yml"))

executor = Executor(ts)


table = Table(show_lines=True)
table.add_column("Request")
table.add_column("Response")
table.add_column("Valid")

print(ts.config)


with Live(table, refresh_per_second=4):  # update 4 times a second to feel fluid
    for tsr in executor.iter_steps():
        table.add_row(
            Pretty(tsr.request.message),
            Pretty(tsr.response.reply),
            Pretty(tsr.asserts),
            "[green]OK" if tsr.result else "[red]FAIL",
        )
