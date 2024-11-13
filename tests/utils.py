from pathlib import Path

import pytest

from contextcheck import TestScenario
from contextcheck.executors.executor import Executor


@pytest.fixture
def executor(request, tmp_path: Path):
    temp_file = tmp_path / "test.yaml"
    temp_file.write_text(request.param)

    ts = TestScenario.from_yaml(temp_file)
    return Executor(ts)
