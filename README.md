# ScreenAlertArgsTgBot

A small Windows tool that sends a message or a screenshot to Telegram from the command line.

Pass text as arguments and the bot delivers it to your chat. Add the word `screen` or `png` and it attaches a screenshot of your display. Useful for alerts from scripts, scheduled tasks and remote machines.

## Features

- Sends text messages to a Telegram chat.
- Captures the screen and sends it as an image.
- Configured through a simple `config.ini` file.
- Can be compiled into a single `.exe` with PyInstaller.

## Tech

Python 3.11 · `pyTelegramBotAPI` · `Pillow` · `configparser` · PyInstaller

## Quick start

1. Clone the repository and install dependencies:

   ```bash
   git clone https://github.com/tankow79/ScreenAlertArgsTgBot.git
   cd ScreenAlertArgsTgBot
   pip install -r requirements.txt
   ```

2. Copy `config.ini.example` to `config.ini` and fill in your values:

   ```ini
   [telegram]
   bot_token = <your_telegram_bot_token>
   chat_id = <your_chat_id>
   computer_name = My_PC
   ```

   | Key | Meaning |
   |---|---|
   | `bot_token` | Token of your Telegram bot (from @BotFather) |
   | `chat_id` | ID of the chat that receives messages |
   | `computer_name` | Name used in message captions |

3. Run it:

   ```bash
   python main.py Hello, Telegram!
   python main.py screen Here is my screen
   ```

## Build an .exe

```bash
pip install pyinstaller
```

**Config next to the exe** (editable after build):

```bash
pyinstaller -w -F --hidden-import=pyTelegramBotAPI main.py
```

Copy `config.ini` into the `dist/` folder next to the exe.

**Config embedded in the exe** (not editable after build):

```bash
pyinstaller -w -F --hidden-import=pyTelegramBotAPI --add-data "config.ini;." main.py
```

Options: `-w` hides the console window, `-F` packs everything into one file, `--hidden-import` includes the Telegram library. On Linux and macOS use `:` instead of `;` in `--add-data`.

The result is `dist/main.exe`. Rename it if you like, for example to `ScreenAlertArgsTgBot.exe`, then run:

```bash
ScreenAlertArgsTgBot.exe screen Here is my screen
```

## Security

Keep your real bot token private. Do not publish a `config.ini` that contains it, and if a token ever leaks, revoke it in @BotFather.

## Project structure

```
.
├─ main.py
├─ config.ini.example
├─ requirements.txt
└─ README.md
```
