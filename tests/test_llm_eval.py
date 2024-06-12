from pathlib import Path

from contextcheck import TestScenario
from contextcheck.executors.executor import Executor


def test_evals():
    ts = TestScenario.from_yaml(Path("tests/scenario_llm_eval.yaml"))
    executor = Executor(ts)
    executor.run_all()
    test_steps = executor.test_scenario.steps

    # Test hallucination evaluator (hallucinated)
    assert test_steps[0].asserts[0].result == False

    # Test QA reference evaluator
    assert test_steps[1].asserts[0].result == True

    # Test QA reference evaluator (invalid answer)
    assert test_steps[2].asserts[0].result == False

    # Test Model grading QA evaluator
    assert test_steps[3].asserts[0].result == True

    # Test Model grading QA evaluator (invalid answer)
    assert test_steps[4].asserts[0].result == False 

    # Test Summarization evaluator
    assert test_steps[5].asserts[0].result == True

    # Test Human vs AI evaluator
    assert test_steps[6].asserts[0].result == True

    # Test Human vs AI evaluator (wrong reference)
    assert test_steps[7].asserts[0].result == False
