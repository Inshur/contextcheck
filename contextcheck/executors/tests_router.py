from pydantic import BaseModel, model_validator, field_validator
import os
import sys
from typing import Literal
from datetime import datetime, timezone

from contextcheck.executors.executor import Executor
from contextcheck.interfaces.interface_tui import InterfaceTUI
from contextcheck.interfaces.interface_output_file import InterfaceOutputFile
from contextcheck.interfaces.interface import InterfaceBase
from contextcheck.models.models import TestScenario


class TestsRouter(BaseModel):
    output_type: Literal["console", "file"]
    filename: list[str] | None = []
    folder: str | None = None
    output_folder: str | None = None
    exit_on_failure: bool = False
    global_test_timestamp: str | None = None

    @field_validator("filename")
    @classmethod
    def check_filename(cls, value: list[str]) -> list[str]:
        if value:
            invalid_files = [file for file in value if not os.path.isfile(file)]
            if invalid_files:
                raise ValueError(
                    f'Files {", ".join(invalid_files)} do not exist. Check --filename argument.'
                )
        return value

    @field_validator("folder")
    @classmethod
    def check_folder(cls, value: str) -> str:
        if value and not os.path.isdir(value):
            raise ValueError(f'Folder "{value}" does not exist. Check --folder argument.')
        return value

    @model_validator(mode="before")
    @classmethod
    def check_files_and_folders(cls, data: dict) -> dict:
        if data["output_type"] == "file":
            if not os.path.isdir(data["output_folder"]):
                os.makedirs(data["output_folder"])
        return data

    def model_post_init(self, __context) -> None:
        if not self.global_test_timestamp:
            now = datetime.now(timezone.utc)
            self.global_test_timestamp = str(datetime.timestamp(now))

    def _run_test_scenario(self, filename: str, interface_type: InterfaceBase) -> bool | None:
        ui = interface_type(test_scenario_filename=filename)  # type: ignore
        ts = TestScenario.from_yaml(ui.get_scenario_path())

        executor = Executor(ts, ui=ui, exit_on_failure=self.exit_on_failure)
        scenario_result = executor.run_all()
        executor.summary(
            output_folder=self.output_folder, global_test_timestamp=self.global_test_timestamp
        )

        return scenario_result, executor.early_stop

    def run_tests(self):
        scenario_results = []
        type_map = {"console": InterfaceTUI, "file": InterfaceOutputFile}
        interface_type = type_map[self.output_type]

        filenames = []
        if self.filename:
            for filename in self.filename:
                filenames.append(filename)
        elif self.folder:
            for filename in os.listdir(self.folder):
                if filename.endswith(".yaml"):
                    filenames.append(filename)

        for filename in filenames:
            scenario_result, early_stop = self._run_test_scenario(filename, interface_type)
            scenario_results.append(scenario_result)
            if self.exit_on_failure and early_stop:
                break

        if self.exit_on_failure and not all(scenario_results):
            sys.exit(1)
