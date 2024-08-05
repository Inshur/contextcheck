# Understanding test scenarios

## What are test scenarios

Test scenario is an file in a YAML format.

**It consists of 3 sections:** 

* `config` - where you define what system or LLM you are going to test, and (if you are going to use LMM-based metrics) configure LLM that is going to be used for evaluation

* `steps` - actual tests used against your endpoint

* `variables` - optional section to define variables that can be used throughout `config` and `steps` sections


**On a high level, single test scenario:**

* Executes tests against single LLM or LMM-like system (e.g. RAG)

* Can have multiple tests `steps`

* Each step can have multiple `assertions`, each assertion uses a specific metric that checks if assertion passes or fails.

* If all `assertions` from single step pass, step test is marked as "passed"

* If all `steps` pass, the scenario is considered as "passed"


Together with ContextCheck CLI, you can execute single test scenario, list of scenarios or all scenarios from a selected folder. Refer to [CLI documentation]() for details.

### The `config` section

The section in it's most basic format:
```yaml
config:
  endpoint_under_test:
    kind: openai
```

Here we are going to use OpenAI model to test our prompts. By default the model version used is `gpt-4o-mini`.

You can change model:
```yaml
config:
  endpoint_under_test:
    kind: openai
    model: gpt-4o
```

Or use another provider. Example below shows how to use local `llama3:8b` model from `Ollama` provider:
```yaml
config:
  endpoint_under_test:
    kind: openai_compatible
    provider: ChatOllama
    model: llama3:8b
```

ContextCheck integrates the most popular providers like:

* ChatOpenAI

* BedrockChat

* AzureChatOpenAI

* ChatDatabricks

* ChatAnthropic

* ChatCohere

* ChatGooglePalm

* ChatMlflow

* ChatOllama

* ChatVertexAI


For provider-specific configuration refer to [LangChain Chat Models](https://python.langchain.com/v0.2/docs/integrations/chat/) documentation. You will need to setup environment variables and/or model name required by the provider.

**#TODO**

* **default request**

* **defining your own endpoint**

* **passing additional parameters in headers**



#### LMM-based evaluator configuration

If you are going to use [LLM-based metrics]() to validate your `endpoint_under_test`, then you need to 

In it's simplest format it looks as follows:
```yaml
config:
  endpoint_under_test:
    kind: openai
  eval_endpoint:
    kind: openai
```

It is recommended to use powerful model, like e.g. `gpt-4o` to perform your LLM-driven evaluations.

The configuration for `eval_endpoint` is identical to that of `endpoint_under_test`, making all the preceding points applicable.

### The `steps` section

```yaml
steps:
  - name: Test hallucination evaluator (hallucinated)
    request:
      message: Where did Mike go? Choose between the home and the park.
    asserts:
      - llm_metric: hallucination
        reference: Mike went to the store.
```


### The `variables` section

**#TODO**

## How to configure test scenario

## Defining steps

**#TODO**
* Available metrics
	* Deterministic metrics
	* LLM-based metrics

**#TODO**
Steps:
* understand YAML syntax
* write your first test
* execute with CLI and check results
