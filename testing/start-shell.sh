#!/usr/bin/env bash

# Updates remote plugins and launches neovim with clear vimrc and current
# directory in runtime path. Also spawns a python3 interactive shell.

nvim -u ./vimrc +UpdateRemotePlugins +qall > /dev/null

tmux split-window -p 30 "sleep 1; NVIM_LISTEN_ADDRESS=/tmp/nvim.socket python3 interactive-shell.py"

NVIM_LISTEN_ADDRESS=/tmp/nvim.socket nvim -u ./vimrc
