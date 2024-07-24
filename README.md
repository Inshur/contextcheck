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

## Getting Started

1. **Setup and initialize Poetry.**

2. **Activate the `ccheck` CLI command** using:
   ```sh
   poetry run ccheck
   ```

3. **Discover available options** by running:
   ```sh
   ccheck --help
   ```

### The `ccheck` Command Features

#### Output Test Results to Console

- **Run a single scenario and output results to the console:**
  ```sh
  ccheck --output-type console --filename path/to/file.yaml
  ```
- **Run multiple scenarios and output results to the console:**
  ```sh
  ccheck --output-type console --filename path/to/file.yaml path/to/another_file.yaml
  ```
- **Run all scenarios from a folder and output results to the console:**
  ```sh
  ccheck --output-type console --folder my_tests
  ```

#### Output Test Results to JSON Files

The `--output-type file` option works similarly to `--output-type console`. It requires either `--filename` or `--folder`, and also an `--output-folder` where the test results will be saved. Each test scenario will be saved as a separate JSON file with the current date and time included in the filename.

- **Example:**
  ```sh
  ccheck --output-type file --folder my_tests --output-folder test_results
  ```

#### Running in CI/CD

To automatically stop the CI/CD process if any tests fail, add the `--exit-on-failure` flag. Failed test will cause the script to exit with code 1.

- **Example:**
  ```sh
  ccheck --exit-on-failure --output-type console --folder my_tests
  ```



Use env variable `OPENAI_API_KEY` to be able to run:
- `tests/scenario_openai.yaml`
- `tests/scenario_defaults.yaml`

## Tests

Only end-to-end tests are currently available.

To run tests:
```
poetry run pytest tests/
```

To include tests which require calling LLM APIs (currently OpenAI and Ollama), run one of: 
```
poetry run pytest --openai          # includes tests that use OpenAI API
poetry run pytest --ollama          # includes tests that use Ollama API
poetry run pytest --openai --ollama # includes tests that use both OpenAI and Ollama API
```

### Synthetic Questions Generator

ContextCheck facilitates the automatic generation of YAML test scenarios by leveraging your RAG (Retrieval-Augmented Generation) system to create questions. 

To use this feature, first integrate ContextCheck with your RAG (details below), then run the CLI command to generate the questions and save them to an output file.

The generator will, by default, create 10 unique topics for each document in your RAG. For each topic, it will, by default, generate 3 questions. 
These questions will be written to an output file in the following format:

```yaml
questions:
- document: MyFirstDocument.pdf
  questions:
  - <Question 1>
  - <Question 2>
  - <Question N>
- document: MySecondDocument.pdf
  questions:
  - <Question 1>
  - <Question 2>
  - <Question N>
```

To use the questions generator, run the CLI command `questions_generator`. 
For detailed information on the required parameters, please refer to the command's documentation.

If the CLI command is not available, you can execute the following command:

```sh
poetry run questions_generator
```

#### RAG wrapper class

The `--wrapper-class-path` flag requires a valid RAG API wrapper, and at
At a high level, your RAG API integration should include methods for:

* Listing all documents uploaded to the RAG,
* Loading documents individually from your system,
* Querying your semantic database endpoint directly.

For further information and detailed instructions, please refer to the provided class interface documentation in `contextcheck/generators/endpoint_wrapper.py`.



