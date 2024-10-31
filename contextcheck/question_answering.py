import sys
from argparse import ArgumentParser
from pathlib import Path

from contextcheck.generators.generate_answers import AnswerGenerator
from contextcheck.generators.utils import import_class_from_string


def generate_answers(
    output_file: str,
    wrapper_class_path: str,
    top_k: int,
    questions_file: Path,
    use_ranker: bool,
    collection_name: str,
    debug: bool,
) -> None:
    """
    Generate answers for the given questions and save them to a YAML file.

    Args:
        @param output_file: Output path and filename to save the generated questions.
        @param wrapper_class_path: Full path to the API wrapper class definition.
        @param top_k: Number of answers.
        @param questions_file: Path to the questions file.

    Returns:
        None
    """
    api_wrapper = import_class_from_string(wrapper_class_path)

    generator_args = {
        "api_wrapper": api_wrapper(),
        "top_k": top_k,
        "questions_file": questions_file,
        "use_ranker": use_ranker,
        "collection_name": collection_name,
        "debug": debug,
    }

    generator = AnswerGenerator(**generator_args)
    generator.save_to_yaml(output_file)


def main():
    parser = ArgumentParser(
        prog="question_answering.py", description="Refer to readme for more information."
    )
    parser.add_argument(
        "--questions-file",
        type=str,
        required=True,
        help="Path to the YAML file containing the questions.",
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
        "Example: For a class 'ClassName' defined in file 'module/submodule.py' use format"
        " 'module.submodule.ClassName'.",
    )
    parser.add_argument(
        "--top-k",
        type=int,
        default=3,
        help="Number of answers",
    )
    parser.add_argument(
        "--use-ranker",
        type=bool,
        default=True,
        help="Use ranker to get relevant documents. Default is True.",
    )
    parser.add_argument(
        "--collection-name",
        type=str,
        default="default",
        help="Name of the collection to use. Default is 'default'.",
    )

    parser.add_argument(
        "--debug",
        type=bool,
        action="store_true",
        help="It will append semantic search chunks along with the questions",
    )

    args = parser.parse_args(args=None if sys.argv[1:] else ["--help"])

    generate_answers(
        output_file=args.output_file,
        wrapper_class_path=args.wrapper_class_path,
        top_k=args.top_k,
        questions_file=Path(args.questions_file),
        use_ranker=args.use_ranker,
        collection_name=args.collection_name,
        debug=args.debug,
    )


if __name__ == "__main__":
    main()
