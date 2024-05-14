from pathlib import Path

from contextcheck import TestScenario


def test_load_scenario0():
    ts = TestScenario.from_yaml(Path("tests/scenario0.yml"))
    assert ts.config.endpoint_url == "http://0.0.0.0:8000/api/v1/"
    assert ts.config.additional_headers is None
    assert len(ts.steps) == 2
    assert ts.steps[0].message == "Write success in the response"
    assert ts.steps[0].name == "Write success in the response"
    assert ts.steps[1].message == "Hello!"
    assert ts.steps[1].name == "Send hello"
