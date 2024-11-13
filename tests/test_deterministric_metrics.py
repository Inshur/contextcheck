from pathlib import Path

import pytest

from contextcheck import TestScenario
from tests.utils import executor

config_contains = """
config:
    endpoint_under_test:
        kind: echo

steps:
  - name: test contains and icontains
    request: 'Foo bar'
    asserts:
      - kind: contains
        assertion: 'Foo'
      - kind: contains
        assertion: 'something else'
      - kind: icontains
        assertion: 'foo'
"""


@pytest.mark.parametrize("executor", [config_contains], indirect=True)
def test_contains(executor):
    executor.run_all()

    # Test: contains
    assert executor.test_scenario.steps[0].asserts[0].result == True
    assert executor.test_scenario.steps[0].asserts[1].result == False

    # Test: icontains
    assert executor.test_scenario.steps[0].asserts[2].result == True


config_contains_all = """
config:
    endpoint_under_test:
        kind: echo

steps:
  - name: test contains-all and icontains-all
    request: 'Quick brown fox jumps over the lazy dog'
    asserts:
      - kind: contains-all
        assertion: ['Quick', 'fox']
      - kind: contains-all
        assertion: ['Quick', 'something else']
      - kind: icontains-all
        assertion: ['quick', 'fox']
"""


@pytest.mark.parametrize("executor", [config_contains_all], indirect=True)
def test_contains_all(executor):
    executor.run_all()

    # Test: contains-all
    assert executor.test_scenario.steps[0].asserts[0].result == True
    assert executor.test_scenario.steps[0].asserts[1].result == False

    # Test: icontains-all
    assert executor.test_scenario.steps[0].asserts[2].result == True


config_contains_any = """
config:
    endpoint_under_test:
        kind: echo

steps:
  - name: test contains-any and icontains-any
    request: 'Quick brown fox jumps over the lazy dog'
    asserts:
      - kind: contains-any
        assertion: ['Quick', 'something else']
      - kind: contains-any
        assertion: ['something else', 'and', 'more']
      - kind: icontains-any
        assertion: ['quick', 'something else']
"""


@pytest.mark.parametrize("executor", [config_contains_any], indirect=True)
def test_contains_any(executor):
    executor.run_all()

    # Test: contains-any
    assert executor.test_scenario.steps[0].asserts[0].result == True
    assert executor.test_scenario.steps[0].asserts[1].result == False

    # Test: icontains-any
    assert executor.test_scenario.steps[0].asserts[2].result == True


config_is_valid_json = """
config:
    endpoint_under_test:
        kind: echo

steps:
  - name: test is-valid-json
    request: '{"name": "John", "age": 30}'
    asserts:
      - kind: is-valid-json
"""


@pytest.mark.parametrize("executor", [config_is_valid_json], indirect=True)
def test_is_valid_json(executor):
    executor.run_all()

    assert executor.test_scenario.steps[0].asserts[0].result == True


config_has_valid_json_schema = """
config:
    endpoint_under_test:
        kind: echo

steps:
  - name: test has-valid-json-schema
    request: '{"name": "John", "age": 30}'
    asserts:
      - kind: has-valid-json-schema
        assertion:
            type: object
            properties:
                name:
                    type: string
                age:
                    type: number
                    minimum: 0
                    maximum: 150
            required: ["name", "age"]
      - kind: has-valid-json-schema
        assertion:
            type: object
            properties:
                name:
                    type: string
                age:
                    type: number
                    minimum: 0
                    maximum: 150
                city:
                    type: string
            required: ["name", "age", "city"]
"""


@pytest.mark.parametrize("executor", [config_has_valid_json_schema], indirect=True)
def test_has_valid_json_schema(executor):
    executor.run_all()

    assert executor.test_scenario.steps[0].asserts[0].result == True
    assert executor.test_scenario.steps[0].asserts[1].result == False


config_equals = """
config:
    endpoint_under_test:
        kind: echo

steps:
  - name: test is-valid-json
    request: 'Foo'
    asserts:
      - kind: equals
        assertion: 'Foo'
"""


@pytest.mark.parametrize("executor", [config_equals], indirect=True)
def test_equals(executor):
    executor.run_all()

    assert executor.test_scenario.steps[0].asserts[0].result == True


config_regex = """
config:
    endpoint_under_test:
        kind: echo

steps:
  - name: test regex
    request: 'Foo16 bar'
    asserts:
      - kind: regex
        assertion: '^\w+\d{2} \w+$'
      - kind: regex
        assertion: \d+
"""


@pytest.mark.parametrize("executor", [config_regex], indirect=True)
def test_regex(executor):
    executor.run_all()

    assert executor.test_scenario.steps[0].asserts[0].result == True
    assert executor.test_scenario.steps[0].asserts[1].result == False


config_regex_2 = """
config:
    endpoint_under_test:
        kind: echo

steps:
  - name: test regex
    request: 'Foo16 bar'
    asserts:
      - kind: regex
        assertion: "\w+" # This fails because regex is in double quotes
"""


def test_regex_exception(tmp_path: Path):
    temp_file = tmp_path / "test.yaml"
    temp_file.write_text(config_regex_2)

    with pytest.raises(
        ValueError, match="Yaml parsing error. It was probably caused by your 'regex' assertion"
    ):
        TestScenario.from_yaml(temp_file)
