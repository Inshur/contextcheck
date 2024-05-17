from pathlib import Path
from typing import Annotated, ClassVar, Self

from pydantic import (
    BaseModel,
    BeforeValidator,
    field_validator,
    model_validator,
)

from contextcheck.endpoints.endpoint import EndpointConfig
from contextcheck.loaders.yaml import load_yaml_file
from contextcheck.models.request import RequestBase
from contextcheck.models.response import ResponseBase


class TestConfig(BaseModel):
    endpoint_under_test: EndpointConfig = EndpointConfig()
    default_request: RequestBase | None = None


class TestStep(BaseModel):
    name: str
    request: RequestBase
    response: ResponseBase | None = None
    default_request: ClassVar[RequestBase] = RequestBase()

    @model_validator(mode="before")
    @classmethod
    def from_obj(cls, obj: dict | str) -> dict:
        return (
            obj
            if type(obj) is dict
            else {"name": obj, "request": RequestBase(message=obj)}
        )

    @field_validator("request")
    @classmethod
    def use_default_request(cls, req: RequestBase) -> RequestBase:
        return cls.default_request.model_copy(update=req.model_dump())


class TestScenario(BaseModel):
    __test__ = False
    steps: list[TestStep] = []
    config: Annotated[
        TestConfig, BeforeValidator(lambda x: {} if x is None else x)
    ]

    @classmethod
    def from_yaml(cls, file_path: Path) -> Self:
        cls_dict = load_yaml_file(file_path)
        config = TestConfig.model_validate(cls_dict.get("config", {}) or {})
        if config.default_request:
            TestStep.default_request = config.default_request
        klass = cls.model_validate(cls_dict)
        return klass


class TestResult(TestScenario):
    passed: bool
