import jsonschema
import json
import jsonschema.exceptions
from pydantic import BaseModel

class JsonValidator(BaseModel):
    request_json: str
    assertion_schema: dict | None = None

    def is_valid(self):
        try:
            json.loads(self.request_json)
            return True
        except json.JSONDecodeError:
            return False
        
    def has_valid_schema(self):
        self.is_valid()

        if self.assertion_schema is None:
            raise ValueError("Assertion schema is not provided.")
        
        try:
            jsonschema.validate(json.loads(self.request_json), schema=self.assertion_schema)
            return True
        except (jsonschema.exceptions.ValidationError, jsonschema.exceptions.SchemaError) as e:
            return False