# 🗣️ TalkMaster Premium

**Learn to talk like anyone you want to be.**

A premium Flask web app with a 30-day structured curriculum, audio features, progress tracking, gamification, and a beautiful glassmorphism UI with dark/light themes.

## ✨ Features

### 30-Day Structured Curriculum
- **Week 1: Foundations** — Leader & Charmer styles
- **Week 2: Emotional Connection** — Flirt & Romantic styles
- **Week 3: Advanced Expression** — Sweetheart & Storyteller styles
- **Week 4: Mastery & Integration** — Diplomat, style switching, real-world scenarios
- Each day includes a lesson, key takeaway, exercise, quiz, and reflection prompt

### 7 Communication Styles
| Style | What You'll Learn |
|-------|------------------|
| 👑 The Leader | Command authority, inspire others, speak with conviction |
| ✨ The Charmer | Be magnetic, make people feel special, use humor |
| 😏 The Flirt | Playful teasing, creating tension, being intriguing |
| 💖 The Romantic | Speaking from the heart, vulnerability, sincerity |
| 🌸 The Sweetheart | Warmth, kindness, making people feel safe |
| 🎭 The Storyteller | Hooks, pacing, making any conversation captivating |
| 🤝 The Diplomat | Persuasion, negotiation, collaborative communication |

### Audio Features (Web Speech API)
- **Text-to-speech** for all lessons, examples, exercises, and tips
- **Voice selection** — choose from available system voices
- **Speed control** — adjust playback from 0.5x to 1.5x
- **Play/pause toggle** on every audio button
- No external dependencies — uses browser's built-in speech synthesis

### Progress Tracking & Gamification
- **XP system** — earn XP for completing lessons and answering quizzes
- **Levels** — level up every 250 XP
- **Streaks** — track consecutive days of learning
- **13 achievement badges** — unlock by completing milestones
- **Progress ring** — visual circular progress indicator
- **localStorage persistence** — all progress saved in the browser
- **Confetti celebrations** — when you complete lessons or unlock badges

### Premium UI
- **Glassmorphism design** with backdrop blur effects
- **Dark/light theme toggle** with smooth transitions
- **Animated gradient background** that shifts subtly
- **Page enter animations** with fade-up effects
- **Scroll-triggered animations** for cards and elements
- **Smooth hover effects** with depth and glow
- **Toast notifications** for feedback
- **Fully responsive** — works on desktop, tablet, and mobile

## 🚀 Quick Start

```bash
git clone https://github.com/m4hruthik/talk-master.git
cd talk-master
pip install -r requirements.txt
python app.py
```

Open `http://localhost:5000` in your browser.

## 🛠️ Tech Stack

- **Backend**: Python + Flask
- **Frontend**: HTML, CSS, JavaScript (vanilla, no frameworks)
- **Audio**: Web Speech API (SpeechSynthesis)
- **Storage**: localStorage (client-side progress tracking)
- **Fonts**: Google Fonts (Inter)

## 📁 Project Structure

```
talk-master/
├── app.py                    # Flask app with curriculum, styles, and API routes
├── requirements.txt          # Python dependencies
├── README.md
├── static/
│   ├── css/
│   │   └── style.css         # Premium glassmorphism styles
│   └── js/
│       └── app.js            # Audio, progress tracking, UI interactions
└── templates/
    ├── base.html             # Base template with nav, theme toggle
    ├── index.html             # Dashboard with progress, styles, badges
    ├── curriculum.html         # 30-day path overview
    ├── day.html               # Daily lesson page with audio & quiz
    ├── learn.html             # Style reference with audio examples
    └── not_found.html         # 404 page
```

## 📖 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Dashboard with progress, styles, and badges |
| `/learn/<style_id>` | GET | Style reference page with audio |
| `/curriculum` | GET | 30-day curriculum overview |
| `/day/<day_num>` | GET | Individual daily lesson (1-30) |
| `/api/quiz/<style_id>` | GET | Generate a random quiz question |
| `/api/practice/<style_id>` | GET | Get a random practice exercise |
| `/api/curriculum` | GET | Full curriculum data as JSON |
| `/health` | GET | Health check |

## 🎮 Gamification Details

- **XP per lesson**: 50-300 XP depending on lesson type
- **Quiz bonus**: +25 XP per correct answer
- **Levels**: Every 250 XP = 1 level
- **13 badges**: First Step, Week Warriors, Streak badges, XP milestones, Quiz Master, Renaissance Communicator, and TalkMaster Graduate
- **Streak tracking**: Consecutive days of completing lessons

## 📝 License

MIT License — open source and free to use.

---

Built with 💜 for people who want to communicate better.
