from pathlib import Path
from tempfile import NamedTemporaryFile
import pytest

from contextcheck import TestScenario
from tests.utils import executor
from contextcheck.executors.executor import Executor

invalid_config = """
config:
    endpoint_under_test:
        kind: openai_compatible
        provider: Foo
        model: bar

steps:
   - 'foo'
"""

ollama_config = """
config:
   endpoint_under_test:
      kind: openai_compatible
      provider: ChatOllama
      model: llama3:8b

steps:
   - name: Send hello
     request: 'Say "Hello"'
     asserts:
        - '"Hello" in response.message'      
"""

openai_config = """
config:
   endpoint_under_test:
      kind: openai_compatible
      provider: ChatOpenAI
      model: gpt-4o-mini
      temperature: 0.5
      max_tokens: 5
"""


def test_invalid_config():
    with NamedTemporaryFile("w", suffix=".yaml") as f:
        f.write(invalid_config)
        f.flush()

        with pytest.raises(ValueError, match="Provider 'Foo' not found"):
            ts = TestScenario.from_yaml(Path(f.name))
            Executor(test_scenario=ts)


@pytest.mark.parametrize("executor", [ollama_config], indirect=True)
def test_ollama_config(executor):
    assert executor.endpoint_under_test.connector.model == "llama3:8b"
    assert executor.endpoint_under_test.connector.provider == "ChatOllama"


@pytest.mark.ollama
@pytest.mark.parametrize("executor", [ollama_config], indirect=True)
def test_ollama_result(executor):
    executor.run_all()
    assert executor.test_scenario.result == True


@pytest.mark.parametrize("executor", [openai_config], indirect=True)
def test_openai_config(executor):
    assert executor.endpoint_under_test.connector.model == "gpt-4o-mini"
    assert executor.endpoint_under_test.connector.provider == "ChatOpenAI"
    assert executor.endpoint_under_test.connector.temperature == 0.5
    assert executor.endpoint_under_test.connector.max_tokens == 5


@pytest.mark.openai
@pytest.mark.parametrize("executor", [openai_config], indirect=True)
def test_openai_result(executor):
    executor.run_all()
    assert executor.test_scenario.result == True
