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
        exit_on_failure: bool = False,
    ) -> None:
        self.test_scenario = test_scenario
        self.context: dict = {}
        self.ui = ui or InterfaceBase()
        self.exit_on_failure = exit_on_failure
        self.endpoint_under_test = endpoint_factory(self.test_scenario.config.endpoint_under_test)
        self.eval_endpoint = (
            endpoint_factory(self.test_scenario.config.eval_endpoint)
            if self.test_scenario.config.eval_endpoint
            else None
        )
        self.early_stop = False

    def run_all(self) -> bool | None:
        """Run all test steps sequentially."""
        logger.info("Running scenario", self.test_scenario)
        result = True
        for test_step in self.run_steps():
            result &= bool(test_step.result)
            if self.early_stop:
                break
        self.test_scenario.result = result
        return result

    def run_steps(self) -> list[TestStep]:
        """Run and yield steps iteratively."""
        step_results = []
        for test_step in self.test_scenario.steps:
            if self.early_stop:
                break
            step = self._run_step(test_step)
            step_results.append(step)
        return step_results

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
                result &= assertion(request, response, eval_endpoint=self.eval_endpoint)
            except Exception as e:
                logger.error(f"Error during assertion: {e}")
                result = False
            self.ui(assertion)
            if result is False and self.exit_on_failure:
                self.early_stop = True
                break
        test_step.result = result
        return test_step

    def _update_context(self, **data) -> None:
        """Update executor context to store global execution data."""
        self.context.update(data)

    def summary(self, **kwargs: dict[str, str]):
        self.ui.summary(self, **kwargs)

    def report_results(self, **kwargs: dict[str, str]):
        # This function isn't utilized on it's own right now, but is rather used by summary
        # at least for tui interface, though I leave it as a separate accessible function
        self.ui.report_results(self, **kwargs)
