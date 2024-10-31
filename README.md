# ✅ ContextCheck 

Human-friendly framework to test and evaluate LLMs, RAGs and ChatBots.

## Features

- Simple test scenario definition by readable .yaml files
- Flexible endpoint-under-test configuration (openai, http)
- Flexible JSON request/response models
- Variables and Jinja2 templating for yaml files
- Response validation using heuristics, LLM as judge, human labeling...
- Pretty printing using `rich` package

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

What things you need to install the software and how to install them

```
Give examples
```

### Installing

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


## Built With

* pydantic

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.


## Authors

Addepto Team:

* Radoslaw Bodus
* Bartlomiej Grasza
* Volodymyr Kepsha
* Vadym Mariiechko
* Michal Tarkowski

* **XYZ** - *Initial work* 

See also the list of [contributors](https://github.com/contextcheck/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc





## Tests and development

Contributions are welcomed!

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


