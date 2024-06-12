HALLUCINATION_PROMPT_TEMPLATE = """
In this task, you will be presented with a query, a reference text and an answer. The answer is
generated to the question based on the reference text. The answer may contain false information. You
must use the reference text to determine if the answer to the question contains false information,
if the answer is a hallucination of facts. Your objective is to determine whether the answer text
contains factual information and is not a hallucination. A 'hallucination' refers to
an answer that is not based on the reference text or assumes information that is not available in
the reference text. "hallucinated" indicates that the answer
provides factually inaccurate information to the query based on the reference text. "factual"
indicates that the answer to the question is correct relative to the reference text, and does not
contain made up information. Please read the query and reference text carefully before determining
your response.

[BEGIN DATA]
************
[Query]: {input}
************
[Reference text]: {reference}
************
[Answer]: {output}
************
[END DATA]

Is the answer above factual or hallucinated based on the query and reference text? 
Your response should be a single word: either "factual" or "hallucinated", and it should not include any other text or characters.
"""

QA_REFERENCE_PROMPT_TEMPLATE = """
You are given a question, an answer and reference text. You must determine whether the
given answer correctly answers the question based on the reference text. Here is the data:
[BEGIN DATA]
************
[Question]: {input}
************
[Reference]: {reference}
************
[Answer]: {output}
[END DATA]

Your response must be a single word, either "correct" or "incorrect", and should not contain any text or characters aside from that word.
"correct" means that the question is correctly and fully answered by the answer.
"incorrect" means that the question is not correctly or only partially answered by the answer.
"""

MODEL_GRADING_QA_PROMPT_TEMPLATE = """
You are grading output according to a user-specified rubric. If the statement in the rubric is true, then the output passes the test.

[EXAMPLES]
************
[Output]: Hello world
************
[Rubric]: Content contains a greeting
************
correct

************
[Output]: Avast ye swabs, repel the invaders!
************
[Rubric]: Does not speak like a pirate
************
incorrect
[END EXAMPLES]

[BEGIN DATA]
[Output]: {output}
************
[Rubric]: {assertion}
************
[END DATA]

Your response must be a single word, either "correct" or "incorrect", and should not contain any text or characters aside from that word.
"correct" means that the output meets the criteria specified in the rubric.
"incorrect" means that the output does not meet the criteria specified in the rubric.
"""

SUMMARIZATION_PROMPT_TEMPLATE = """
You are comparing the summary text and it's original document and trying to determine if the summary is good. Here is the data:
[BEGIN DATA]
************
[Summary]: {output}
************
[Original Document]: {input}
[END DATA]

Compare the Summary above to the Original Document and determine if the Summary is comprehensive, concise, coherent, 
and independent relative to the Original Document. 
Your response must be a single word, either "good" or "bad", and should not contain any text or characters aside from that. 
"bad" means that the Summary is not comprehensive, concise, coherent, and independent relative to the Original Document. 
"good" means the Summary is comprehensive, concise, coherent, and independent relative to the Original Document.
"""

HUMAN_VS_AI_PROMPT_TEMPLATE = """
You are comparing a human ground truth answer from an expert to an answer from an AI model.
Your goal is to determine if the AI answer correctly matches, in substance, the human answer.
[BEGIN DATA]
************
[Question]: {input}
************
[Human Ground Truth Answer]: {reference}
************
[AI Answer]: {output}
************
[END DATA]

Compare the AI answer to the human ground truth answer, if the AI correctly answers the question, then the AI answer is "correct". 
If the AI answer is longer but contains the main idea of the Human answer please answer "correct". 
If the AI answer divergences or does not contain the main idea of the human answer, please answer "incorrect".
Your response must be a single word, either "correct" or "incorrect", and should not contain any text or characters aside from that. 
"""
