from pathlib import Path

import yaml
from jinja2 import Template


def load_yaml_file(file_path: Path, parse_template: bool = True) -> dict:
    """Load yaml file and optionally parse it before as jinja2 template."""
    if not file_path.exists():
        raise FileNotFoundError(f"File '{file_path}' does not exist.")

    with open(file_path, "r") as file:
        yaml_content = file.read()

    if parse_template:
        # Get variables from original yaml:
        try:
            yaml_dict_without_template = yaml.safe_load(yaml_content)
        except yaml.scanner.ScannerError as e:  # type: ignore
            message = (
                "Yaml parsing error. It was probably caused by your 'regex' assertion defined with"
                f" double-quotes.\nUse single quotes or no quotes to fix it.\nError details:\n\n{e}"
            )
            raise ValueError(message)

        variables = yaml_dict_without_template.get("variables", {})

        # Some variables text can be multiline, so we need to replace newlines with spaces
        variables = {
            key: value.replace("\n", " ") if isinstance(value, str) else value
            for key, value in variables.items()
        }

        # Create jinja2 template from original yaml and render it using variables
        template = Template(yaml_content)
        rendered_yaml = template.render(variables)

        # Finally, load rendered yaml
        yaml_dict = yaml.safe_load(rendered_yaml)
    else:
        yaml_dict = yaml.safe_load(yaml_content)

    return yaml_dict
