"""
TalkMaster - Learn to talk like anyone you want to be.

A Flask web app that helps people learn different communication styles —
from leadership and confidence to flirty, romantic, and lovable.
Users pick a mode and get tips, example phrases, do's & don'ts,
practice exercises, and pro tips.
"""

from flask import Flask, render_template, jsonify, request
import random

app = Flask(__name__)

# ---------------------------------------------------------------------------
# Communication Style Data
# ---------------------------------------------------------------------------

STYLES = {
    "leader": {
        "name": "The Leader",
        "tagline": "Command the room with authority and vision",
        "icon": "👑",
        "color": "#6366f1",
        "color_light": "#e0e7ff",
        "description": (
            "Leadership communication is about clarity, decisiveness, and "
            "inspiring others to follow. You don't need a title to lead — "
            "you need a voice that people trust."
        ),
        "principles": [
            "Speak with certainty, not arrogance — own your statements",
            "Use 'we' more than 'I' to build collective ownership",
            "Paint a vision of where you're going, not just what to do",
            "Be direct but respectful — hedge less, commit more",
            "Listen actively; leaders who listen earn the right to speak",
            "Frame problems as opportunities, not obstacles",
        ],
        "examples": [
            {"bad": "I think maybe we should probably try this approach?", "good": "Here's the plan. We go with this approach because it gives us the best shot at hitting our goal."},
            {"bad": "I don't know, what do you guys want to do?", "good": "I recommend we focus on the top three priorities. Let's start with the first one and move fast."},
            {"bad": "That's not my fault, the team didn't deliver.", "good": "The outcome wasn't what we wanted. I take responsibility — here's what we'll do differently next time."},
            {"bad": "We need to do better somehow.", "good": "By the end of this quarter, we will improve our response time by 30%. Here's how we get there."},
            {"bad": "Um, I guess I could try to lead this project?", "good": "I'll take ownership of this project. Here's the timeline and what I need from each of you."},
        ],
        "dos": [
            "Use confident body language — stand tall, make eye contact",
            "Pause deliberately before key points to create emphasis",
            "Ask powerful questions that make people think deeper",
            "Acknowledge mistakes openly and pivot to solutions",
            "Give credit to others when things go well",
        ],
        "donts": [
            "Overuse filler words like 'um', 'like', 'you know'",
            "Apologize for having an opinion — say it with conviction",
            "Blame others when things go wrong",
            "Talk over people or dismiss their input",
            "Use vague language — 'maybe', 'sort of', 'I guess'",
        ],
        "exercises": [
            "Record yourself giving instructions for a task, then listen back and count filler words",
            "Practice starting sentences with 'I believe', 'I've decided', 'Here's the plan'",
            "Give a 60-second pitch for a project you care about using only confident language",
            "Next time someone asks 'what should we do?', respond with a clear recommendation within 5 seconds",
        ],
        "tips": [
            "Lower your voice slightly at the end of sentences to sound more authoritative",
            "Silence is a leadership tool — learn to be comfortable with pauses",
            "The word 'because' is powerful — always explain your reasoning",
        ],
    },

    "charmer": {
        "name": "The Charmer",
        "tagline": "Be magnetic, confident, and impossible to ignore",
        "icon": "✨",
        "color": "#f59e0b",
        "color_light": "#fef3c7",
        "description": (
            "Charisma isn't something you're born with — it's a skill. "
            "It's the art of making people feel seen, heard, and special "
            "while being unapologetically yourself."
        ),
        "principles": [
            "Make people feel like they're the most interesting person in the room",
            "Use humor to break tension — self-deprecating, never at others' expense",
            "Remember and use people's names — it's the sweetest sound to them",
            "Be genuinely curious; ask questions that go beyond small talk",
            "Express positive emotions openly — enthusiasm is contagious",
            "Compliment specifics, not generics — 'I love how you phrased that' beats 'you're great'",
        ],
        "examples": [
            {"bad": "Nice to meet you.", "good": "I've been looking forward to meeting you — I heard about that project you led. Tell me more about it."},
            {"bad": "Cool outfit.", "good": "That color looks incredible on you — did you pick it for a reason?"},
            {"bad": "Yeah, I had a decent weekend.", "good": "I had the best weekend — tried something totally new. But enough about me, how was yours? I want details."},
            {"bad": "You're funny.", "good": "You have this way of saying things that just catches me off guard. I love it."},
            {"bad": "I like your work.", "good": "The way you handled that situation was sharp. You clearly think two steps ahead."},
        ],
        "dos": [
            "Smile with your eyes — it makes people feel welcome",
            "Lean in slightly when someone is speaking to show genuine interest",
            "Use light, appropriate touch (handshake, shoulder tap) to build warmth",
            "Mirror the energy of the person you're talking to, then raise it slightly",
            "Share brief, funny personal stories to build connection",
        ],
        "donts": [
            "Make everything about yourself — the spotlight should bounce back and forth",
            "Over-compliment to the point it feels fake",
            "Be overly agreeable — having opinions makes you more interesting",
            "Check your phone mid-conversation — it kills the magic instantly",
            "Try too hard — forced charm feels manipulative",
        ],
        "exercises": [
            "Go to a social setting and have a conversation where you ask 3x more questions than you answer",
            "Practice giving 5 different people a specific, genuine compliment today",
            "Memorize one interesting detail about 3 people you meet and reference it later",
            "Tell a 30-second funny story about yourself to a stranger",
        ],
        "tips": [
            "People remember how you made them feel, not what you said",
            "A slight head tilt while listening signals warmth and attentiveness",
            "Laughter shared is connection built — find the joy in conversations",
        ],
    },

    "flirt": {
        "name": "The Flirt",
        "tagline": "Be playful, teasing, and irresistibly fun",
        "icon": "😏",
        "color": "#ec4899",
        "color_light": "#fce7f3",
        "description": (
            "Flirting is playful communication that creates attraction through "
            "humor, teasing, and tension. It's not about being overt — it's "
            "about being intriguing, confident, and fun."
        ),
        "principles": [
            "Tease lightly — make them laugh, not uncomfortable",
            "Create push-pull: show interest, then playfully pull back",
            "Use playful eye contact — hold it a beat longer than normal",
            "Be unpredictable — mix compliments with gentle teasing",
            "Create inside jokes early — shared humor builds intimacy",
            "Leave them wanting more — end conversations at a high point",
        ],
        "examples": [
            {"bad": "You're really pretty.", "good": "Are you always this charming, or is today a special occasion?"},
            {"bad": "I like you.", "good": "I haven't decided if I like you yet, but you're definitely growing on me."},
            {"bad": "We should hang out sometime.", "good": "I'm going to take you to the best coffee place in town. Non-negotiable."},
            {"bad": "You have a nice smile.", "good": "That smile is dangerous. You should come with a warning label."},
            {"bad": "Can I get your number?", "good": "Give me your phone. I'm putting my number in. You can decide later if you want to use it."},
        ],
        "dos": [
            "Read the room — calibrate your energy to their response",
            "Use playful challenges: 'I bet you can't...' or 'You seem like the type who...'",
            "Smile slyly — half-smiles create intrigue",
            "Create playful nicknames or inside references",
            "Be comfortable with silence — tension builds attraction",
        ],
        "donts": [
            "Cross the line from playful to disrespectful — if they look uncomfortable, dial it back",
            "Be too available — mystery is attractive",
            "Use crude or overly sexual language too early",
            "Compliment appearance too much — compliment personality and vibe instead",
            "Force it — if the banter isn't flowing, just be genuine",
        ],
        "exercises": [
            "Practice playful teasing with a friend — say something cheeky, then immediately smile to soften it",
            "Write 5 playful responses to common compliments and practice delivering them naturally",
            "Next conversation, try holding eye contact 2 seconds longer than usual and notice the shift",
            "Practice the 'takeaway' — end a fun conversation first, before it dies down",
        ],
        "tips": [
            "Confidence is the foundation — flirting without confidence feels awkward",
            "Your tone of voice matters more than your words — slow down, lower the pitch",
            "Playful disagreement is more attractive than constant agreement",
        ],
    },

    "romantic": {
        "name": "The Romantic",
        "tagline": "Speak from the heart with warmth and sincerity",
        "icon": "💖",
        "color": "#e11d48",
        "color_light": "#ffe4e6",
        "description": (
            "Romantic communication is about vulnerability, sincerity, and "
            "making someone feel deeply valued. It's not grand gestures — "
            "it's the small, genuine words that land in the heart."
        ),
        "principles": [
            "Be specific about what you love — details show you truly see them",
            "Vulnerability is strength — share your real feelings without hedging",
            "Express appreciation for who they are, not just what they do for you",
            "Use 'I feel' statements — own your emotions instead of projecting",
            "Timing matters — romantic words hit harder in quiet, intimate moments",
            "Actions amplify words — follow through on what you say",
        ],
        "examples": [
            {"bad": "I love you.", "good": "I love the way your whole face lights up when you talk about something you care about. It's my favorite thing."},
            {"bad": "You're special to me.", "good": "Before I met you, my days felt ordinary. Now even the boring moments feel like something, just because you're in them."},
            {"bad": "Thanks for everything.", "good": "I don't say it enough, but the way you show up for the people you love — including me — it's rare. I notice it. I'm grateful for it."},
            {"bad": "You look nice today.", "good": "There's something about the way you look right now — it's not just how you appear. It's the energy. It stops me for a second every time."},
            {"bad": "I'm glad you're in my life.", "good": "You make me want to be better — not because you ask me to, but because loving you makes me want to give you the best version of myself."},
        ],
        "dos": [
            "Write handwritten notes — they carry weight texts never will",
            "Remember small details they mention and bring them up later",
            "Express feelings in quiet moments — a whisper hits harder than a shout",
            "Be present — put the phone down and give them your full attention",
            "Say their name with warmth — it changes the entire tone",
        ],
        "donts": [
            "Use generic lines you found online — sincerity can't be copy-pasted",
            "Rush the moment — let pauses breathe",
            "Overdo it to the point it feels performative",
            "Use romantic words as a transaction or to get something",
            "Forget that listening is just as romantic as speaking",
        ],
        "exercises": [
            "Write down 5 specific things you appreciate about someone you love — be detailed",
            "Practice saying 'I feel [emotion] when you [specific action]' without blaming",
            "Leave an unexpected note for someone — no occasion needed",
            "Tell someone one thing you've been feeling but haven't said yet",
        ],
        "tips": [
            "Eye contact during emotional words multiplies their impact",
            "A soft, slower tone signals sincerity — speed signals nervousness",
            "Sometimes the most romantic thing you can say is nothing — just hold their hand",
        ],
    },

    "sweetheart": {
        "name": "The Sweetheart",
        "tagline": "Be warm, kind, and impossible not to adore",
        "icon": "🌸",
        "color": "#14b8a6",
        "color_light": "#ccfbf1",
        "description": (
            "Being a sweetheart is about genuine warmth that makes people "
            "feel safe and valued around you. It's not about being a pushover "
            "— it's about kindness that comes from strength."
        ),
        "principles": [
            "Kindness is a choice — choose it especially when it's hard",
            "Make people feel safe to be themselves around you",
            "Small acts of care matter more than big gestures",
            "Celebrate others' wins like they're your own",
            "Be the person who checks in, remembers, and follows through",
            "Warmth + boundaries = irresistible — kind doesn't mean weak",
        ],
        "examples": [
            {"bad": "Oh, I'm fine, don't worry about me.", "good": "I'm having a rough day, but talking to you already makes it better. Thank you for being here."},
            {"bad": "Good job.", "good": "I'm so proud of you — I saw how hard you worked on this, and it shows."},
            {"bad": "Sorry I'm late again.", "good": "I know my being late affects you. I'm working on it because I respect your time — you deserve better."},
            {"bad": "That sucks.", "good": "That sounds really hard. I'm here for you — whatever you need, even if it's just someone to listen."},
            {"bad": "Happy birthday!", "good": "Happy birthday! I'm grateful you exist — the world is better with you in it. I hope today feels as special as you are."},
        ],
        "dos": [
            "Use people's names when you talk to them — it signals care",
            "Remember details — 'How did that interview go?' shows you listened",
            "Offer help before people have to ask",
            "Be the first to forgive and the last to hold a grudge",
            "Express gratitude openly and often",
        ],
        "donts": [
            "Be so agreeable that you lose your own voice",
            "Let people take advantage of your kindness — set boundaries",
            "Be passive-aggressive when you're upset — say it directly but gently",
            "Over-apologize — save 'sorry' for when you truly mean it",
            "Forget to be kind to yourself too",
        ],
        "exercises": [
            "Send 3 people a message telling them something you appreciate about them — be specific",
            "Practice saying 'no' kindly: 'I care about you, but I can't do this right now. Let me support you another way.'",
            "Next time someone shares good news, respond with twice the enthusiasm you think is normal",
            "Do one anonymous act of kindness today — no credit, no recognition",
        ],
        "tips": [
            "Warmth in your voice can defuse almost any conflict",
            "People forget what you said but never forget how you made them feel",
            "Being kind when you're having a bad day is the highest form of strength",
        ],
    },

    "storyteller": {
        "name": "The Storyteller",
        "tagline": "Never be boring — captivate with every word",
        "icon": "🎭",
        "color": "#8b5cf6",
        "color_light": "#ede9fe",
        "description": (
            "The storyteller turns ordinary moments into adventures. "
            "It's not about being the loudest — it's about being the most "
            "engaging. Every conversation is a chance to make someone "
            "lean in and want more."
        ),
        "principles": [
            "Start with a hook — make the first sentence impossible to ignore",
            "Use the rule of three — setup, tension, payoff",
            "Show, don't tell — describe feelings, not just facts",
            "Vary your pacing — slow down for tension, speed up for excitement",
            "Bring characters to life with voices and gestures",
            "End with a punchline or a lesson — never let a story fizzle",
        ],
        "examples": [
            {"bad": "My day was okay, I went to the store.", "good": "So picture this: I walk into the store, completely confident I know what I need. 45 minutes later, I'm in an aisle I didn't know existed, holding cheese I can't pronounce, and the cashier is my high school teacher."},
            {"bad": "It was a fun trip.", "good": "The trip started normal. Then our GPS died in the middle of nowhere. And that's when we met the strangest person I've ever encountered..."},
            {"bad": "I had a crazy weekend.", "good": "I need to tell you about my weekend because I'm still processing it. It involved a goat, a misunderstanding, and a very long walk home."},
            {"bad": "Work was busy.", "good": "Today at work, three things happened that should never happen on the same day. By the third one, I was laughing so hard I had to step outside."},
            {"bad": "The movie was good.", "good": "I went in expecting nothing. An hour later, I was on the edge of my seat, forgotten popcorn in my lap, completely hooked. And the ending? I didn't see it coming from a mile away."},
        ],
        "dos": [
            "Use vivid sensory details — what did you see, hear, feel?",
            "Pause for effect before the punchline",
            "Involve your listener — 'You know that feeling when...?'",
            "Embrace the awkward — embarrassing stories are the best stories",
            "Practice on friends and watch what makes them react",
        ],
        "donts": [
            "Drag stories out past their natural endpoint",
            "Give too much unnecessary background before getting to the point",
            "Use the same tone throughout — monotone kills stories",
            "Interrupt other people's stories to tell your own",
            "Explain the moral — let the listener figure it out",
        ],
        "exercises": [
            "Turn your most boring day into a 60-second story with a hook, tension, and payoff",
            "Tell the same story three times — each time more exaggerated — and find the best version",
            "Practice starting stories with: 'The craziest thing happened...', 'You won't believe...', 'So I have a theory...'",
            "Watch a stand-up comedian and study their pacing and pauses",
        ],
        "tips": [
            "The best stories come from your most embarrassing moments — own them",
            "A well-timed pause creates more tension than any words could",
            "Details make stories believable — 'the coffee was cold' beats 'the coffee was bad'",
        ],
    },

    "diplomat": {
        "name": "The Diplomat",
        "tagline": "Be persuasive, professional, and respected",
        "icon": "🤝",
        "color": "#0ea5e9",
        "color_light": "#e0f2fe",
        "description": (
            "Diplomatic communication is the art of getting what you want "
            "while making the other person feel like they won too. It's "
            "about influence through respect, logic, and strategic empathy."
        ),
        "principles": [
            "Seek to understand before seeking to be understood",
            "Frame your asks in terms of mutual benefit",
            "Stay calm under pressure — emotion undermines logic",
            "Use 'yes, and' instead of 'no, but' to build on ideas",
            "Acknowledge opposing views before presenting yours",
            "Choose your battles — not every disagreement needs a debate",
        ],
        "examples": [
            {"bad": "That won't work.", "good": "I see where you're coming from, and I think we can build on that. What if we also considered..."},
            {"bad": "You're wrong about this.", "good": "I understand your perspective. Here's another angle to consider — what are your thoughts on this?"},
            {"bad": "I need this done now.", "good": "I know you have a lot on your plate. This one's time-sensitive though — can we figure out a way to prioritize it together?"},
            {"bad": "That's a bad idea.", "good": "Interesting approach. I'm curious — how would we handle the risk of [specific concern]?"},
            {"bad": "Do it my way.", "good": "Here's what I'm suggesting and why. But I want to hear your take — what am I missing?"},
        ],
        "dos": [
            "Use the person's name — it signals respect and attention",
            "Mirror their language subtly to build rapport",
            "Ask 'how might we...' questions to frame problems collaboratively",
            "Summarize what they said before responding — it proves you listened",
            "Offer options, not ultimatums — people resist being cornered",
        ],
        "donts": [
            "Use absolute words like 'always' or 'never' — they trigger defensiveness",
            "Win the argument but lose the relationship",
            "Dismiss concerns — even small ones matter to the person raising them",
            "Get emotional when challenged — stay composed",
            "Assume you know their motivations — ask instead",
        ],
        "exercises": [
            "Practice the 'steel man' technique: argue someone else's position better than they did, then respond",
            "Next disagreement, try saying 'You're right about X. And I'd add Y' before making your point",
            "Write an email asking for something using only collaborative language — no demands",
            "Practice summarizing someone's argument in one sentence before responding",
        ],
        "tips": [
            "The phrase 'Help me understand...' disarms defensiveness instantly",
            "People decide based on emotion and justify with logic — address both",
            "Silence after a question is powerful — don't rush to fill it",
        ],
    },
}


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    """Home page — choose a communication style."""
    return render_template("index.html", styles=STYLES)


