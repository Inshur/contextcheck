from contextcheck.models.models import TestScenario


class Executor:
    def __init__(self) -> None:
        pass

    def run(self, test_scenario: TestScenario) -> None:
        print(test_scenario)
