from typing import Self

from contextcheck.endpoints.factory import factory as endpoint_factory
from contextcheck.models.models import TestResult, TestScenario, TestStep


class Executor:
    def __init__(self, test_scenario: TestScenario) -> None:
        self.test_scenario = test_scenario
        self.endpoint_under_test = endpoint_factory(
            self.test_scenario.config.endpoint_under_test
        )

    def run(self) -> TestStep:
        for test_step in self.test_scenario.steps:
            test_step = self._run_step(test_step)
            yield test_step

    def _run_step(self, test_step: TestStep) -> TestStep:
        request = test_step.request
        response = self.endpoint_under_test.send_request(request)
        test_step.response = response
        return test_step
