import re
from pydantic import BaseModel, ConfigDict, model_validator

from contextcheck.assertions.llm_metrics import LLMMetricEvaluator, llm_metric_factory
from contextcheck.endpoints.endpoint import EndpointBase
from contextcheck.models.request import RequestBase
from contextcheck.models.response import ResponseBase
from contextcheck.assertions.utils import JsonValidator


class AssertionBase(BaseModel):
    model_config = ConfigDict(extra="allow")
    result: bool | None = None

    @model_validator(mode="before")
    @classmethod
    def from_obj(cls, obj: dict | str) -> dict:
        # Default assertion without keyword:
        return obj if isinstance(obj, dict) else {"eval": obj}

    def __call__(
        self, request: RequestBase, response: ResponseBase, eval_endpoint=EndpointBase
    ) -> bool:
        raise NotImplementedError


class AssertionEval(AssertionBase):
    eval: str

    def __call__(
        self, request: RequestBase, response: ResponseBase, eval_endpoint=EndpointBase
    ) -> bool:
        if self.result is None:
            try:
                result = eval(self.eval)
            except NameError:
                raise NameError(f"Given eval `{self.eval}` uses non-existent name.")
            if not isinstance(result, bool):
                raise ValueError(f"Given eval `{self.eval}` does not evaluate to bool.")
            self.result = result
        return self.result


class AssertionLLM(AssertionBase):
    llm_metric: str
    reference: str = ""
    assertion: str = ""

    def __call__(
        self, request: RequestBase, response: ResponseBase, eval_endpoint=EndpointBase
    ) -> bool:
        if self.result is None:
            metric = llm_metric_factory(metric_type=self.llm_metric)

            self.metric_evaluator = LLMMetricEvaluator(
                eval_endpoint=eval_endpoint, metric=metric  # type: ignore
            )

            self.result = self.metric_evaluator.evaluate(
                input=request.message,  # type: ignore
                output=response.message,  # type: ignore
                **self.model_dump(exclude={"llm_metric", "result"}),
            )

        return self.result


deterministic_metrics = {
    "contains": lambda assertion, response: assertion in response,
    "icontains": lambda assertion, response: assertion.lower() in response.lower(),
    "contains-all": lambda assertion, response: all(
        [assertion in response for assertion in assertion]
    ),
    "icontains-all": lambda assertion, response: all(
        [assertion.lower() in response.lower() for assertion in assertion]
    ),
    "contains-any": lambda assertion, response: any(
        [assertion in response for assertion in assertion]
    ),
    "icontains-any": lambda assertion, response: any(
        [assertion.lower() in response.lower() for assertion in assertion]
    ),
    "is-valid-json": lambda assertion, response: JsonValidator(request_json=response).is_valid(),
    "has-valid-json-schema": lambda assertion, response: JsonValidator(
        request_json=response, assertion_schema=assertion
    ).has_valid_schema(),
    "equals": lambda assertion, response: assertion == response,
    "regex": lambda assertion, response: bool(re.match(assertion, response)),
}


class AssertionDeterministic(AssertionBase):
    type: str
    assertion: str | list[str] | dict | None = None

    def __call__(
        self, request: RequestBase, response: ResponseBase, eval_endpoint=EndpointBase
    ) -> bool:
        if self.result is None:

            if self.type in deterministic_metrics:
                self.result = deterministic_metrics[self.type](self.assertion, response.message)
            else:
                raise ValueError(f"Given type `{self.type}` is not a deterministic metric.")

        return self.result  # type: ignore
