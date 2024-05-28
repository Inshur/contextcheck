import time

from pydantic import BaseModel


class ConnectorStats(BaseModel):
    conn_start_time: float | None = None
    conn_end_time: float | None = None
    conn_duration: float | None = None


class ConnectorBase(BaseModel):
    stats: ConnectorStats = ConnectorStats()

    def __enter__(self):
        self.stats.conn_start_time = time.perf_counter()
        return self

    def __exit__(self, type, value, traceback):
        self.stats.conn_end_time = time.perf_counter()
        self.stats.conn_duration = self.stats.conn_end_time - self.stats.conn_start_time

    def send(self, args, **kwargs):
        raise NotImplementedError
