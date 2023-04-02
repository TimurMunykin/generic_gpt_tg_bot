import openai
import os
from chatgpt_bot import is_question

openai.api_key = os.getenv("OPENAI_API_KEY")

def test_is_question_integration():
    question_sample = [{"role": "user", "content": "Is this a question?"}]
    statement_sample = [{"role": "user", "content": "This is a statement."}]
    advanced_question_sample = [{"role": "user", "content": "is it possible to detect my statement or not"}]
    advanced_ru_question_sample = [{"role": "user", "content": "мне вот интересно молжет ли человек долететть до луны"}]

    assert is_question(question_sample) is True, "Expected True for a question"
    assert is_question(advanced_question_sample) is True, "Expected False for a statement"
    assert is_question(advanced_ru_question_sample) is True, "Expected False for a statement"
    assert is_question(statement_sample) is False, "Expected False for a statement"
