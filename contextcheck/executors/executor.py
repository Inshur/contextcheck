from contextcheck.endpoints.factory import factory as endpoint_factory
from contextcheck.models.models import TestResult, TestScenario, TestStep


class Executor:
    def __init__(self, test_scenario: TestScenario) -> None:
        self.test_scenario = test_scenario
        self.endpoint_under_test = endpoint_factory(
            self.test_scenario.config.endpoint_under_test
        )

    def run(self) -> None:
        for test_step in self.test_scenario.steps:
            self._run_step(test_step)

    def _run_step(self, test_step: TestStep) -> TestResult:
        request = test_step.request
        ret = self.endpoint_under_test.send_request(request)
        print(ret)

        return TestResult(passed=True)
