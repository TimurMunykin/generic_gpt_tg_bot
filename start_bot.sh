#!/bin/bash
cd "$(dirname "$0")"
nohup python3 chatgpt_bot.py > chatgpt_bot.log 2>&1 & disown
