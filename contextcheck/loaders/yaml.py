from pathlib import Path

import yaml


def load_yaml_file(file_path: Path) -> dict:
    if not file_path.exists():
        raise FileNotFoundError(f"File '{file_path}' does not exist.")

    with open(file_path, "r") as file:
        yaml_dict = yaml.safe_load(file)
    return yaml_dict
