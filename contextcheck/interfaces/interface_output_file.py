import json
import os
from datetime import datetime, timezone
from pathlib import Path

import fsspec

from contextcheck.executors.executor import Executor
from contextcheck.interfaces.interface import InterfaceBase


def create_output_path(file_path: str, output_folder: str, suffix: str = "") -> Path:
    filename = os.path.basename(file_path)  # type: ignore
    filename = filename.split(".")[0] + suffix
    date_now = datetime.now(timezone.utc)
    output_path = f"{output_folder}/{filename}_{date_now.strftime('%Y-%m-%d_%H-%M-%S')}.json"

    return output_path, date_now


class InterfaceOutputFile(InterfaceBase):
    test_scenario_filename: str | None = None

    def get_scenario_path(self) -> Path:
        return Path(self.test_scenario_filename or "")

    def summary(
        self, executor: Executor, output_folder: str, global_test_timestamp: str, **kwargs
    ) -> None:
        output_path, date_now = create_output_path(
            file_path=self.test_scenario_filename, output_folder=output_folder
        )

        res = executor.test_scenario.model_dump()
        res["global_test_timestamp"] = global_test_timestamp
        res["test_timestamp"] = str(datetime.timestamp(date_now))

        if kwargs.get("aggregate_results", False):
            report = self._create_a_summary_report(executor=executor)
            res["report"] = report

        if kwargs.get("show_time_statistics", False):
            time_statistics = self._create_time_statistics(executor=executor)
            res["time_statistics"] = time_statistics

        res = json.dumps(res, indent=4)
        FileHandler(output_path).write_file(res)

    def report_results(
        self, executor: Executor, output_folder: str, global_test_timestamp: str
    ) -> None:
        output_path, date_now = create_output_path(
            file_path=self.test_scenario_filename, output_folder=output_folder, suffix="_report"
        )

        res = {}
        res["global_test_timestamp"] = global_test_timestamp
        res["test_timestamp"] = str(datetime.timestamp(date_now))

        scenario_results = self._create_a_summary_report(executor=executor)
        res["report"] = scenario_results

        res = json.dumps(res, indent=4)
        FileHandler(output_path).write_file(res)

    def report_time(
        self, executor: Executor, output_folder: str, global_test_timestamp: str
    ) -> None:
        output_path, date_now = create_output_path(
            file_path=self.test_scenario_filename,
            output_folder=output_folder,
            suffix="_time_statistics",
        )

        res = {}
        res["global_test_timestamp"] = global_test_timestamp
        res["test_timestamp"] = str(datetime.timestamp(date_now))

        scenario_results = self._create_a_summary_report(executor=executor)
        res["time_statistics"] = scenario_results

        res = json.dumps(res, indent=4)
        FileHandler(output_path).write_file(res)


class FileHandler:
    def __init__(self, file_path):
        self.file_path = file_path

    def write_file(self, content: str):
        with fsspec.open(self.file_path, "w") as f:
            f.write(content)  # type: ignore
        print(f"File written to {self.file_path}")

    def read_file(self):
        with fsspec.open(self.file_path, "r") as f:
            content = f.read()  # type: ignore
        print(f"File read from {self.file_path}")
        return content
