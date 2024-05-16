import time

from openai import BaseModel


class ConnectorStats(BaseModel):
    duration_context: float | None = None


class ConnectorBase(BaseModel):
    _stats: ConnectorStats = ConnectorStats()

    def __enter__(self):
        self._stats.duration_context = time.perf_counter()
        return self

    def __exit__(self, type, value, traceback):
        self._stats.duration_context = (
            time.perf_counter() - self._stats.duration_context
        )
