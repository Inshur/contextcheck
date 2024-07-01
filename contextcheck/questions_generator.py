from argparse import ArgumentParser
from importlib import import_module
import sys

from contextcheck.endpoints.endpoint_config import EndpointConfig
from contextcheck.generators.generate_questions import QuestionsGenerator


def import_class_from_string(path):
    module_path, class_name = path.rsplit(".", 1)
    module = import_module(module_path)
    clazz = getattr(module, class_name)
    return clazz


def generate_questions(
    output_file: str,
    wrapper_class_path: str,
    num_topics: int,
    questions_per_topic: int,
    llm_model_provider: str,
    llm_model: str,
) -> None:
    api_wrapper = import_class_from_string(wrapper_class_path)

    endpoint_config = EndpointConfig(
        kind="openai_compatible", provider=llm_model_provider, model=llm_model
    )

    generator_args = {
        "api_wrapper": api_wrapper(),
        "questions_generator_endpoint_config": endpoint_config,
    }

    if num_topics:
        generator_args["num_topics"] = num_topics
    if questions_per_topic:
        generator_args["questions_per_topic"] = questions_per_topic

    generator = QuestionsGenerator.model_validate(generator_args)
    generator.save_to_yaml(output_file)


def main():
    parser = ArgumentParser(
        prog="questions_generator.py", description="Refer to readme for more information."
    )
    parser.add_argument(
        "--output-file",
        type=str,
        required=True,
        help="Output path and filename to save the generated questions. "
        "Example: 'my_folder/my_file.yaml'. If folder does not exist, it will be created.",
    )
    parser.add_argument(
        "--wrapper-class-path",
        type=str,
        required=True,
        help="Full path to the API wrapper class definition. "
        "Example: For a class 'ClassName' defined in file 'module/submodule.py' use format 'module.submodule.ClassName'.",
    )
    parser.add_argument(
        "--num-topics",
        type=int,
        default=10,
        help="Number of topics generated for each file. Default is 10",
    )
    parser.add_argument(
        "--questions-per-topic",
        type=int,
        default=3,
        help="Number of questions generater per each topic. Default is 3.",
    )
    parser.add_argument(
        "--llm-model-provider",
        type=str,
        default="ChatOpenAI",
        help="LLM model provider. Default one is OpenAI.",
    )
    parser.add_argument(
        "--llm-model",
        type=str,
        default="gpt-3.5-turbo",
        help="LLM model to use. Default one is GPT-3.5-turbo.",
    )

    args = parser.parse_args(args=None if sys.argv[1:] else ["--help"])

    generate_questions(
        output_file=args.output_file,
        wrapper_class_path=args.wrapper_class_path,
        num_topics=args.num_topics,
        questions_per_topic=args.questions_per_topic,
        llm_model_provider=args.llm_model_provider,
        llm_model=args.llm_model,
    )


if __name__ == "__main__":
    main()