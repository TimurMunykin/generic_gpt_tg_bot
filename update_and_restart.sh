#!/bin/bash

# Change to the directory where your chatbot is located
cd $CHATBOT_DIR

# Stop the currently running chatbot instance (if it's running)
if pgrep -f "chatgpt_bot.py" > /dev/null; then
    pkill -f "chatgpt_bot.py"
fi

# Pull the latest changes from the Git repository
git pull

# Install any new dependencies
pip install -r requirements.txt

# Start the updated chatbot instance
nohup python chatgpt_bot.py &
