import openai
import os
from chatgpt_bot import is_conversation, is_question, truncate_conversation

openai.api_key = os.getenv("OPENAI_API_KEY")

def test_is_question_integration():
    question_sample = [{"role": "user", "content": "Is this a question?"}]
    statement_sample = [{"role": "user", "content": "This is a statement."}]
    advanced_question_sample = [{"role": "user", "content": "is it possible to detect my statement or not"}]
    advanced_ru_question_sample = [{"role": "user", "content": "мне вот интересно молжет ли человек долететть до луны"}]
    statement_ru_sample = [{"role": "user", "content": "раз два три четыре пять"}]

    assert is_question(question_sample) is True, "Expected True for a question"
    assert is_question(advanced_question_sample) is True, "Expected False for a statement"
    assert is_question(advanced_ru_question_sample) is True, "Expected False for a statement"
    assert is_question(statement_sample) is False, "Expected False for a statement"
    assert is_question(statement_ru_sample) is False, "Expected False for a statement"

def test_is_conversation_integration():
    conversation_sample = [
        {"role": "user", "content": "Hey, how are you doing today?"},
        {"role": "user", "content": "I'm doing great, thanks! How about you?"}
    ]
    standalone_sample = [
        {"role": "user", "content": "I love ice cream!"}
    ]
    conversation_ru_sample = [
        {"role": "user", "content": "Привет, как дела?"},
        {"role": "user", "content": "Хорошо, спасибо! А у тебя?"}
    ]
    standalone_ru_sample = [
        {"role": "user", "content": "Я люблю мороженое!"}
    ]
    conversation_sample_2 = [
        {"role": "user", "content": "What's your favorite movie?"},
        {"role": "user", "content": "I really like The Shawshank Redemption. What about you?"}
    ]
    standalone_sample_2 = [
        {"role": "user", "content": "The weather is nice today."}
    ]
    conversation_ru_sample_2 = [
        {"role": "user", "content": "Какая у тебя любимая книга?"},
        {"role": "user", "content": "Мне очень нравится 'Мастер и Маргарита'. А тебе?"}
    ]
    standalone_ru_sample_2 = [
        {"role": "user", "content": "Сегодня хорошая погода."}
    ]

    assert is_conversation(conversation_sample) is True, "Expected True for a conversation"
    assert is_conversation(standalone_sample) is False, "Expected False for a standalone message"
    assert is_conversation(conversation_ru_sample) is True, "Expected True for a conversation in Russian"
    assert is_conversation(standalone_ru_sample) is False, "Expected False for a standalone message in Russian"
    assert is_conversation(conversation_sample_2) is True, "Expected True for a conversation"
    assert is_conversation(standalone_sample_2) is False, "Expected False for a standalone message"
    assert is_conversation(conversation_ru_sample_2) is True, "Expected True for a conversation in Russian"
    assert is_conversation(standalone_ru_sample_2) is False, "Expected False for a standalone message in Russian"
