import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal

from loguru import logger
from pydantic import BaseModel, field_validator, model_validator

from contextcheck.executors.executor import Executor
from contextcheck.interfaces.interface import InterfaceBase
from contextcheck.interfaces.interface_output_file import InterfaceOutputFile
from contextcheck.interfaces.interface_tui import InterfaceTUI
from contextcheck.models.models import TestScenario


class TestsRouter(BaseModel):
    output_type: Literal["console", "file"]
    filename: list[Path] | None = []
    folder: Path | None = None
    output_folder: Path | None = None
    exit_on_failure: bool = False
    global_test_timestamp: str | None = None
    aggregate_results: bool = False
    show_time_statistics: bool = False

    @model_validator(mode="before")
    @classmethod
    def initialize_paths(cls, data: dict) -> dict:
        if "output_folder" in data and data["output_folder"]:
            data["output_folder"] = Path(data["output_folder"])
        if "folder" in data and data["folder"]:
            data["folder"] = Path(data["folder"])
        if "filename" in data and data["filename"]:
            data["filename"] = [Path(file) for file in data["filename"]]
        return data

    @field_validator("filename")
    @classmethod
    def check_filename(cls, value: list[Path] | None) -> list[Path]:
        if value:
            invalid_files = [file for file in value if not file.is_file()]
            if invalid_files:
                raise ValueError(
                    f'Files {", ".join(map(str, invalid_files))} do not exist. Check --filename'
                    " argument."
                )
        return value or []

    @field_validator("folder")
    @classmethod
    def check_folder(cls, value: Path | None) -> Path | None:
        if value and not value.is_dir():
            raise ValueError(f'Folder "{value}" does not exist. Check --folder argument.')
        return value

    @field_validator("output_folder")
    @classmethod
    def ensure_output_folder_exists(cls, value: Path | None) -> Path | None:
        if value and not value.exists():
            value.mkdir(parents=True)
        return value

    def model_post_init(self, __context) -> None:
        if not self.global_test_timestamp:
            now = datetime.now(timezone.utc)
            self.global_test_timestamp = str(datetime.timestamp(now))

    def run_tests(self):
        scenario_results = []
        executors: list[Executor] = []
        type_map = {"console": InterfaceTUI, "file": InterfaceOutputFile}
        interface_type = type_map[self.output_type]

        filenames = self.filename or []
        if self.folder:
            filenames.extend(self.folder.glob("*.yaml"))

        if not filenames:
            logger.warning("No test scenario to run.")
            return

        # TODO: Potential place to increase performance by running several scenarios at once
        for filename in filenames:
            executor, scenario_result, early_stop = self._run_test_scenario(
                filename, interface_type
            )
            executors.append(executor)
            scenario_results.append(scenario_result)
            if self.exit_on_failure and early_stop:
                break

        for executor in executors:
            executor.summary(
                output_folder=str(self.output_folder) if self.output_folder else None,
                global_test_timestamp=self.global_test_timestamp,
                aggregate_results=self.aggregate_results,
                show_time_statistics=self.show_time_statistics,
            )

        if self.exit_on_failure and not all(scenario_results):
            sys.exit(1)

    def _run_test_scenario(
        self, filename: Path, interface_type: InterfaceBase
    ) -> tuple[Executor, bool | None, bool]:
        ui = interface_type(test_scenario_filename=str(filename))  # type: ignore
        ts = TestScenario.from_yaml(ui.get_scenario_path())

        executor = Executor(ts, ui=ui, exit_on_failure=self.exit_on_failure)
        scenario_result = executor.run_all()

        return executor, scenario_result, executor.early_stop
