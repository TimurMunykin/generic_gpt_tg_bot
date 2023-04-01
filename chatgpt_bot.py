import os
import openai
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

openai.api_key = os.getenv("OPENAI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TG_API_KEY")

def chatgpt_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=2048,
        n=1,
        stop=None,
        temperature=0.8,
    )

    return response.choices[0].text.strip()

def mention_handler(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    message = update.effective_message.text
    user = update.effective_user.username
    bot_name = context.bot.username

    logger = logging.getLogger(__name__)
    logger.info(f"Received mention from @{user} in chat_id: {chat_id}")

    if bot_name in message:
        prompt = f"{user}: {message.replace('@' + bot_name, '').strip()}"
        response = chatgpt_response(prompt)
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
