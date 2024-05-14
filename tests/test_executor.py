from pathlib import Path

import pytest

from contextcheck.executors.executor import Executor
from contextcheck.models.models import TestScenario


@pytest.fixture
def scenario0() -> TestScenario:
    return TestScenario.from_yaml(Path("tests/scenario0.yml"))


def test_execute_scenario(scenario0: TestScenario):
    executor = Executor()
    executor.run(scenario0)
