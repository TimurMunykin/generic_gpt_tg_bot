import os
import openai
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from collections import defaultdict


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

openai.api_key = os.getenv("OPENAI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TG_API_KEY")

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

def mention_handler(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    message = update.effective_message.text
    user = update.effective_user.username
    bot_name = context.bot.username

    logger = logging.getLogger(__name__)
    logger.info(f"Received mention from @{user} in chat_id: {chat_id}")

    if bot_name in message:
        message_without_mention = message.replace('@' + bot_name, '').strip()

        # Add the user's message to the conversation history
        conversations[chat_id].append({"role": "user", "content": message_without_mention})

        response = chatgpt_response(conversations[chat_id])

        # Add the bot's response to the conversation history
        conversations[chat_id].append({"role": "assistant", "content": response})

        update.message.reply_text(f"@{user} {response}")

def main():
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, mention_handler))

    logger = logging.getLogger(__name__)
    logger.info("Bot started successfully")

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
