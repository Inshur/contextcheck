from typing import Generator

from loguru import logger
from rich import print
from rich.panel import Panel

from contextcheck.endpoints.factory import factory as endpoint_factory
from contextcheck.models.models import TestScenario, TestStep
from contextcheck.models.response import ResponseBase


class Executor:
    def __init__(self, test_scenario: TestScenario) -> None:
        self.test_scenario = test_scenario
        self.endpoint_under_test = endpoint_factory(
            self.test_scenario.config.endpoint_under_test
        )
        self.last_response: ResponseBase | None = None

    def run_all(self) -> bool | None:
        logger.info("Running scenario", self.test_scenario)
        result = True
        for test_step in self.run_steps():
            result = result and test_step.result
        self.test_scenario.result = result
        return result

    def run_steps(self) -> Generator[TestStep, None, None]:
        for test_step in self.test_scenario.steps:
            test_step = self._run_step(test_step)
            yield test_step

    def _run_step(self, test_step: TestStep) -> TestStep:
        # Set context for response build
        context = {"last_response": self.last_response}
        request = test_step.request.build(context)
        print(Panel("[bold red]:speech_balloon: Request:"))
        print(request)
        response = self.endpoint_under_test.send_request(request)
        print(Panel("[bold red]:balloon: Response:"))
        print(response)
        test_step.response = response
        self.last_response = response
        print(Panel("[bold red]:face_with_monocle: Validation:"))

        test_step.result = True

        for assert_ in test_step.asserts:
            test_step.result &= assert_(test_step.response)
            print(assert_)
        return test_step
