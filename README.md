# Operators Bot

A simple Discord bot with **tarot readings**, **operator philosophy** when you @mention it, **/reflect** for journaling prompts, and **/leverage** for mental models. Built with [discord.py](https://discord.py.readthedocs.io/).

## Setup

1. **Python 3.8+**  
   Make sure Python is installed.

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Create a Discord application and bot**
   - Go to [Discord Developer Portal](https://discord.com/developers/applications) → New Application.
   - In the app, open **Bot** → Add Bot. Copy the **token** (keep it secret).
   - In **OAuth2 → URL Generator**, select scopes: `bot`, `applications.commands`. Copy the generated URL and open it in a browser to invite the bot to your server.

4. **Set your bot token**
   - Option A: Create a `.env` file in this folder (recommended):
     ```
     BOT_TOKEN=your_token_here
     ```
   - Option B: Set an environment variable, e.g. `set BOT_TOKEN=your_token_here` (Windows).

5. **Run the bot**
   ```bash
   python bot.py
   ```

## Commands

| Command   | Description |
|----------|-------------|
| `/tarot [cards]` | Tarot reading. Use 1, 2, or 3 cards (default 1). |
| `/reflect`      | Get a random journaling prompt. |
| `/leverage`      | Get a random mental model. |
| **@mention bot** | Bot replies with a random operator philosophy quote. |

## Project layout

- `bot.py` – All bot logic (single file, beginner-friendly).
- `requirements.txt` – Python dependencies.

Enjoy.
