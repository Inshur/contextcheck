import json

import jsonschema
import jsonschema.exceptions
from loguru import logger
from pydantic import BaseModel


class JsonValidator(BaseModel):
    request_json: str
    assertion_schema: dict | None = None

    def is_valid(self):
        try:
            json.loads(self.request_json)
            return True
        except json.JSONDecodeError as e:
            logger.error(f"Error message: {e}")
            return False

    def has_valid_schema(self):
        if not self.is_valid():
            return False

        if self.assertion_schema is None:
            raise ValueError("Assertion schema is not provided.")

        try:
            jsonschema.validate(json.loads(self.request_json), schema=self.assertion_schema)
            return True
        except (jsonschema.exceptions.ValidationError, jsonschema.exceptions.SchemaError) as e:
            logger.error(f"Error message: {e}")
            return False
