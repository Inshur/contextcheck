![image](./docs/contextchecklogo.png)

# ContextCheck 

A human-friendly framework for testing and evaluating LLMs, RAGs, and chatbots.

**ContextCheck** is an open-source framework designed to evaluate, test, and validate large language models (LLMs), Retrieval-Augmented Generation (RAG) systems, and chatbots. It provides tools to automatically generate queries, request completions, detect regressions, perform penetration tests, and assess hallucinations, ensuring the robustness and reliability of these systems. ContextCheck is configurable via YAML and can be integrated into continuous integration (CI) pipelines for automated testing.

## Features

- **Simple test scenario definition** using human-readable `.yaml` files
- **Flexible endpoint configuration** for OpenAI, HTTP, and more
- **Customizable JSON request/response models**
- **Support for variables and Jinja2 templating** in YAML files
- **Response validation** options, including heuristics, LLM-based judgment, and human labeling
- **Enhanced output formatting** with the `rich` package for clear, readable displays


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 


### Installing

🚧 TODO: installation using pypi repo

1. **Setup and initialize Poetry.**

2. **Activate the `ccheck` CLI command** using:
   ```sh
   poetry run ccheck
   ```

3. **Discover available options** by running:
   ```sh
   ccheck --help
   ```

### Tutorial

Please refer to `examples/` folder for the tutorial.

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


#### Running in CI/CD

To automatically stop the CI/CD process if any tests fail, add the `--exit-on-failure` flag. Failed test will cause the script to exit with code 1.

- **Example:**
  ```sh
  ccheck --exit-on-failure --output-type console --folder my_tests
  ```



Use env variable `OPENAI_API_KEY` to be able to run:
- `tests/scenario_openai.yaml`
- `tests/scenario_defaults.yaml`


## Made with ❤️ by the Addepto Team

ContextCheck is an extension of the [ContextClue](https://context-clue.com/) product, created by the [Addepto](https://addepto.com/) team. This project is the result of our team’s dedication, combining innovation and expertise.

Addepto Team:

* Radoslaw Bodus
* Bartlomiej Grasza
* Volodymyr Kepsha
* Vadym Mariiechko
* Michal Tarkowski

Like what we’re building? ⭐ Give it a star to support its development!

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details



## Contributing, tests and development

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


