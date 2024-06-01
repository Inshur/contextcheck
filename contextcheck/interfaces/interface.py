from pydantic import BaseModel


class InterfaceBase(BaseModel):

    def request_callback(self, request: dict) -> None:
        pass

    def response_callback(self, response: dict) -> None:
        pass

    def assertion_callback(self, assertion: dict) -> None:
        pass

    def finish_callback(self, test_scenario: dict) -> None:
        pass
