from pathlib import Path
from typing import Annotated, Any, Self

from pydantic import BaseModel, BeforeValidator, SerializeAsAny, field_validator, model_validator

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
    default_request: RequestBase = RequestBase()
    asserts: list[SerializeAsAny[AssertionBase]] = []
    result: bool | None = None

    @model_validator(mode="before")
    @classmethod
    def from_obj(cls, obj: dict | str) -> dict:
        # Default test step is request with `message` field
        return obj if isinstance(obj, dict) else {"name": obj, "request": RequestBase(message=obj)}

    @model_validator(mode="after")
    def use_default_request(self) -> Self:
        if self.default_request:
            self.request = self.default_request.model_copy(update=self.request.model_dump())
        return self

    @field_validator("asserts")
    @classmethod
    def prepare_asserts(cls, asserts: list[AssertionBase]) -> list[AssertionBase]:
        prepared_asserts = [assertions_factory(assert_.model_dump()) for assert_ in asserts]
        return prepared_asserts


class TestScenario(BaseModel):
    __test__ = False
    steps: list[TestStep] = []
    config: Annotated[TestConfig, BeforeValidator(lambda x: {} if x is None else x)]
    result: bool | None = None
    filename: str | None = None

    @model_validator(mode="before")
    @classmethod
    def provide_default_request_for_steps(cls, data: Any) -> Any:
        default_request = None
        steps = None
        if isinstance(data, BaseModel):
            data = data.model_dump()

        if isinstance(data, dict):
            if config := data.get("config", {}):
                if isinstance(config, dict) and config.get("default_request", {}):
                    default_request = config.get("default_request")

            steps = data.get("steps", [])

        if default_request is not None and isinstance(steps, list) and steps:
            new_steps = []
            for step in steps:
                new_step = step
                if isinstance(step, str):
                    new_step = {"name": step, "request": step, "default_request": default_request}
                elif isinstance(step, dict):
                    step["default_request"] = step.get("default_request", {}) or default_request
                new_steps.append(new_step)

            data["steps"] = new_steps
        # We can return the same data, as everything was in place
        return data

    @classmethod
    def from_yaml(cls, file_path: Path | str) -> Self:
        file_path = Path(file_path)
        cls_dict = load_yaml_file(file_path=file_path)
        cls_dict["filename"] = file_path.name
        return cls.model_validate(cls_dict)
