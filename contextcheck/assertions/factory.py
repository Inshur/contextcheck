from contextcheck.assertions.assertions import (
    AssertionBase,
    AssertionDeterministic,
    AssertionEval,
    AssertionLLM,
)
from contextcheck.assertions.settings import AssertionKind

assertions_map = {
    AssertionKind.EVAL: AssertionEval,
    AssertionKind.LLM_METRIC: AssertionLLM,
    AssertionKind.DETERMINISTIC: AssertionDeterministic,
}


def factory(assert_definition: dict) -> AssertionBase:
    # Take first key from assertions_map present in assert_deffinition
    try:
        kind = next(
            assert_key for assert_key in assert_definition.keys() if assert_key in assertions_map
        )
    except StopIteration:
        raise ValueError(f"No assertion for definition {assert_definition}")

    assertion_class = assertions_map[kind]
    return assertion_class.model_validate(assert_definition)
