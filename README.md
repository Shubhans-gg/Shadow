# Shadow 🖤

A Python-based voice assistant that responds to voice commands and answers questions using Gemini AI.

## Features
-  Wake word activation ("arise")
-  Gemini AI for smart responses
-  Open websites by voice
-  Play YouTube videos
-  Wikipedia search
-  Google search
-  Weather updates
-  Latest news
-  Hindi translation
-  Open system apps (Notepad, Calculator)
-  Coin flip & dice roll
-  Voice calculations
-  Exit by saying "rest" or pressing ESC

## Tech Stack
- Python
- SpeechRecognition
- pyttsx3
- Google Gemini API
- OpenWeatherMap API
- NewsAPI
- Wikipedia
- Deep Translator
- pywhatkit

## Setup
1. Clone the repo
2. Create virtual environment: `python -m venv .venv`
3. Activate it: `.venv\Scripts\activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Create `.env` file and add your API keys:
```
GEMINI_API_KEY=your_key
WEATHER_API_KEY=your_key
NEWS_API_KEY=your_key
```
6. Run: `python main.py`
7. Say **"arise"** to activate Shadow

## Commands
| Command | Action |
|---|---|
| "arise" | Wake up Shadow |
| "open youtube" | Opens YouTube |
| "play [video title]" | Plays the video on YouTube |
| "search [query]" | Google search |
| "[topic] wikipedia" | Wikipedia summary |
| "weather in [city]" | Weather update |
| "news" | Top 3 headlines |
| "translate [text] to hindi" | Hindi translation |
| "calculate [math]" | Solve calculations |
| "flip a coin" | Heads or tails |
| "roll a dice" | Random 1-6 |
| "rest" | Shutdown Shadow |

## Note
- Brave Browser is used by default if installed, otherwise falls back to your default browser
- Hindi translation opens Google Translate in browser (TTS doesn't support Hindi)
- Gemini API free tier has rate limits — if Shadow doesn't respond, wait a moment and try again

## Author
Built by [Shubhans](https://github.com/Shubhans-gg) 🖤
