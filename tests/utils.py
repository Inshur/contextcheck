from pathlib import Path
from tempfile import NamedTemporaryFile

import pytest

from contextcheck import TestScenario
from contextcheck.executors.executor import Executor


@pytest.fixture
def executor(request):
    with NamedTemporaryFile("w", suffix=".yaml") as f:
        f.write(request.param)
        f.flush()

        ts = TestScenario.from_yaml(Path(f.name))
        return Executor(ts)
