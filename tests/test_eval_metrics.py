import pytest

from tests.utils import executor

config_eval_message = """
config:
    endpoint_under_test:
        kind: echo

steps:
  - name: test eval message
    request: 'Foo bar foo'
    asserts:
      - eval: '"Foo" in response.message'
      - eval: '"bar" in response.message'
      - eval: '"Foo bar foo" == response.message'
      - eval: '"fo fo" in response.message'
"""

config_eval_stats = """
config:
    endpoint_under_test:
        kind: echo

steps:
  - name: test eval stats
    request: 'Foo bar foo'
    asserts:
      - eval: 'response.stats.tokens_request is None'
      - eval: 'response.stats.tokens_response is None'
      - eval: 'response.stats.tokens_total is None'
      - eval: 'response.stats.tokens_total == 1232'
"""

config_eval_build = """
config:
    endpoint_under_test:
        kind: echo

steps:
  - name: test eval build
    request: 'Foo'
    asserts:
      - eval: '"Foo" == response.message'
  - name: test eval build
    request:
      message:
        eval: last_response.message + ' Bar'
    asserts:
      - eval: '"Foo Bar" == response.message'
  - name: test eval build
    request:
      message:
        eval: last_response.message
    asserts:
      - eval: '"Foo Bar" in response.message'
"""


@pytest.mark.parametrize("executor", [config_eval_message], indirect=True)
def test_eval_messages(executor):
    executor.run_all()

    # Test: eval
    assert executor.test_scenario.steps[0].asserts[0].result is True
    assert executor.test_scenario.steps[0].asserts[1].result is True
    assert executor.test_scenario.steps[0].asserts[2].result is True
    assert executor.test_scenario.steps[0].asserts[3].result is False


@pytest.mark.parametrize("executor", [config_eval_stats], indirect=True)
def test_eval_stats(executor):
    executor.run_all()

    # Test: eval
    assert executor.test_scenario.steps[0].asserts[0].result is True
    assert executor.test_scenario.steps[0].asserts[1].result is True
    assert executor.test_scenario.steps[0].asserts[2].result is True
    assert executor.test_scenario.steps[0].asserts[3].result is False


@pytest.mark.parametrize("executor", [config_eval_build], indirect=True)
def test_eval_build(executor):
    executor.run_all()

    # Test: eval
    assert executor.test_scenario.steps[0].asserts[0].result is True
    assert executor.test_scenario.steps[1].asserts[0].result is True
    assert executor.test_scenario.steps[2].asserts[0].result is True
