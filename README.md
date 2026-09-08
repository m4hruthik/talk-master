# 🗣️ TalkMaster

**Learn to talk like anyone you want to be.**

TalkMaster is a web app that helps you learn different communication styles — from leadership and confidence to flirty, romantic, and lovable. Pick a style, study the principles, see before-and-after examples, and practice with real exercises.

## ✨ Features

- **7 Communication Styles**: The Leader, The Charmer, The Flirt, The Romantic, The Sweetheart, The Storyteller, The Diplomat
- **Before & After Examples**: See weak vs. powerful ways of saying the same thing
- **Do's & Don'ts**: Quick-reference checklists for each style
- **Practice Exercises**: Actionable exercises you can try in real life
- **Interactive Quizzes**: Test your understanding with generated quiz questions
- **Pro Tips**: Battle-tested advice for each communication mode
- **Beautiful Dark UI**: Modern, responsive design with smooth animations

## 🎨 Communication Styles

| Style | What You'll Learn |
|-------|------------------|
| 👑 The Leader | Command authority, inspire others, speak with conviction |
| ✨ The Charmer | Be magnetic, make people feel special, use humor |
| 😏 The Flirt | Playful teasing, creating tension, being intriguing |
| 💖 The Romantic | Speaking from the heart, vulnerability, sincerity |
| 🌸 The Sweetheart | Warmth, kindness, making people feel safe |
| 🎭 The Storyteller | Hooks, pacing, making any conversation captivating |
| 🤝 The Diplomat | Persuasion, negotiation, collaborative communication |

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/m4hruthik/talk-master.git
cd talk-master

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
```

The app will be available at `http://localhost:5000`.

## 🛠️ Tech Stack

- **Backend**: Python + Flask
- **Frontend**: HTML, CSS, JavaScript (vanilla)
- **Fonts**: Google Fonts (Inter)

## 📁 Project Structure

```
talk-master/
├── app.py                 # Flask app with routes & communication data
├── requirements.txt       # Python dependencies
├── README.md             # You are here
├── static/
│   ├── css/
│   │   └── style.css      # All styling
│   └── js/
│       └── app.js         # Frontend interactions
└── templates/
    ├── base.html          # Base template
    ├── index.html          # Home page — style selection
    ├── learn.html          # Learning page for each style
    └── not_found.html      # 404 page
```

## 📖 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Home page with style selection |
| `/learn/<style_id>` | GET | Learning page for a specific style |
| `/api/quiz/<style_id>` | GET | Generate a random quiz question |
| `/api/practice/<style_id>` | GET | Get a random practice exercise |
| `/health` | GET | Health check |

## 🤝 Contributing

Contributions are welcome! If you'd like to add a new communication style or improve existing ones:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/new-style`)
3. Add your style to the `STYLES` dictionary in `app.py`
4. Commit your changes (`git commit -m 'Add new communication style'`)
5. Push to the branch (`git push origin feature/new-style`)
6. Open a Pull Request

## 📝 License

This project is open source and available under the MIT License.

---

Built with 💜 for people who want to communicate better.
