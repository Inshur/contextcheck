from pathlib import Path
from typing import Annotated, Any, ClassVar, Self

from pydantic import AfterValidator, AnyUrl, BaseModel, ConfigDict, field_validator, model_validator

from contextcheck.endpoints.endpoint import EndpointConfig
from contextcheck.loaders.yaml import load_yaml_file


class MessagePrototype(BaseModel):
    message: str | None = None
    model_config = ConfigDict(
        extra="allow",
    )

    def __str__(self):
        return self.message

    @model_validator(mode="before")
    @classmethod
    def populate_steps(cls, obj: Any) -> Any:
        if type(obj) is str:
            return {"message": obj}
        elif type(obj) is dict:
            return obj
        else:
            raise ValueError("Message in a wrong format!")


class TestConfig(BaseModel):
    endpoint_under_test: EndpointConfig = EndpointConfig()
    default_request: MessagePrototype | None = None

    @model_validator(mode="before")
    @classmethod
    def handle_none(cls, data: Any) -> Any:
        return data if data else {}


class TestStep(BaseModel):
    name: str
    request: MessagePrototype
    default_request: ClassVar[MessagePrototype] = MessagePrototype()

    @classmethod
    def from_obj(cls, obj) -> Self:
        if type(obj) is str:
            return cls(name=obj, request=MessagePrototype(message=obj))
        elif type(obj) is dict:
            return cls.model_validate(obj)
        else:
            raise ValueError("Test step in a wrong format!")

    @field_validator("request")
    @classmethod
    def use_default_request(cls, req: MessagePrototype) -> MessagePrototype:
        req = cls.default_request.model_copy(update=req.model_dump())
        return req

    # @model_validator(mode="after")
    # def set_message_if_not_provided(self) -> Self:
    #     if not self.message:
    #         self.message = self.name
    #     return self


class TestScenario(BaseModel):
    __test__ = False
    steps: list[TestStep] = []
    config: TestConfig

    @classmethod
    def from_yaml(cls, file_path: Path) -> Self:
        cls_dict = load_yaml_file(file_path)
        config = TestConfig.model_validate(cls_dict.get("config", {}))
        if config.default_request:
            TestStep.default_request = config.default_request
        klass = cls.model_validate(cls_dict)
        return klass

    @model_validator(mode="before")
    @classmethod
    def populate_steps(cls, data: Any) -> Any:
        assert "steps" in data, "No steps provided!"
        data["steps"] = [TestStep.from_obj(step) for step in data["steps"]]
        return data


class TestResult(BaseModel):
    passed: bool