@app.route("/learn/<style_id>")
def learn(style_id):
    """Learning page for a specific communication style."""
    style = STYLES.get(style_id)
    if not style:
        return render_template("not_found.html"), 404
    return render_template("learn.html", style=style, style_id=style_id)


@app.route("/api/quiz/<style_id>")
def quiz(style_id):
    """Generate a quick quiz question for the given style."""
    style = STYLES.get(style_id)
    if not style:
        return jsonify({"error": "Style not found"}), 404

    examples = style["examples"]
    pick = random.choice(examples)
    if random.random() > 0.5:
        return jsonify({
            "question": f"What's wrong with this way of speaking?",
            "example": pick["bad"],
            "answer": f"Here's a better version: \"{pick['good']}\"",
            "type": "fix",
        })
    else:
        return jsonify({
            "question": f"What makes this way of speaking effective?",
            "example": pick["good"],
            "answer": f"Compare with the weak version: \"{pick['bad']}\"",
            "type": "analyze",
        })


@app.route("/api/practice/<style_id>")
def practice(style_id):
    """Return a random practice exercise."""
    style = STYLES.get(style_id)
    if not style:
        return jsonify({"error": "Style not found"}), 404
    exercise = random.choice(style["exercises"])
    tip = random.choice(style["tips"])
    return jsonify({"exercise": exercise, "tip": tip})


@app.route("/health")
def health():
    return jsonify({"status": "ok", "styles": len(STYLES)})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
