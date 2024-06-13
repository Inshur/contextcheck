from typing import Generator

from loguru import logger

from contextcheck.endpoints.factory import factory as endpoint_factory
from contextcheck.interfaces.interface import InterfaceBase
from contextcheck.models.models import TestScenario, TestStep


class Executor:
    """
    Executes a given scenario.

    The idea here is to use executor to have all the logic needed for conducting test scenario
    basically what to "do" with the TestScenario object.
    Thus, Test* models represent mainly data handling, parsing etc.
    Doing so allows for flexible test logic definition with debugging, different outputs, concurrency etc.
    Even distributed tests later on.
    """

    def __init__(
        self,
        test_scenario: TestScenario,
        ui: InterfaceBase | None = None,
    ) -> None:
        self.test_scenario = test_scenario
        self.context: dict = {}
        self.ui = ui or InterfaceBase()
        self.endpoint_under_test = endpoint_factory(self.test_scenario.config.endpoint_under_test)

    def run_all(self) -> bool | None:
        """Run all test steps sequentially."""
        logger.info("Running scenario", self.test_scenario)
        result = True
        for test_step in self.run_steps():
            result &= bool(test_step.result)
        self.test_scenario.result = result
        return result

    def run_steps(self) -> Generator[TestStep, None, None]:
        """Run and yield steps iteratively."""
        for test_step in self.test_scenario.steps:
            yield self._run_step(test_step)

    def _run_step(self, test_step: TestStep) -> TestStep:
        """Run a given step and update result."""

        self.ui(test_step)

        request = test_step.request.build(self.context)

        self.ui(request)

        response = self.endpoint_under_test.send_request(request)
        test_step.response = response
        self._update_context(last_response=response)

        self.ui(response)

        result = True
        for assertion in test_step.asserts:
            try:
                result &= assertion(test_step, self.test_scenario.config)
            except Exception as e:
                logger.error(f"Error during assertion: {e}")
                result = False
            self.ui(assertion)
        test_step.result = result
        return test_step

    def _update_context(self, **data) -> None:
        """Update executor context to store global execution data."""
        self.context.update(data)

    def summary(self):
        self.ui.summary(self)
