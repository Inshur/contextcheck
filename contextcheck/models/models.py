from pathlib import Path
from typing import Annotated, Any, Self

from pydantic import AfterValidator, AnyUrl, BaseModel, ConfigDict, model_validator

from contextcheck.endpoints.endpoint import EndpointConfig
from contextcheck.loaders.yaml import load_yaml_file


class TestConfig(BaseModel):
    endpoint_under_test: EndpointConfig = EndpointConfig()

    @model_validator(mode="before")
    @classmethod
    def handle_none(cls, data: Any) -> Any:
        return data if data else {}


class MessagePrototype(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )


class TestStep(BaseModel):
    name: str
    message: str | MessagePrototype | None = None

    @classmethod
    def from_obj(cls, obj) -> Self:
        if type(obj) is str:
            return cls(name=obj)
        elif type(obj) is dict:
            return cls.model_validate(obj)
        else:
            raise ValueError("Test step in a wrong format!")

    @model_validator(mode="after")
    def set_message_if_not_provided(self) -> Self:
        if not self.message:
            self.message = self.name
        return self


class TestScenario(BaseModel):
    __test__ = False
    steps: list[TestStep] = []
    config: TestConfig

    @classmethod
    def from_yaml(cls, file_path: Path) -> Self:
        return cls.model_validate(load_yaml_file(file_path))

    @model_validator(mode="before")
    @classmethod
    def populate_steps(cls, data: Any) -> Any:
        assert "steps" in data, "No steps provided!"
        data["steps"] = [TestStep.from_obj(step) for step in data["steps"]]
        return data


class TestResult(BaseModel):
    passed: bool
