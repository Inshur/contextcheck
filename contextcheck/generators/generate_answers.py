import os
from pathlib import Path

import yaml
from pydantic import BaseModel, ConfigDict, Field, TypeAdapter

from contextcheck.generators.endpoint_wrapper import RagApiWrapperBase
from contextcheck.loaders.yaml import load_yaml_file


# NOTE RB: There's no yaml for answer generation therefore I've deduced the structure from code
class DocumentQuestions(BaseModel):
    model_config = ConfigDict(extra="ignore")

    document: str = Field(description="A document from which a question is derived?")
    questions: list[str] = Field(description="A list of questions regarding a document")


# NOTE RB: It probably won't work with new changes to ContextClue (new checkbox in MR template? :P)
class AnswerGenerator(BaseModel):
    top_k: int = 3
    collection_name: str = "default"
    questions_file: Path
    api_wrapper: RagApiWrapperBase
    questions: list[DocumentQuestions] = Field(
        default_factory=list, description="A list of nested questions regarding a document"
    )
    alpha: float = 0.75
    use_ranker: bool = True
    debug: bool = False

    def model_post_init(self, __context):
        questions_dict = load_yaml_file(self.questions_file)["questions"]
        self.questions = TypeAdapter(list[DocumentQuestions]).validate_python(questions_dict)

    def generate(self) -> dict:
        """
        Generate answers for the given questions.

        Returns:
            dict: A dictionary containing the questions and their answers.
        """

        qa_data = {"QA": []}

        for document_questions in self.questions:
            current_document = document_questions.document
            entry = {"document": current_document, "qa": []}
            list_of_questions = document_questions.questions
            data = {}
            print("Generating answers for document:", current_document)
            for idx, question in enumerate(list_of_questions):
                answers = self.api_wrapper.query_qa(
                    question, use_ranker=self.use_ranker, top_k=self.top_k, alpha=self.alpha
                )
                data["item_" + str(idx)] = {
                    "question": question,
                    "answer": answers["result"],
                }

                if self.debug:
                    data["item_" + str(idx)] = {
                        "answers": [
                            [
                                {
                                    "chunk": answer["chunk"],
                                    "document": answer["metadata"]["document_name"],
                                }
                            ]
                            for answer in answers[
                                : self.top_k
                            ]  # NOTE RB: Why self.top_k is used here?
                        ]
                    }

                print(f"Processing {idx + 1}/{len(list_of_questions)} questions")
                entry["qa"].append(data["item_" + str(idx)])
            qa_data["QA"].append(entry)

        return qa_data

    def save_to_yaml(self, filepath: str):
        """
        Save the generated questions to a YAML file.

        Args:
            filepath (str): The path to the output file.

        Returns:
            None
        """
        qa = self.generate()
        dirs = os.path.dirname(filepath)
        if dirs:
            os.makedirs(dirs, exist_ok=True)

        with open(filepath, "w") as f:
            yaml.dump(qa, stream=f, width=200)
