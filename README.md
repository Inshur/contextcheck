# ContextCheck

Framework for LLM/RAG testing.

## Features

⚠️ Under development

- Test scenario definition by .yaml files
- Endpoint configuration (openai, http)
- JSON request/response 
- Variables and Jinja2 templating for yaml files
- Response validation using `eval` 
- Dynamic fields using `eval` - including passing fields from last response
- Pretty printing using `rich` package

## Getting started

For now, this is just:
```
poetry run python main_tui.py tests/scenario_echo.yaml
```

Use env variable `OPENAI_API_KEY` to be able to run:
- `tests/scenario_openai.yaml`
- `tests/scenario_defaults.yaml`

## Tests

Only end-to-end tests are currently available. Feel free to add some.

To run tests:
```
poetry run pytest tests/
```