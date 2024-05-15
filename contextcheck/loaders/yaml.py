from pathlib import Path

import yaml
from jinja2 import Template


def load_yaml_file(file_path: Path) -> dict:
    if not file_path.exists():
        raise FileNotFoundError(f"File '{file_path}' does not exist.")

    print(file_path)

    with open(file_path, "r") as file:
        yaml_content = file.read()

    # Get variables from original yaml:
    yaml_dict_without_template = yaml.safe_load(yaml_content)
    variables = yaml_dict_without_template.get("variables", {})

    # Create jinja2 template from original yaml and render it using variables
    template = Template(yaml_content)
    rendered_yaml = template.render(variables)

    # Finally, load rendered yaml
    yaml_dict = yaml.safe_load(rendered_yaml)

    return yaml_dict
