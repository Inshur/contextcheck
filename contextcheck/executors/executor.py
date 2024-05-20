from typing import Generator, Self

from rich import print
from rich.panel import Panel

from contextcheck.endpoints.factory import factory as endpoint_factory
from contextcheck.models.models import (
    TestScenario,
    TestScenarioResult,
    TestStep,
)


class Executor:
    def __init__(self, test_scenario: TestScenario) -> None:
        self.test_scenario = test_scenario
        self.endpoint_under_test = endpoint_factory(
            self.test_scenario.config.endpoint_under_test
        )

    def run(self) -> TestScenarioResult:
        result = True
        for test_step in self.test_scenario.steps:
            test_step = self._run_step(test_step)
            result = result and test_step.result

    def iter_steps(self) -> Generator[TestStep, None, None]:
        for test_step in self.test_scenario.steps:
            test_step = self._run_step(test_step)
            yield test_step

    def _run_step(self, test_step: TestStep) -> TestStep:
        request = test_step.request
        print(Panel("[bold red]:speech_balloon: Request:"))
        print(request)
        response = self.endpoint_under_test.send_request(request)
        print(Panel("[bold red]:balloon: Response:"))
        print(response)
        test_step.response = response
        print(Panel("[bold red]:face_with_monocle: Validation:"))

        test_step.result = True

        for assert_ in test_step.asserts:
            assert_.check(test_step.response)
            test_step.result &= assert_.result
            print(assert_)
        return test_step
