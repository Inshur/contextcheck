from contextcheck.endpoints.endpoint import factory
from contextcheck.endpoints.endpoint_cc_prompt_llm import EndpointCCPromptLLM
from contextcheck.endpoints.endpoint_openai import EndpointOpenAI
from contextcheck.models.models import TestResult, TestScenario, TestStep


class Executor:
    def __init__(self, test_scenario: TestScenario) -> None:
        self.test_scenario = test_scenario
        self.endpoint_under_test = factory(self.test_scenario.config.endpoint_under_test)

    def run(self) -> None:
        for test_step in self.test_scenario.steps:
            self._run_step(test_step)

    def _run_step(self, test_step: TestStep) -> TestResult:
        message = self.endpoint_under_test.prepare_message(test_step)
        print(message)
        ret = self.endpoint_under_test.send_message(message)
        print(ret)

        return TestResult(passed=True)
