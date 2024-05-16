from pathlib import Path

import pytest

from contextcheck.executors.executor import Executor
from contextcheck.models.models import TestScenario


def test_execute_scenario_default():
    ts = TestScenario.from_yaml(Path("tests/scenario_defaults.yml"))
    executor = Executor(ts)
    executor.run()


def test_execute_scenario_openai():
    ts = TestScenario.from_yaml(Path("tests/scenario_openai.yml"))
    executor = Executor(ts)
    executor.run()


def test_execute_scenario_cc_prompt_llm():
    ts = TestScenario.from_yaml(Path("tests/scenario_cc_prompt_llm.yml"))
    executor = Executor(ts)
    executor.run()


def test_execute_scenario_tg_chat1():
    ts = TestScenario.from_yaml(Path("tests/scenario_tg_1.yml"))
    executor = Executor(ts)
    executor.run()


def test_execute_scenario_tg_chat2():
    ts = TestScenario.from_yaml(Path("tests/scenario_tg_2.yaml"))
    executor = Executor(ts)
    executor.run()
