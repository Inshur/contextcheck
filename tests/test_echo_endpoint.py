from pathlib import Path

from contextcheck import TestScenario
from contextcheck.endpoints.endpoint import EndpointConfig
from contextcheck.endpoints.endpoint_dummy_echo import EndpointDummyEcho
from contextcheck.executors.executor import Executor


def test_load_scenario_from_yaml():
    ts = TestScenario.from_yaml(Path("tests/scenario_echo.yaml"))
    assert isinstance(ts.config.endpoint_under_test, EndpointConfig)
    assert ts.config.endpoint_under_test.kind == "echo"
    assert ts.config.default_request.chat_uuid == "0xdead"
    assert len(ts.steps) == 4
    assert ts.steps[0].request.message == "Write success in the response"
    assert ts.steps[0].request.chat_uuid == "0xdead"
    assert ts.steps[0].name == "Write success in the response"
    assert ts.steps[1].request.message == "Hello!"
    assert ts.steps[1].request.chat_uuid == "0x00"
    assert ts.steps[1].name == "Send hello"
    assert len(ts.steps[2].asserts) == 3
    assert ts.steps[2].asserts[0].eval == "True == True"
    assert ts.steps[2].asserts[1].eval == 'response.message == "Hello!"'
    assert ts.steps[2].asserts[2].eval == 'response.chat_uuid == "0x11"'


def test_run():
    ts = TestScenario.from_yaml(Path("tests/scenario_echo.yaml"))
    executor = Executor(ts)
    assert isinstance(executor.endpoint_under_test, EndpointDummyEcho)
    assert executor.test_scenario.result is None
    for step in executor.test_scenario.steps:
        assert step.result is None
        assert step.response is None
    executor.run()
    ts = executor.test_scenario

    assert ts.result is not None
    assert ts.result is False

    for step in ts.steps:
        assert step.result is not None
        assert step.response is not None

    assert ts.steps[0].response.message == "Write success in the response"

    assert ts.steps[1].response.message == "Hello!"
    assert ts.steps[1].response.chat_uuid == "0x00"

    assert ts.steps[2].asserts[0].result is True
    assert ts.steps[2].asserts[1].result is False

    assert ts.steps[0].response.stats is not None
    assert ts.steps[0].response.stats.tokens_total is None
