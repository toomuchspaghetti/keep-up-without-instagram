# keep up without instagram

if you ever wanted to get instagram message notifications without having instagram installed, here's the program for you.

## `.env`
you need to supply the following in a `.env` file:
1. `TELEGRAM_TOKEN`: your telegram bot's token
2. `TELEGRAM_CHAT_ID`: the chat id of the user you want notified of your instagram messages
3. `INSTAGRAM_SESSION_ID`: your instagram `sessionid` cookie (do not share!)
4. `CHROMIUM_PATH`: a path to a chromium binary

## set up
steps for setting up:
1. `npm i`
2. `python3 -m venv .venv`
3. `source .venv/bin/activate`
4. `pip install -r requirements.txt`

## running the program
run with `python main.py`

## enjoy!