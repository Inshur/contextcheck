from pathlib import Path

import pytest
from rich import print

from contextcheck.executors.executor import Executor
from contextcheck.models.models import TestScenario


def test_assert_1():
    ts = TestScenario.from_yaml(Path("tests/scenario_openai.yml"))
    executor = Executor(ts)
    executor.run()
