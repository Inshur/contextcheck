from pathlib import Path

from contextcheck import TestScenario


def test_load_scenario0():
    ts = TestScenario.from_yaml(Path("tests/scenario_openai.yml"))
    assert len(ts.steps) == 2
    assert ts.steps[0].message.message == "Write success in the response"
    assert ts.steps[0].name == "Write success in the response"
    assert ts.steps[1].message.message == "Hello!"
    assert ts.steps[1].name == "Send hello"


def test_load_scenario01():
    ts = TestScenario.from_yaml(Path("tests/scenario_openai.yml"))
    assert len(ts.steps) == 2


def test_load_variables():
    ts = TestScenario.from_yaml(Path("tests/scenario_tg_1.yml"))

    assert ts.steps[1].message.chat_uuid == "123e4567-e89b-12d3-a456-426614174000"
    assert ts.steps[1].message.asr_build == "{}"

    assert ts.steps[2].message.message == "[reset]"
    assert ts.steps[2].message.sender_name == "John Doe"

    assert ts.steps[3].message.message == "[qa] Hello!"
    assert ts.steps[3].message.sender_name == "John Doe"
