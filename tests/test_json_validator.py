from contextcheck.assertions.utils import JsonValidator


def test_json_validator():
    request_json = '{"name": "John", "age": 30, "city": "New York"}'
    assertion_schema = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "age": {"type": "number", "minimum": 0, "maximum": 150},
        },
        "required": ["name", "age"],
    }

    json_validator = JsonValidator(request_json=request_json, assertion_schema=assertion_schema)
    assert json_validator.is_valid() == True
    assert json_validator.has_valid_schema() == True

    invalid_request_json_1 = (
        'Here is your response in a json format:\n{"name": "John", "age": 30, "city": "New York"}'
    )
    json_validator = JsonValidator(
        request_json=invalid_request_json_1, assertion_schema=assertion_schema
    )
    assert json_validator.is_valid() == False

    invalid_request_json_2 = '{"name": "John", "age": -30, "city": "New York"}'
    json_validator = JsonValidator(
        request_json=invalid_request_json_2, assertion_schema=assertion_schema
    )
    assert json_validator.is_valid() == True
    assert json_validator.has_valid_schema() == False

    invalid_request_json_3 = '{"name": "John"}'
    json_validator = JsonValidator(
        request_json=invalid_request_json_3, assertion_schema=assertion_schema
    )
    assert json_validator.is_valid() == True
    assert json_validator.has_valid_schema() == False
