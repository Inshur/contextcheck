from pathlib import Path

from contextcheck.executors.executor import Executor
from contextcheck.models.models import TestScenario

ts = TestScenario.from_yaml(Path("tests/scenario_echo.yaml"))
# ts = TestScenario.from_yaml(Path("tests/scenario_cc_prompt_llm.yml"))
# ts = TestScenario.from_yaml(Path("tests/scenario_openai.yml"))

executor = Executor(ts)
executor.run_all()


# table = Table(show_lines=True)
# table.add_column("Request")
# table.add_column("Response")
# table.add_column("Valid")

# print(ts.config)


# with Live(table, refresh_per_second=4):  # update 4 times a second to feel fluid
#     for tsr in executor.run_steps():
#         table.add_row(
#             Pretty(tsr.request.message),
#             Pretty(tsr.response),
#             Pretty(tsr.asserts),
#             "[green]OK" if tsr.result else "[red]FAIL",
#         )
