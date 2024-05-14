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

    @model_validator(mode="after")
    def set_message_if_not_provided(self) -> Self:
        if not self.message:
            self.message = self.name
        return self


class TestScenario(BaseModel):
    steps: list[TestStep] = []
    config: TestConfig

    @classmethod
    def from_yaml(cls, file_path: Path) -> Self:
        return cls.model_validate(load_yaml_file(file_path))

    @model_validator(mode="before")
    @classmethod
    def populate_steps(cls, data: Any) -> Any:
        assert "steps" in data, "No steps provided!"
        steps = []
        for step_obj in data["steps"]:
            if type(step_obj) is str:
                step = TestStep(name=step_obj)
            elif type(step_obj) is dict:
                step = TestStep.model_validate(step_obj)
            else:
                raise ValueError("Test step in a wrong format!")
            steps.append(step)

        data["steps"] = steps
        return data
