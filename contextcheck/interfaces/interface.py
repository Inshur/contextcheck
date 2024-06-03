from typing import Any


from pydantic import BaseModel


class InterfaceBase(BaseModel):

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        pass

    def request_callback(self, request: BaseModel) -> None:
        pass

    def response_callback(self, response: BaseModel) -> None:
        pass

    def assertion_callback(self, assertion: BaseModel) -> None:
        pass

    def finish_callback(self, test_scenario: BaseModel) -> None:
        pass
