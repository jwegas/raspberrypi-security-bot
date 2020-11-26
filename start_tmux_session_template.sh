#!/usr/bin/env bash

#  you can add command to run this script to your .bashrc
#  to run bot after device is booted.

#  put path where Bot Repo was cloned to
HOME_PROJECT=PATH_TO_BOT

#  name of TMUX session
SESSION_NAME=bot

#  start session
#  ut assumes that `venv` is your virtual environment for bot. You can change it.
get_tmux() {
    tmux new -s $SESSION_NAME -n run-bot \; \
        send-keys "cd $HOME_PROJECT" Enter \; \
        send-keys "source ~/venv/bin/activate" Enter \; \
        send-keys "python run_bot.py" Enter
}

tmux has-session -t $SESSION_NAME 2>/dev/null

#  sleep 30 seconds before running
if [ $? != 0 ]; then
  sleep 30
  get_tmux
fi
