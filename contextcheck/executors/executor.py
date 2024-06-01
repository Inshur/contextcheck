from typing import Generator

from loguru import logger

from contextcheck.endpoints.factory import factory as endpoint_factory
from contextcheck.interfaces.interface_tui import InterfaceTUI
from contextcheck.models.models import TestScenario, TestStep
from contextcheck.models.response import ResponseBase


class Executor:
    def __init__(self, test_scenario: TestScenario) -> None:
        self.test_scenario = test_scenario
        self.context: dict = {}
        self.ui = InterfaceTUI()
        self.endpoint_under_test = endpoint_factory(
            self.test_scenario.config.endpoint_under_test
        )

    def run_all(self) -> bool | None:
        logger.info("Running scenario", self.test_scenario)
        result = True
        for test_step in self.run_steps():
            result &= bool(test_step.result)
        self.test_scenario.result = result
        return result

    def run_steps(self) -> Generator[TestStep, None, None]:
        for test_step in self.test_scenario.steps:
            yield self._run_step(test_step)

    def _run_step(self, test_step: TestStep) -> TestStep:
        """
        The idea here is to use executor to have all the logic needed for conducting test scenario
        basically what to "do" with the TestScenario object.
        Thus, Test* models represent mainly data handling, parsing etc.
        Doing so allows for flexible test logic definition with debugging, different outputs, concurrency etc.
        Even distributed tests later on.
        """

        request = test_step.request.build(self.context)

        self.ui.request_callback(request)

        response = self.endpoint_under_test.send_request(request)
        test_step.response = response
        self._update_context(last_response=response)

        self.ui.response_callback(response)

        result = True
        for assertion in test_step.asserts:
            result &= assertion(test_step.response)
            self.ui.assertion_callback(assertion)
        test_step.result = result
        return test_step

    def _update_context(self, **data) -> None:
        self.context.update(data)
