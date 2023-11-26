# Claude Linguist: Anthropic Hack Language Learning Bot Project
If we strive to learn a new language, the most important part is to have someone to practice converstation with, someone to correct you when you get things wrong and to teach you new words. Enter Claude.

The goal is to create a Telegram bot that helps you learn a language by conversing with you in that language.

* Practice conversation 
* Learn new words
* Get corrections on your grammar

<img src="https://github.com/amberrignell/anthropic-hack-2023/assets/79009541/96051729-567d-4b7d-a759-9ebaad18aa0d" alt="Claude Linguist" width="300">

## How it works
Telegram facilitates using Claude as easily as you would message a friend. But it is important to note that Claude is an LLM, not a friend. 

Rigorous prompt engineering structures Claude's response to highlight mistakes, teach new words and then include them the response.

# Setup ( <3 minutes )
```
python3 -m venv venv
source venv/bin/activate
pip install python-telegram-bot requests python-dotenv anthropic
```

You will need to create a `.env` file with the following contents:
```
AUTH_TOKEN=<your telegram bot token>
ANTHROPIC_API_KEY=<your anthropic api key>
```

See [here](https://core.telegram.org/bots/features#creating-a-new-bot) for creating a telegram bot and getting the token.

```
python src/main.py
```
## Team
Amber Rignell, Mimi Reyburn, Louis Horrell.
