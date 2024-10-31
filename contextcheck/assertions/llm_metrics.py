from enum import StrEnum

from pydantic import BaseModel

from contextcheck.assertions.llm_eval_prompts import (
    HALLUCINATION_PROMPT_TEMPLATE,
    HUMAN_VS_AI_PROMPT_TEMPLATE,
    MODEL_GRADING_QA_PROMPT_TEMPLATE,
    QA_REFERENCE_PROMPT_TEMPLATE,
    SUMMARIZATION_PROMPT_TEMPLATE,
)
from contextcheck.endpoints.endpoint import EndpointBase
from contextcheck.models.request import RequestBase
from contextcheck.models.response import ResponseBase


class LlmMetricEnum(StrEnum):
    HALLUCINATION = "hallucination"
    QA_REFERENCE = "qa-reference"
    MODEL_GRADING_QA = "model-grading-qa"
    SUMMARIZATION = "summarization"
    HUMAN_VS_AI = "human-vs-ai"


class LLMMetric(BaseModel):
    prompt_template: str
    rails: dict = {}

    def parse_prompt(self, input: str, output: str, **kwargs) -> str:
        return self.prompt_template.format(
            input=input, output=output, reference=kwargs["reference"]
        )

    def check_response_rails(self, response: ResponseBase) -> bool:
        if response.message.lower() not in self.rails:  # type: ignore
            raise ValueError(
                f"Response message '{response.message}' should be one of : {list(self.rails.keys())}"
            )

        return self.rails[response.message.lower()]  # type: ignore


class MetricHallucination(LLMMetric):
    prompt_template: str = HALLUCINATION_PROMPT_TEMPLATE
    rails: dict = {"factual": True, "hallucinated": False}


class MetricQAReference(LLMMetric):
    prompt_template: str = QA_REFERENCE_PROMPT_TEMPLATE
    rails: dict = {"correct": True, "incorrect": False}


class MetricModelGradingQA(LLMMetric):
    prompt_template: str = MODEL_GRADING_QA_PROMPT_TEMPLATE
    rails: dict = {"correct": True, "incorrect": False}

    def parse_prompt(self, input: str, output: str, **kwargs) -> str:
        return self.prompt_template.format(output=output, assertion=kwargs["assertion"])


class MetricSummarization(LLMMetric):
    prompt_template: str = SUMMARIZATION_PROMPT_TEMPLATE
    rails: dict = {"good": True, "bad": False}

    def parse_prompt(self, input: str, output: str, **kwargs) -> str:
        return self.prompt_template.format(input=input, output=output)


class MetricHumanVsAI(LLMMetric):
    prompt_template: str = HUMAN_VS_AI_PROMPT_TEMPLATE
    rails: dict = {"correct": True, "incorrect": False}


LLM_METRIC_TYPE_MAPPING = {
    LlmMetricEnum.HALLUCINATION: MetricHallucination,
    LlmMetricEnum.QA_REFERENCE: MetricQAReference,
    LlmMetricEnum.MODEL_GRADING_QA: MetricModelGradingQA,
    LlmMetricEnum.SUMMARIZATION: MetricSummarization,
    LlmMetricEnum.HUMAN_VS_AI: MetricHumanVsAI,
}


def llm_metric_factory(metric_type: LlmMetricEnum) -> LLMMetric:
    try:
        metric_class = LLM_METRIC_TYPE_MAPPING[metric_type]
    except KeyError:
        raise ValueError(f"No metric found for type '{metric_type}'")

    return metric_class()


class LLMMetricEvaluator(BaseModel):
    eval_endpoint: EndpointBase
    metric: LLMMetric

    class EvalRequest(RequestBase):
        message: str = ""

    def evaluate(self, input: str, output: str, **kwargs) -> bool:
        message = self.metric.parse_prompt(input=input, output=output, **kwargs)
        response = self.eval_endpoint.send_request(self.EvalRequest(message=message))
        return self.metric.check_response_rails(response)
