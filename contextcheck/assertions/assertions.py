from pydantic import BaseModel, ConfigDict, model_validator

from contextcheck.assertions.metrics import LLMMetricEvaluator, llm_metric_factory
from contextcheck.endpoints.endpoint import EndpointBase
from contextcheck.models.request import RequestBase
from contextcheck.models.response import ResponseBase



class AssertionBase(BaseModel):
    model_config = ConfigDict(extra="allow")
    result: bool | None = None

    @model_validator(mode="before")
    @classmethod
    def from_obj(cls, obj: dict | str) -> dict:
        # Default assertion without keyword:
        return obj if isinstance(obj, dict) else {"eval": obj}
    
    def update_config(self, *args, **kwargs):
        raise NotImplementedError

    def __call__(self, request: RequestBase, response: ResponseBase, *args, **kwargs) -> bool:
        raise NotImplementedError


class AssertionEval(AssertionBase):
    eval: str

    def __call__(self, request: RequestBase, response: ResponseBase, *args, **kwargs) -> bool:
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

    def __call__(self, request: RequestBase, response: ResponseBase, *args, **kwargs) -> bool:
        try:
            eval_endpoint = kwargs["eval_endpoint"]
        except KeyError:
            raise KeyError("LLM-based assertions require 'eval_endpoint' defined in the test scenario.")

        if self.result is None:
            metric = llm_metric_factory(metric_type=self.llm_metric)

            self.metric_evaluator = LLMMetricEvaluator(
                eval_endpoint=eval_endpoint, metric=metric # type: ignore
            )

            self.result = self.metric_evaluator.evaluate(
                input=request.message, # type: ignore
                output=response.message, # type: ignore
                **self.model_dump(exclude={"llm_metric", "result"})
            )

        return self.result
