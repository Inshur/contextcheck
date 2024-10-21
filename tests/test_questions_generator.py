from unittest.mock import patch

import lorem
import pytest

from contextcheck.endpoints.endpoint_config import EndpointConfig
from contextcheck.generators.endpoint_wrapper import RagApiWrapperBase
from contextcheck.generators.generate_questions import QuestionsGenerator


@pytest.fixture
def api_wrapper_mock():
    class RagApiWrapperMock(RagApiWrapperBase):
        def list_documents(self) -> list[dict[str, str]]:
            return [{"id": "1", "name": "Document 1"}, {"id": "2", "name": "Document 2"}]

        def get_document_chunks(self, document_id: str) -> list[str]:
            return [lorem.paragraph() for _ in range(20)]

        def query_semantic_db(self, query: str) -> list[dict]:
            return [{"chunk": lorem.paragraph()} for _ in range(10)]

        def query_qa(self, query: str) -> list[dict]:
            return [{"result": lorem.paragraph()} for _ in range(20)]

    return RagApiWrapperMock()


@patch("contextcheck.generators.generate_questions.endpoint_factory")
def test_generate_questions(endpoint_factory_mock, api_wrapper_mock):
    endpoint_factory_mock.return_value.send_request.return_value.message = "\n".join(
        [f'{{"question": "What is Foo ({i})?"}}' for i in range(3)]
    )

    generator = QuestionsGenerator(
        api_wrapper=api_wrapper_mock,
        questions_generator_endpoint_config=EndpointConfig(kind="echo"),
    )
    questions = generator.generate()

    assert len(questions) == 2
    assert all(isinstance(q, dict) for q in questions)
    assert all("document" in q and "questions" in q for q in questions)
    assert all(isinstance(q["document"], str) for q in questions)
    assert all(isinstance(q["questions"], list) for q in questions)

    for document_questions in questions:
        assert len(document_questions["questions"]) == 30
        assert all(q.startswith("What is Foo") for q in document_questions["questions"])
