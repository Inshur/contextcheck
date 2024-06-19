from pathlib import Path
from typing import Annotated, ClassVar, Self

from pydantic import BaseModel, BeforeValidator, field_validator, model_validator

from contextcheck.assertions.assertions import AssertionBase
from contextcheck.assertions.factory import factory as assertions_factory
from contextcheck.endpoints.endpoint_config import EndpointConfig
from contextcheck.loaders.yaml import load_yaml_file
from contextcheck.models.request import RequestBase
from contextcheck.models.response import ResponseBase


class TestConfig(BaseModel):
    endpoint_under_test: EndpointConfig = EndpointConfig()
    default_request: RequestBase | None = None
    eval_endpoint: EndpointConfig | None = None


class TestStep(BaseModel):
    name: str
    request: RequestBase
    response: ResponseBase | None = None
    default_request: ClassVar[RequestBase] = RequestBase()
    asserts: list[AssertionBase] = []
    result: bool | None = None

    @model_validator(mode="before")
    @classmethod
    def from_obj(cls, obj: dict | str) -> dict:
        # Default test step is request with `message` field
        return (
            obj
            if isinstance(obj, dict)
            else {"name": obj, "request": RequestBase(message=obj)}
        )

    @field_validator("request")
    @classmethod
    def use_default_request(cls, req: RequestBase) -> RequestBase:
        return cls.default_request.model_copy(update=req.model_dump())

    @field_validator("asserts")
    @classmethod
    def prepare_asserts(cls, asserts: list[AssertionBase]) -> list[AssertionBase]:
        return [assertions_factory(assert_.model_dump()) for assert_ in asserts]


class TestScenario(BaseModel):
    __test__ = False
    steps: list[TestStep] = []
    config: Annotated[TestConfig, BeforeValidator(lambda x: {} if x is None else x)]
    result: bool | None = None

    @classmethod
    def from_yaml(cls, file_path: Path) -> Self:
        cls_dict = load_yaml_file(file_path)

        # Get config here to set default request
        config = TestConfig.model_validate(cls_dict.get("config", {}) or {})
        if config.default_request:
            TestStep.default_request = config.default_request

        return cls.model_validate(cls_dict)
