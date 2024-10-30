from enum import StrEnum


class AssertionKind(StrEnum):
    EVAL = "eval"
    LLM_METRIC = "llm_metric"
    DETERMINISTIC = "kind"
