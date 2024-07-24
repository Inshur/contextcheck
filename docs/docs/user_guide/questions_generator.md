# Synthetic Questions Generator

ContextCheck facilitates the automatic generation of YAML test scenarios by leveraging your RAG system to create questions. 

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

#### 

In order to integrate your RAG with ContextCheck questions generator, you need to implement a simple wrapper class.

The `--wrapper-class-path` flag requires a valid RAG API wrapper.

At a high level, your RAG API integration should include methods for:

* Listing all documents uploaded to the RAG,
* Loading documents individually from your system,
* Querying your semantic database endpoint directly.

For further information and detailed instructions, please refer to the provided class interface documentation in `contextcheck/generators/endpoint_wrapper.py`.

