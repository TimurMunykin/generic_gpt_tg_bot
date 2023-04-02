import os
import openai
import logging
from telegram import Update, MessageEntity
from collections import deque
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from collections import defaultdict

log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
log_handler = logging.FileHandler('conversation_logs.log', mode='a', encoding='utf-8')
log_handler.setFormatter(log_formatter)

conversation_logger = logging.getLogger('conversation_logs')
conversation_logger.setLevel(logging.INFO)
conversation_logger.addHandler(log_handler)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

openai.api_key = os.getenv("OPENAI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TG_API_KEY")

def get_chat_logger(chat_id):
    logger_name = f"conversation_{chat_id}"
    chat_logger = logging.getLogger(logger_name)

    if not chat_logger.handlers:
        log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        log_handler = logging.FileHandler(f'conversation_logs_{chat_id}.log', mode='a', encoding='utf-8')
        log_handler.setFormatter(log_formatter)

        chat_logger.setLevel(logging.INFO)
        chat_logger.addHandler(log_handler)

    return chat_logger

def start_command(update: Update, context: CallbackContext):
    update.message.reply_text("Hello! I'm a helpful assistant. Just mention me or send a message in the chat, and I'll try to help!")

def chatgpt_response(conversation_history):
    conversation = [
        {"role": "system", "content": "You are a helpful assistant."},
    ] + conversation_history

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation,
        max_tokens=2048,
        n=1,
        stop=None,
        temperature=0.8,
    )

    return response.choices[0].message['content']

conversations = defaultdict(list)

def is_question(conversation_history):
    conversation = [
        {"role": "system", "content": "You are a multilingual assistant that determines if the user's message is a question or not."},
    ] + conversation_history

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation,
        max_tokens=600,
        n=1,
        stop=None,
        temperature=0.8,
    )

    response_text = response.choices[0].message['content'].lower()

    english_keywords = ["question", "ask", "inquiry"]
    russian_keywords = ["вопрос", "спрашивает", "запрос"]

    if any(keyword in response_text for keyword in english_keywords + russian_keywords):
        return True
    else:
        return False


def text_message_handler(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    message = update.effective_message.text
    user = update.effective_user.username

    chat_logger = get_chat_logger(chat_id)
    chat_logger.info(f"Received message from @{user} in chat_id: {chat_id}")

    # Add the user's message to the conversation history
    conversation = [{"role": "user", "content": message}]

    # Check if the message is a question
    if is_question(conversation):
        # Add the user's question to the conversation history
        conversations[chat_id].append({"role": "user", "content": message})

        response = chatgpt_response(conversations[chat_id])

        # Add the bot's response to the conversation history
        conversations[chat_id].append({"role": "assistant", "content": response})

        # Log the conversation
        chat_logger.info(f"User: @{user} | Message: {message} | Response: {response}")

        update.message.reply_text(f"@{user} {response}")
    else:
        # If it's not a question, you can either ignore it or process it differently
        pass

def mention_handler(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    message = update.effective_message.text
    user = update.effective_user.username
    bot_name = context.bot.username

    chat_logger = get_chat_logger(chat_id)
    chat_logger.info(f"Received mention from @{user} in chat_id: {chat_id}")

    if bot_name in message:
        message_without_mention = message.replace('@' + bot_name, '').strip()

        # Add the user's message to the conversation history
        conversations[chat_id].append({"role": "user", "content": message_without_mention})

        response = chatgpt_response(conversations[chat_id])

        # Add the bot's response to the conversation history
        conversations[chat_id].append({"role": "assistant", "content": response})

        # Log the conversation
        chat_logger.info(f"User: @{user} | Message: {message_without_mention} | Response: {response}")

        update.message.reply_text(f"@{user} {response}")

message_buffers = defaultdict(lambda: deque(maxlen=5))


def main():
    updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Register handlers
    start_handler = CommandHandler('start', start_command)
    mention_message_handler = MessageHandler(Filters.text & Filters.entity(MessageEntity.MENTION), mention_handler)
    text_message_handler_obj = MessageHandler(Filters.text & ~Filters.entity(MessageEntity.MENTION), text_message_handler)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(mention_message_handler)
    dispatcher.add_handler(text_message_handler_obj)

    # Start the bot
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
