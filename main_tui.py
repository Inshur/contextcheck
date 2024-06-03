from contextcheck.executors.executor import Executor
from contextcheck.interfaces.interface_tui import InterfaceTUI
from contextcheck.models.models import TestScenario

ui = InterfaceTUI()


ts = TestScenario.from_yaml(ui.get_scenario_path())


executor = Executor(ts, ui=ui)
executor.run_all()

executor.summary()
