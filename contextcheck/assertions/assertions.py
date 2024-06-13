from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, model_validator

from contextcheck.assertions.metrics import LLMMetricEvaluator, llm_metric_factory
from contextcheck.endpoints.factory import factory as endpoint_factory

if TYPE_CHECKING:
    from contextcheck.models.models import TestConfig, TestStep


class AssertionBase(BaseModel):
    model_config = ConfigDict(extra="allow")
    result: bool | None = None

    @model_validator(mode="before")
    @classmethod
    def from_obj(cls, obj: dict | str) -> dict:
        # Default assertion without keyword:
        return obj if isinstance(obj, dict) else {"eval": obj}

    def __call__(self, test_step: "TestStep", test_config: "TestConfig" = None) -> bool:  # type: ignore
        raise NotImplementedError


class AssertionEval(AssertionBase):
    eval: str

    def __call__(self, test_step: "TestStep", test_config: "TestConfig") -> bool:
        response = test_step.response
        if self.result is None:
            try:
                result = eval(self.eval)
            except NameError:
                raise NameError(f"Given eval `{self.eval}` uses non-existent name.")
            if not isinstance(result, bool):
                raise ValueError(f"Given eval `{self.eval}` does not evaluate to bool.")
            self.result = result
        return self.result


class LLMAssertion(AssertionBase):
    llm_metric: str
    reference: str = ""
    assertion: str = ""

    def __call__(self, test_step: "TestStep", test_config: "TestConfig") -> bool:
        if self.result is None:
            eval_endpoint = endpoint_factory(test_config.eval_endpoint)  # type: ignore
            metric = llm_metric_factory(metric_type=self.llm_metric)

            self.metric_evaluator = LLMMetricEvaluator(
                eval_endpoint=eval_endpoint, metric=metric
            )

            self.result = self.metric_evaluator.evaluate(
                input=test_step.request.message,  # type: ignore
                output=test_step.response.message,  # type: ignore
                **self.model_dump(exclude={"llm_metric", "result"})
            )

        return self.result
