# English Yummy Bot

**English Yummy Bot** is a Telegram-based educational assistant for young learners of English as a Foreign Language.  
It provides vocabulary training, reading and listening comprehension, writing practice, and test-style review exercises.

The bot is available at: [@englishyummybot2025_bot](https://t.me/englishyummybot2025_bot)

If the hosted version is unavailable, you can run it locally using the instructions below.

---

## Features

- Vocabulary learning with category-based flashcards (links to Quizlet)
- Listening comprehension using AI-generated audio
- Reading passages followed by multiple choice
- Writing prompts based on food-related images
- Session progress tracking with accuracy and mistake feedback
- Final test link to assess vocabulary mastery
- Fuzzy error-checking using `SequenceMatcher` to tolerate minor typos

---

## Requirements

- Python 3.10+
- Telegram Bot token (create one at [BotFather](https://t.me/BotFather))

---

## Running Locally

1. **Clone the repository**
```bash
git clone https://github.com/Ildar-Galiev2408/english_yummy_bot.git
cd english_yummy_bot
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Export your bot token**
```bash
export API_TOKEN=your-telegram-bot-token
```
For Windows PowerShell:
```powershell
$env:API_TOKEN="your-telegram-bot-token"
```

4. **Run the bot**
```bash
python bot.py
```

---

## Deployment

The bot is currently deployed to [Render](https://render.com) and linked to this repository.

---

## Project Structure

```
english_yummy_bot/
├── bot.py               # Bot logic and handlers
├── requirements.txt     # Python dependencies
├── Dockerfile           # Deployment build config
├── fly.toml             # Legacy Fly.io config (optional)
├── audio/               # Pre-generated mp3 files for listening
├── images/              # Vocabulary prompt images
└── README.md
```

---

## License

MIT License

---

## Author

Ildar Galiev  
