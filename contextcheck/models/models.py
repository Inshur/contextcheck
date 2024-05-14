from pathlib import Path
from typing import Annotated, Any, Self

from pydantic import AfterValidator, AnyUrl, BaseModel, model_validator

from contextcheck.loaders.yaml import load_yaml_file


class TestConfig(BaseModel):
    endpoint_url: Annotated[AnyUrl, AfterValidator(str)]
    additional_headers: dict | None = {}
    request_format: str | None = None


class TestStep(BaseModel):
    name: str
    message: str | None = None

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
