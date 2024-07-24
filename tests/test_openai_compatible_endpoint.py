import pytest

from tests.utils import executor

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


@pytest.mark.parametrize("executor", [invalid_config], indirect=True)
def test_invalid_config(executor):
    with pytest.raises(ValueError, match="Provider 'Foo' not found"):
        executor.run_all()


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
