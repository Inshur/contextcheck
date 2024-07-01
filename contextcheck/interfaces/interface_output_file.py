import json
import os
from pathlib import Path
from datetime import datetime, timezone
import fsspec

from contextcheck.interfaces.interface import InterfaceBase
from contextcheck.executors.executor import Executor


class InterfaceOutputFile(InterfaceBase):
    test_scenario_filename: str | None = None

    def get_scenario_path(self) -> Path:
        return Path(self.test_scenario_filename or "")
    
    def summary(self, executor: Executor, output_folder: str, global_test_timestamp: str) -> None:
        filename = os.path.basename(self.test_scenario_filename) # type: ignore
        filename = filename.split(".")[0]
        date_now = datetime.now(timezone.utc)
        output_path = f"{output_folder}/{filename}_{date_now.strftime('%Y-%m-%d_%H-%M-%S')}.json"

        res = executor.test_scenario.model_dump()
        res['global_test_timestamp'] = global_test_timestamp
        res['test_timestamp'] = str(datetime.timestamp(date_now))
        res = json.dumps(res, indent=4)
        FileHandler(output_path).write_file(res)


class FileHandler:
    def __init__(self, file_path):
        self.file_path = file_path

    def write_file(self, content: str):
        with fsspec.open(self.file_path, 'w') as f:
            f.write(content) # type: ignore
        print(f"File written to {self.file_path}")

    def read_file(self):
        with fsspec.open(self.file_path, 'r') as f:
            content = f.read() # type: ignore
        print(f"File read from {self.file_path}")
        return content