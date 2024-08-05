import json
import os

import nltk
import yaml
from gensim import corpora
from gensim.models import LdaModel
from gensim.utils import simple_preprocess
from nltk.corpus import stopwords
from pydantic import BaseModel

from contextcheck.endpoints.endpoint import EndpointBase
from contextcheck.endpoints.endpoint_config import EndpointConfig
from contextcheck.endpoints.factory import factory as endpoint_factory
from contextcheck.generators.endpoint_wrapper import RagApiWrapperBase
from contextcheck.models.request import RequestBase
from contextcheck.models.response import ResponseBase

PROMPT_SINGLE_QUESTION = """Generate question basing on the content chunks above. Only respond with the question, do not provide answers. 
Put question in a separate JSONL entity. Use the following format:
{"question": "<QUESTION>"}
"""

PROMPT_QUESTIONS = """Generate {num_questions} questions basing on the content chunks above. Only respond with the questions, do not provide answers. 
Put each question in a separate JSONL entity. Use the following format:
{{"question": "<QUESTION>"}}
"""


class QuestionsGenerator(BaseModel):
    num_topics: int = 10
    questions_per_topic: int = 3
    words_per_topic: int = 30

    api_wrapper: RagApiWrapperBase
    questions_generator_endpoint_config: EndpointConfig
    llm_endpoint: EndpointBase | None = None

    stop_words: set = set(stopwords.words(["english", "spanish"]))
    generated_questions: list[str] = []

    def model_post_init(self, __context) -> None:
        nltk.download("stopwords")
        self.llm_endpoint = endpoint_factory(self.questions_generator_endpoint_config)

    def preprocess_text(self, text: str, stop_words):
        result = []
        for token in simple_preprocess(text, deacc=True):
            if token not in self.stop_words and len(token) > 3:
                result.append(token)
        return result

    def get_topic_lists_from_chunks(self, documents: list[str]):
        processed_documents = [self.preprocess_text(doc, self.stop_words) for doc in documents]

        dictionary = corpora.Dictionary(processed_documents)
        corpus = [dictionary.doc2bow(doc) for doc in processed_documents]

        lda_model = LdaModel(corpus, num_topics=self.num_topics, id2word=dictionary, passes=15)

        topics = lda_model.print_topics(num_words=self.words_per_topic)

        topics_ls = []
        for topic in topics:
            words = topic[1].split("+")
            topic_words = [word.split("*")[1].replace('"', "").strip() for word in words]
            topics_ls.append(topic_words)

        return topics_ls

    def _prepare_request(self, chunks: list[dict]) -> RequestBase:
        if self.questions_per_topic > 1:
            prompt = PROMPT_QUESTIONS.format(num_questions=self.questions_per_topic)
        else:
            prompt = PROMPT_SINGLE_QUESTION

        chunks_joined = "\n---\n".join([chunk["chunk"] for chunk in chunks])
        message = f"{chunks_joined}.\n\n------\n{prompt}"
        return RequestBase(message=message)

    def _parse_response(self, response: ResponseBase) -> list[str]:
        """Split the response by newlines and extract the question from each JSON entity.
        Return a list of questions."""
        msg = response.message
        questions = msg.split("\n")
        parsed_questions = []
        for q in questions:
            try:
                parsed_questions.append(json.loads(q)["question"])
            except:
                continue
        return parsed_questions

    def generate(self) -> list[str]:
        documents = self.api_wrapper.list_documents()

        questions = []

        for document in documents:
            chunks = self.api_wrapper.get_document_chunks(document["id"])
            document_topics = self.get_topic_lists_from_chunks(chunks)

            topic_questions = []
            for topic_num, topic in enumerate(document_topics):
                print(f"Generating questions for document {document['name']} topic {topic_num}.")
                # Get chunks from semantic db with space separated topic words
                topic_chunks = self.api_wrapper.query_semantic_db(" ".join(topic))

                prompt = self._prepare_request(topic_chunks)
                response = self.llm_endpoint.send_request(prompt)
                topic_questions += self._parse_response(response)

            questions.append({"document": document["name"], "questions": topic_questions})

        self.generated_questions = questions
        return questions

    def save_to_yaml(self, filepath: str):
        if not self.generated_questions:
            self.generate()

        dirs = os.path.dirname(filepath)
        if dirs:
            os.makedirs(dirs, exist_ok=True)

        with open(filepath, "w") as f:
            yaml.dump({"questions": self.generated_questions}, stream=f, width=200)
