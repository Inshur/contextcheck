from pathlib import Path

from contextcheck import TestScenario


def test_load_scenario0():
    ts = TestScenario.from_yaml(Path("tests/scenario_openai.yml"))
    assert len(ts.steps) == 2
    assert ts.steps[0].message == "Write success in the response"
    assert ts.steps[0].name == "Write success in the response"
    assert ts.steps[1].message == "Hello!"
    assert ts.steps[1].name == "Send hello"


def test_load_scenario01():
    ts = TestScenario.from_yaml(Path("tests/scenario_openai.yml"))
    assert len(ts.steps) == 2
