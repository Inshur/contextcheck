import re
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, model_validator

from contextcheck.assertions.llm_metrics import (
    LlmMetricEnum,
    LLMMetricEvaluator,
    llm_metric_factory,
)
from contextcheck.assertions.utils import JsonValidator
from contextcheck.endpoints.endpoint import EndpointBase
from contextcheck.models.request import RequestBase
from contextcheck.models.response import ResponseBase


class AssertionBase(BaseModel):
    model_config = ConfigDict(extra="allow")
    result: bool | None = Field(default=None, description="Result of a assertion")

    @model_validator(mode="before")
    @classmethod
    def from_obj(cls, obj: dict | str) -> dict:
        # Default assertion without keyword:
        return obj if isinstance(obj, dict) else {"eval": obj}

    def __call__(
        self, request: RequestBase, response: ResponseBase, eval_endpoint: EndpointBase
    ) -> bool:
        raise NotImplementedError


class AssertionEval(AssertionBase):
    eval: str = Field(description="Eval string to be used for python's eval")

    def __call__(
        self, request: RequestBase, response: ResponseBase, eval_endpoint: EndpointBase
    ) -> bool:
        if self.result is None:
            try:
                # NOTE: I suppose running eval has some major security risks attached
                # Pass 'response' via 'globals' to ensure it's accessible in all scopes
                # within eval()
                result = eval(self.eval, {"response": response}, {})
            except NameError:
                raise NameError(f"Given eval `{self.eval}` uses non-existent name.")
            if not isinstance(result, bool):
                raise ValueError(f"Given eval `{self.eval}` does not evaluate to bool.")
            self.result = result
        return self.result


class AssertionLLM(AssertionBase):
    llm_metric: LlmMetricEnum
    reference: str = Field(default="", description="Reference given to llm")
    assertion: str = Field(
        default="", description="Assertion given to llm to compare against the obtained results"
    )

    def __call__(
        self, request: RequestBase, response: ResponseBase, eval_endpoint: EndpointBase
    ) -> bool:
        if self.result is None:
            # This is required as otherwise time statistics will be shared across assertions
            # for a given TestScenario
            eval_endpoint = eval_endpoint.model_copy(deep=True)
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


class DeterministicMetricsEnum(StrEnum):
    CONTAINS = "contains"
    ICONTAINS = "icontains"
    CONTAINS_ALL = "contains-all"
    ICONTAINS_ALL = "icontains-all"
    CONTAINS_ANY = "contains-any"
    ICONTAINS_ANY = "icontains-any"
    IS_VALID_JSON = "is-valid-json"
    HAS_VALID_JSON_SCHEMA = "has-valid-json-schema"
    EQUALS = "equals"
    REGEX = "regex"


DETERMINISTIC_METRICS_MAPPING = {
    DeterministicMetricsEnum.CONTAINS: lambda assertion, response: assertion in response,
    DeterministicMetricsEnum.ICONTAINS: (
        lambda assertion, response: assertion.lower() in response.lower()
    ),
    DeterministicMetricsEnum.CONTAINS_ALL: lambda assertion, response: all(
        [assertion in response for assertion in assertion]
    ),
    DeterministicMetricsEnum.ICONTAINS_ALL: lambda assertion, response: all(
        [assertion.lower() in response.lower() for assertion in assertion]
    ),
    DeterministicMetricsEnum.CONTAINS_ANY: lambda assertion, response: any(
        [assertion in response for assertion in assertion]
    ),
    DeterministicMetricsEnum.ICONTAINS_ANY: lambda assertion, response: any(
        [assertion.lower() in response.lower() for assertion in assertion]
    ),
    DeterministicMetricsEnum.IS_VALID_JSON: lambda assertion, response: JsonValidator(
        request_json=response
    ).is_valid(),
    DeterministicMetricsEnum.HAS_VALID_JSON_SCHEMA: lambda assertion, response: JsonValidator(
        request_json=response, assertion_schema=assertion
    ).has_valid_schema(),
    DeterministicMetricsEnum.EQUALS: lambda assertion, response: assertion == response,
    DeterministicMetricsEnum.REGEX: lambda assertion, response: bool(re.match(assertion, response)),
}


class AssertionDeterministic(AssertionBase):
    kind: DeterministicMetricsEnum = Field(description="A type of deterministic evaluation")
    assertion: str | list[str] | dict | None = Field(
        default=None, description="Assertion to be evaluated"
    )

    def __call__(
        self, request: RequestBase, response: ResponseBase, eval_endpoint=EndpointBase
    ) -> bool:
        if self.result is None:
            if self.kind in DETERMINISTIC_METRICS_MAPPING:
                self.result = DETERMINISTIC_METRICS_MAPPING[self.kind](
                    self.assertion, response.message
                )
            else:
                raise ValueError(f"Given kind `{self.kind}` is not a deterministic metric.")

        return self.result  # type: ignore
