"""
TalkMaster Premium — Learn to talk like anyone you want to be.

A Flask web app with a 30-day structured curriculum, audio features,
progress tracking, gamification, and a premium glassmorphism UI.

Features:
- 7 communication styles with deep content
- 30-day structured learning path with daily lessons
- Text-to-speech audio for all examples
- Progress tracking with streaks, XP, and achievement badges
- Spaced repetition review quizzes
- Dark/light theme toggle
- Smooth page transitions and animations
"""

from flask import Flask, render_template, jsonify, request
import random

app = Flask(__name__)

# ---------------------------------------------------------------------------
# Communication Style Data
# ---------------------------------------------------------------------------

STYLES = {
    "leader": {
        "name": "The Leader", "tagline": "Command the room with authority and vision",
        "icon": "👑", "color": "#6366f1", "color_light": "#e0e7ff",
        "description": "Leadership communication is about clarity, decisiveness, and inspiring others to follow. You don't need a title to lead — you need a voice that people trust.",
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
        "dos": ["Use confident body language — stand tall, make eye contact", "Pause deliberately before key points to create emphasis", "Ask powerful questions that make people think deeper", "Acknowledge mistakes openly and pivot to solutions", "Give credit to others when things go well"],
        "donts": ["Overuse filler words like 'um', 'like', 'you know'", "Apologize for having an opinion — say it with conviction", "Blame others when things go wrong", "Talk over people or dismiss their input", "Use vague language — 'maybe', 'sort of', 'I guess'"],
        "exercises": ["Record yourself giving instructions for a task, then listen back and count filler words", "Practice starting sentences with 'I believe', 'I've decided', 'Here's the plan'", "Give a 60-second pitch for a project you care about using only confident language", "Next time someone asks 'what should we do?', respond with a clear recommendation within 5 seconds"],
        "tips": ["Lower your voice slightly at the end of sentences to sound more authoritative", "Silence is a leadership tool — learn to be comfortable with pauses", "The word 'because' is powerful — always explain your reasoning"],
    },
    "charmer": {
        "name": "The Charmer", "tagline": "Be magnetic, confident, and impossible to ignore",
        "icon": "✨", "color": "#f59e0b", "color_light": "#fef3c7",
        "description": "Charisma isn't something you're born with — it's a skill. It's the art of making people feel seen, heard, and special while being unapologetically yourself.",
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
        "dos": ["Smile with your eyes — it makes people feel welcome", "Lean in slightly when someone is speaking to show genuine interest", "Use light, appropriate touch (handshake, shoulder tap) to build warmth", "Mirror the energy of the person you're talking to, then raise it slightly", "Share brief, funny personal stories to build connection"],
        "donts": ["Make everything about yourself — the spotlight should bounce back and forth", "Over-compliment to the point it feels fake", "Be overly agreeable — having opinions makes you more interesting", "Check your phone mid-conversation — it kills the magic instantly", "Try too hard — forced charm feels manipulative"],
        "exercises": ["Go to a social setting and have a conversation where you ask 3x more questions than you answer", "Practice giving 5 different people a specific, genuine compliment today", "Memorize one interesting detail about 3 people you meet and reference it later", "Tell a 30-second funny story about yourself to a stranger"],
        "tips": ["People remember how you made them feel, not what you said", "A slight head tilt while listening signals warmth and attentiveness", "Laughter shared is connection built — find the joy in conversations"],
    },
    "flirt": {
        "name": "The Flirt", "tagline": "Be playful, teasing, and irresistibly fun",
        "icon": "😏", "color": "#ec4899", "color_light": "#fce7f3",
        "description": "Flirting is playful communication that creates attraction through humor, teasing, and tension. It's not about being overt — it's about being intriguing, confident, and fun.",
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
        "dos": ["Read the room — calibrate your energy to their response", "Use playful challenges: 'I bet you can't...' or 'You seem like the type who...'", "Smile slyly — half-smiles create intrigue", "Create playful nicknames or inside references", "Be comfortable with silence — tension builds attraction"],
        "donts": ["Cross the line from playful to disrespectful — if they look uncomfortable, dial it back", "Be too available — mystery is attractive", "Use crude or overly sexual language too early", "Compliment appearance too much — compliment personality and vibe instead", "Force it — if the banter isn't flowing, just be genuine"],
        "exercises": ["Practice playful teasing with a friend — say something cheeky, then immediately smile to soften it", "Write 5 playful responses to common compliments and practice delivering them naturally", "Next conversation, try holding eye contact 2 seconds longer than usual and notice the shift", "Practice the 'takeaway' — end a fun conversation first, before it dies down"],
        "tips": ["Confidence is the foundation — flirting without confidence feels awkward", "Your tone of voice matters more than your words — slow down, lower the pitch", "Playful disagreement is more attractive than constant agreement"],
    },
    "romantic": {
        "name": "The Romantic", "tagline": "Speak from the heart with warmth and sincerity",
        "icon": "💖", "color": "#e11d48", "color_light": "#ffe4e6",
        "description": "Romantic communication is about vulnerability, sincerity, and making someone feel deeply valued. It's not grand gestures — it's the small, genuine words that land in the heart.",
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
        "dos": ["Write handwritten notes — they carry weight texts never will", "Remember small details they mention and bring them up later", "Express feelings in quiet moments — a whisper hits harder than a shout", "Be present — put the phone down and give them your full attention", "Say their name with warmth — it changes the entire tone"],
        "donts": ["Use generic lines you found online — sincerity can't be copy-pasted", "Rush the moment — let pauses breathe", "Overdo it to the point it feels performative", "Use romantic words as a transaction or to get something", "Forget that listening is just as romantic as speaking"],
        "exercises": ["Write down 5 specific things you appreciate about someone you love — be detailed", "Practice saying 'I feel [emotion] when you [specific action]' without blaming", "Leave an unexpected note for someone — no occasion needed", "Tell someone one thing you've been feeling but haven't said yet"],
        "tips": ["Eye contact during emotional words multiplies their impact", "A soft, slower tone signals sincerity — speed signals nervousness", "Sometimes the most romantic thing you can say is nothing — just hold their hand"],
    },
    "sweetheart": {
        "name": "The Sweetheart", "tagline": "Be warm, kind, and impossible not to adore",
        "icon": "🌸", "color": "#14b8a6", "color_light": "#ccfbf1",
        "description": "Being a sweetheart is about genuine warmth that makes people feel safe and valued around you. It's not about being a pushover — it's about kindness that comes from strength.",
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
        "dos": ["Use people's names when you talk to them — it signals care", "Remember details — 'How did that interview go?' shows you listened", "Offer help before people have to ask", "Be the first to forgive and the last to hold a grudge", "Express gratitude openly and often"],
        "donts": ["Be so agreeable that you lose your own voice", "Let people take advantage of your kindness — set boundaries", "Be passive-aggressive when you're upset — say it directly but gently", "Over-apologize — save 'sorry' for when you truly mean it", "Forget to be kind to yourself too"],
        "exercises": ["Send 3 people a message telling them something you appreciate about them — be specific", "Practice saying 'no' kindly: 'I care about you, but I can't do this right now. Let me support you another way.'", "Next time someone shares good news, respond with twice the enthusiasm you think is normal", "Do one anonymous act of kindness today — no credit, no recognition"],
        "tips": ["Warmth in your voice can defuse almost any conflict", "People forget what you said but never forget how you made them feel", "Being kind when you're having a bad day is the highest form of strength"],
    },
    "storyteller": {
        "name": "The Storyteller", "tagline": "Never be boring — captivate with every word",
        "icon": "🎭", "color": "#8b5cf6", "color_light": "#ede9fe",
        "description": "The storyteller turns ordinary moments into adventures. It's not about being the loudest — it's about being the most engaging. Every conversation is a chance to make someone lean in and want more.",
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
        "dos": ["Use vivid sensory details — what did you see, hear, feel?", "Pause for effect before the punchline", "Involve your listener — 'You know that feeling when...?'", "Embrace the awkward — embarrassing stories are the best stories", "Practice on friends and watch what makes them react"],
        "donts": ["Drag stories out past their natural endpoint", "Give too much unnecessary background before getting to the point", "Use the same tone throughout — monotone kills stories", "Interrupt other people's stories to tell your own", "Explain the moral — let the listener figure it out"],
        "exercises": ["Turn your most boring day into a 60-second story with a hook, tension, and payoff", "Tell the same story three times — each time more exaggerated — and find the best version", "Practice starting stories with: 'The craziest thing happened...', 'You won't believe...', 'So I have a theory...'", "Watch a stand-up comedian and study their pacing and pauses"],
        "tips": ["The best stories come from your most embarrassing moments — own them", "A well-timed pause creates more tension than any words could", "Details make stories believable — 'the coffee was cold' beats 'the coffee was bad'"],
    },
    "diplomat": {
        "name": "The Diplomat", "tagline": "Be persuasive, professional, and respected",
        "icon": "🤝", "color": "#0ea5e9", "color_light": "#e0f2fe",
        "description": "Diplomatic communication is the art of getting what you want while making the other person feel like they won too. It's about influence through respect, logic, and strategic empathy.",
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
        "dos": ["Use the person's name — it signals respect and attention", "Mirror their language subtly to build rapport", "Ask 'how might we...' questions to frame problems collaboratively", "Summarize what they said before responding — it proves you listened", "Offer options, not ultimatums — people resist being cornered"],
        "donts": ["Use absolute words like 'always' or 'never' — they trigger defensiveness", "Win the argument but lose the relationship", "Dismiss concerns — even small ones matter to the person raising them", "Get emotional when challenged — stay composed", "Assume you know their motivations — ask instead"],
        "exercises": ["Practice the 'steel man' technique: argue someone else's position better than they did, then respond", "Next disagreement, try saying 'You're right about X. And I'd add Y' before making your point", "Write an email asking for something using only collaborative language — no demands", "Practice summarizing someone's argument in one sentence before responding"],
        "tips": ["The phrase 'Help me understand...' disarms defensiveness instantly", "People decide based on emotion and justify with logic — address both", "Silence after a question is powerful — don't rush to fill it"],
    },
}

# ---------------------------------------------------------------------------
# 30-Day Curriculum
# ---------------------------------------------------------------------------

CURRICULUM = [
    # Week 1: Foundations
    {"day": 1, "week": 1, "title": "Welcome to TalkMaster", "style": None, "type": "intro",
     "duration": "5 min", "xp": 50,
     "lesson": "Communication is the most powerful skill you can develop. It affects your career, your relationships, your confidence, and your ability to influence the world around you. Over the next 30 days, you'll learn 7 distinct communication styles — from leadership to charm, from romance to diplomacy. Each style is a tool. The mastery is knowing which to use, when, and how to switch between them seamlessly. Today is simple: explore the styles, pick the one that excites you most, and get ready to transform how you speak.",
     "key_takeaway": "Communication is a learnable skill, not an innate talent. Every great communicator was once a beginner.",
     "exercise": "Browse all 7 communication styles. Which one excites you most? Which one scares you? Write down both.",
     "reflection": "What's one conversation you wish you'd handled differently? Keep this in mind as you learn.",
     "quiz": {"question": "What's the most important factor in becoming a great communicator?", "options": ["Natural talent", "Consistent practice over time", "Having a large vocabulary", "Being extroverted"], "answer": 1, "explanation": "Research consistently shows that communication is a skill built through deliberate practice, not an innate talent. Even naturally shy people can become exceptional communicators."}},

    {"day": 2, "week": 1, "title": "The Leader: Principles of Authority", "style": "leader", "type": "learn",
     "duration": "8 min", "xp": 75,
     "lesson": "Leadership communication is about three things: clarity, decisiveness, and vision. Leaders don't hedge — they commit. They don't say 'maybe we should' — they say 'here's the plan.' But true leadership communication isn't about being bossy; it's about being so clear and confident that people naturally want to follow. The key shift: replace uncertainty with conviction, replace blame with responsibility, and replace vagueness with specificity. When you speak like a leader, you don't need a title — people will look to you naturally.",
     "key_takeaway": "Leaders speak in certainties, take responsibility for outcomes, and paint a vision others want to join.",
     "exercise": "Write down 3 sentences you say regularly that hedge or deflect. Rewrite each one with leader-level conviction.",
     "reflection": "Think of a leader you admire. What specific words or phrases do they use that make you trust them?",
     "quiz": {"question": "Which sentence sounds most like a leader?", "options": ["I think maybe we should try this", "I guess this could work if we're lucky", "Here's the plan. We go with this approach because it gives us the best shot", "I don't know, what do you want to do?"], "answer": 2, "explanation": "A leader commits to a direction, explains the reasoning, and moves forward. The other options all hedge responsibility and signal uncertainty."}},

    {"day": 3, "week": 1, "title": "The Leader: Practice & Examples", "style": "leader", "type": "practice",
     "duration": "10 min", "xp": 100,
     "lesson": "Today we put leadership communication into practice. The key technique is the 'commitment shift' — taking any wishy-washy statement and rewriting it with authority. Notice the pattern: weak statements use qualifiers (maybe, probably, I guess), while strong statements use commitments (I will, here's the plan, I recommend). Practice saying each example aloud — your voice should drop slightly at the end of a sentence to signal authority, not rise like a question.",
     "key_takeaway": "Authority comes from commitment language: 'I will,' 'Here's the plan,' 'I recommend.' Eliminate hedging words.",
     "exercise": "Stand in front of a mirror and say each 'good' example aloud. Pay attention to your posture — stand tall, shoulders back, chin level. Record yourself if possible and listen back.",
     "reflection": "How did it feel to speak with authority? Did it feel natural or forced? What would make it feel more natural?",
     "quiz": {"question": "What's a common mistake people make when trying to sound authoritative?", "options": ["Using too much eye contact", "Raising their voice at the end of sentences (uptalk)", "Speaking too slowly", "Using the word 'because'"], "answer": 1, "explanation": "Uptalk — raising your pitch at the end of a sentence — turns a statement into a question and signals uncertainty. Leaders lower their voice at the end to signal confidence."}},

    {"day": 4, "week": 1, "title": "The Charmer: Principles of Magnetism", "style": "charmer", "type": "learn",
     "duration": "8 min", "xp": 75,
     "lesson": "Charisma is not a personality trait — it's a set of behaviors that anyone can learn. The core principle: make people feel like they're the most interesting person in the room. Charmers are genuinely curious, remember details, use humor (especially self-deprecating), and make people feel seen. The secret weapon? Specificity. 'I love how you phrased that' beats 'you're great' every time. Specific compliments show you're actually paying attention, not just going through the motions.",
     "key_takeaway": "Charm = genuine curiosity + specific compliments + making people feel seen. It's about them, not you.",
     "exercise": "Write 5 specific, genuine compliments for 5 different people in your life. Be specific — mention exactly what they did and why it impressed you.",
     "reflection": "Who's the most charming person you know? What do they do that makes you feel special around them?",
     "quiz": {"question": "Which compliment is more charming and why?", "options": ["'You're really great' — it's simple and direct", "'You're really great' — it works for anyone", "'I love how you handled that question — you thought two steps ahead' — it's specific and shows genuine attention", "'You look nice' — it's a classic"], "answer": 2, "explanation": "Specific compliments prove you're actually paying attention. Generic compliments could apply to anyone, which makes them feel less sincere."}},

    {"day": 5, "week": 1, "title": "The Charmer: Practice & Examples", "style": "charmer", "type": "practice",
     "duration": "10 min", "xp": 100,
     "lesson": "Today we practice charm techniques. The key exercise is the 'curiosity ratio' — aim to ask 3 questions for every 1 thing you share about yourself. This flips the normal conversation dynamic and makes people feel fascinating. Also practice the 'energy mirror' — match the other person's energy level, then raise it slightly. If they're calm, be slightly more animated. If they're excited, match and exceed their enthusiasm. Listen to the examples and notice how charmers redirect attention to the other person.",
     "key_takeaway": "The curiosity ratio (3 questions per 1 personal share) makes people feel fascinating and builds instant connection.",
     "exercise": "In your next conversation, count your questions vs. statements. Aim for 3:1. Notice how the other person opens up when you show genuine curiosity.",
     "reflection": "How hard was it to ask more questions than you answered? What did you learn about the other person that you wouldn't have otherwise?",
     "quiz": {"question": "What's the 'energy mirror' technique?", "options": ["Copy the person's exact words back to them", "Match their energy level, then raise it slightly", "Mirror their body posture exactly", "Repeat their last sentence as a question"], "answer": 1, "explanation": "Matching energy builds rapport because people feel understood. Raising it slightly elevates the conversation without jarring them."}},

    {"day": 6, "week": 1, "title": "Week 1 Review: Leader & Charmer", "style": None, "type": "review",
     "duration": "8 min", "xp": 125,
     "lesson": "This week you learned two powerful styles. The Leader teaches you to speak with authority — replacing hedging with commitment, blame with responsibility. The Charmer teaches you to make people feel seen — through curiosity, specific compliments, and genuine warmth. These two complement each other: leadership gives you authority, charm gives you warmth. Together, they make you someone people respect AND like. The best communicators blend both.",
     "key_takeaway": "Leadership = authority + vision. Charm = curiosity + specificity. Together they create respected warmth.",
     "exercise": "Write a short paragraph (3-4 sentences) that demonstrates BOTH leader and charmer qualities. Start with a clear recommendation (leader), then build connection through a specific compliment (charmer).",
     "reflection": "Which style felt more natural — Leader or Charmer? Which one do you need to work on more? Why?",
     "quiz": {"question": "What's the best way to combine leadership and charm?", "options": ["Be commanding first, then warm", "Give a clear recommendation, then build connection with a specific compliment", "Always be charming, never authoritative", "Be authoritative to some people and charming to others"], "answer": 1, "explanation": "Starting with a clear recommendation establishes authority, and following with a specific compliment builds warmth. This combination creates 'respected warmth' — the sweet spot."}},

    {"day": 7, "week": 1, "title": "Reflection & Journaling", "style": None, "type": "reflection",
     "duration": "5 min", "xp": 50,
     "lesson": "Reflection is where learning becomes permanent. Research shows that people who reflect on what they've learned retain up to 50% more than those who don't. Today, take 5 minutes to write down what you've learned this week. What surprised you? What challenged you? What will you try differently tomorrow? The act of writing cements knowledge and reveals patterns you might miss otherwise.",
     "key_takeaway": "Reflection converts experience into learning. Writing about what you learned increases retention by up to 50%.",
     "exercise": "Write a journal entry (at least 5 sentences) answering: What did I learn about communication this week? What will I do differently?",
     "reflection": "What pattern did you notice in your communication this week? What's one small change you can commit to for next week?",
     "quiz": {"question": "Why is reflection important for learning?", "options": ["It's not — practice is enough", "It converts experience into permanent learning and reveals patterns", "It helps you memorize vocabulary", "It's only useful for extroverts"], "answer": 1, "explanation": "Studies show that reflection converts raw experience into structured learning. Without it, lessons fade quickly even with extensive practice."}},

    # Week 2: Emotional Connection
    {"day": 8, "week": 2, "title": "The Flirt: Principles of Playfulness", "style": "flirt", "type": "learn",
     "duration": "8 min", "xp": 75,
     "lesson": "Flirting is the art of creating playful tension. It's not about being overt or sexual — it's about being intriguing, unpredictable, and fun. The core technique is 'push-pull': show interest, then playfully pull back. 'I haven't decided if I like you yet, but you're definitely growing on me.' This creates tension and keeps the other person engaged. The key ingredients: confidence (you can't flirt if you're unsure of yourself), playfulness (it should feel like a game, not a strategy), and reading the room (always calibrate to their response).",
     "key_takeaway": "Flirting = push-pull (show interest, then playfully retreat) + confidence + playfulness. It's a game, not a strategy.",
     "exercise": "Write 3 playful responses to the compliment 'You're really attractive.' Aim for responses that are teasing, confident, and fun — not crude or overly eager.",
     "reflection": "What makes flirting feel natural vs. forced? Think of a time someone flirted with you well — what did they do differently?",
     "quiz": {"question": "What is 'push-pull' in flirting?", "options": ["Pushing the person away physically", "Showing interest, then playfully pulling back to create tension", "Being mean, then being nice", "Asking lots of questions"], "answer": 1, "explanation": "Push-pull creates dynamic tension — you show interest (pull), then playfully retreat (push). This keeps the interaction engaging and unpredictable."}},

    {"day": 9, "week": 2, "title": "The Flirt: Practice & Examples", "style": "flirt", "type": "practice",
     "duration": "10 min", "xp": 100,
     "lesson": "Today we practice flirting techniques. The key exercise is 'playful reframing' — taking a boring statement and making it provocative. 'We should hang out sometime' becomes 'I'm going to take you to the best coffee place in town. Non-negotiable.' Notice the shift: passive becomes active, uncertain becomes confident, boring becomes fun. Practice saying each example aloud with a slight smile. Your tone should be relaxed, your pace slightly slower than normal. Remember: the goal is to make them smile, not uncomfortable. If they're not smiling, dial it back.",
     "key_takeaway": "Playful reframing turns boring statements into engaging ones: passive to active, uncertain to confident, boring to fun.",
     "exercise": "Take 5 boring statements (like 'Nice weather today' or 'What do you do?') and rewrite each as a playful, flirtatious version. Practice saying them aloud with a smile.",
     "reflection": "How did playful reframing change the energy of the statements? Which ones felt natural and which felt forced?",
     "quiz": {"question": "What's the most important rule when flirting?", "options": ["Always be the loudest person", "Read the room — calibrate to their response and dial back if they seem uncomfortable", "Never show genuine interest", "Use as many compliments as possible"], "answer": 1, "explanation": "Reading the room is essential. Flirting only works when both people are having fun. If the other person isn't smiling or seems uncomfortable, dial it back immediately."}},

    {"day": 10, "week": 2, "title": "The Romantic: Principles of Sincerity", "style": "romantic", "type": "learn",
     "duration": "8 min", "xp": 75,
     "lesson": "Romantic communication is about vulnerability and specificity. The mistake most people make: they use generic phrases ('I love you', 'you're special') when what moves people is specific, observed details. 'I love the way your whole face lights up when you talk about something you care about' is 100x more powerful than 'I love you' because it shows you're paying attention. The key principle: be specific about what you love. Details demonstrate that you truly see the other person, not just the idea of them.",
     "key_takeaway": "Specificity is the soul of romance. 'I love how you [specific detail]' is infinitely more powerful than 'I love you.'",
     "exercise": "Write down 5 specific things you love about someone in your life. Be detailed — not 'your smile' but 'the way your eyes crinkle when you laugh at your own jokes.'",
     "reflection": "When was the last time someone said something specific and romantic to you? How did it make you feel compared to a generic compliment?",
     "quiz": {"question": "Why is specificity more romantic than generic compliments?", "options": ["It uses more words", "It shows you truly see and pay attention to the person, not just the idea of them", "It's more poetic", "Generic compliments are always fake"], "answer": 1, "explanation": "Specific compliments prove you're paying attention to who they really are, not just projecting an idea onto them. This creates genuine emotional intimacy."}},

    {"day": 11, "week": 2, "title": "The Romantic: Practice & Examples", "style": "romantic", "type": "practice",
     "duration": "10 min", "xp": 100,
     "lesson": "Today we practice romantic communication. The key technique is the 'specificity upgrade' — taking any generic romantic statement and making it specific. 'I love you' becomes 'I love the way your whole face lights up when you talk about something you care about.' 'You look nice' becomes 'There's something about the way you look right now — it's the energy, it stops me for a second.' The pattern: always add the specific detail that shows WHY you feel what you feel. Practice saying these aloud — your tone should be soft, sincere, and slightly slower than normal.",
     "key_takeaway": "The 'specificity upgrade' transforms generic statements into powerful ones by adding the WHY behind your feelings.",
     "exercise": "Take 5 generic romantic phrases and 'upgrade' each one with specific details. Practice saying them aloud with a soft, sincere tone.",
     "reflection": "How did adding specificity change the emotional weight of each statement? Which upgrade felt most powerful to you?",
     "quiz": {"question": "What's the 'specificity upgrade'?", "options": ["Adding more adjectives to a sentence", "Adding specific details that show WHY you feel what you feel", "Making sentences longer", "Using poetic language"], "answer": 1, "explanation": "The specificity upgrade adds the 'why' — the specific detail that demonstrates genuine attention. 'I love you' + why = a powerful romantic statement."}},

    {"day": 12, "week": 2, "title": "Week 2 Review: Flirt & Romantic", "style": None, "type": "review",
     "duration": "8 min", "xp": 125,
     "lesson": "This week you learned two emotionally powerful styles. The Flirt creates attraction through playfulness, tension, and push-pull dynamics. The Romantic creates depth through vulnerability, specificity, and sincerity. These two styles represent different forms of emotional connection: flirtation creates spark, romance creates depth. The best communicators know when to spark and when to deepen. Use flirting early in an interaction to build attraction, and romantic communication once trust is established to create lasting emotional bonds.",
     "key_takeaway": "Flirting creates spark (attraction through playfulness). Romance creates depth (connection through specificity). Use both at the right time.",
     "exercise": "Write a conversation (5-6 lines) that starts with playful flirting and transitions into something more romantic and sincere. Notice how the shift feels.",
     "reflection": "Which felt more natural — flirting or romantic communication? Which one do you want to develop further?",
     "quiz": {"question": "What's the right order for flirt and romantic communication?", "options": ["Always romantic first, then flirt", "Flirt early to build attraction, then romantic communication once trust is established", "Only use one, never both", "It doesn't matter — use them randomly"], "answer": 1, "explanation": "Flirting creates initial attraction and interest. Once a connection is established, romantic communication deepens it. Using them in this order creates a natural emotional progression."}},

    {"day": 13, "week": 2, "title": "Combining Styles: Emotional Intelligence", "style": None, "type": "integration",
     "duration": "8 min", "xp": 100,
     "lesson": "Today we start combining styles. The most emotionally intelligent communicators don't stick to one style — they blend them based on the situation. Leader + Charmer = respected warmth (authoritative but likable). Flirt + Romantic = magnetic depth (fun but sincere). The key skill is 'style switching' — reading the room and shifting your communication approach in real time. If someone's stressed, switch from playful to sincere. If someone's disengaged, switch from formal to charming. This adaptability is what separates good communicators from great ones.",
     "key_takeaway": "Emotional intelligence in communication = knowing which style to use, when to switch, and how to blend them seamlessly.",
     "exercise": "Think of 3 different people in your life (a boss, a friend, a romantic partner). Which style blend would work best for each? Write down your choices.",
     "reflection": "Which style blend feels most natural to you? Which blend would be most challenging?",
     "quiz": {"question": "What is 'style switching'?", "options": ["Changing your outfit", "Reading the room and shifting your communication style in real time", "Talking in different languages", "Using different voices for different people"], "answer": 1, "explanation": "Style switching is the ability to read social cues and adapt your communication style — from formal to casual, from playful to sincere — based on what the situation demands."}},

    {"day": 14, "week": 2, "title": "Reflection & Journaling", "style": None, "type": "reflection",
     "duration": "5 min", "xp": 50,
     "lesson": "Two weeks in. You've now learned 4 of 7 styles: Leader, Charmer, Flirt, and Romantic. Take a moment to reflect on your progress. Which style has had the biggest impact on how you communicate? Which one challenged you the most? The act of journaling about your experience helps consolidate learning and reveals patterns. Research shows that learners who journal about their progress are 25% more likely to complete a learning program.",
     "key_takeaway": "You're halfway through the core styles. Journaling about your experience increases completion rates by 25%.",
     "exercise": "Write a journal entry answering: Which style changed how I communicate the most? What do I want to focus on for week 3?",
     "reflection": "What communication habit have you changed in the past 2 weeks? What habit do you still want to change?",
     "quiz": {"question": "What's the benefit of journaling about your learning?", "options": ["It's just busywork", "It consolidates learning and reveals patterns, increasing completion rates by 25%", "It helps you memorize facts", "It's only useful for writers"], "answer": 1, "explanation": "Journaling converts scattered experiences into structured insights. Learners who reflect and journal are significantly more likely to complete their learning journey."}},

    # Week 3: Advanced Expression
    {"day": 15, "week": 3, "title": "The Sweetheart: Principles of Warmth", "style": "sweetheart", "type": "learn",
     "duration": "8 min", "xp": 75,
     "lesson": "Being a sweetheart is about genuine warmth that makes people feel safe around you. It's NOT about being a pushover — it's kindness that comes from strength. The key principle: 'warmth + boundaries = irresistible.' Sweethearts remember details, check in on people, celebrate others' wins, and make people feel safe to be themselves. The secret weapon: enthusiastic celebration. When someone shares good news, respond with twice the enthusiasm you think is normal. This creates deep emotional bonds because most people under-respond to others' good news.",
     "key_takeaway": "Warmth + boundaries = irresistible. Enthusiastic celebration of others' wins creates deep emotional bonds.",
     "exercise": "Think of someone who shared good news with you recently. Write down how you responded, then rewrite it with 2x the enthusiasm. Send the upgraded version.",
     "reflection": "When was the last time someone made you feel truly safe to be yourself? What did they do that created that safety?",
     "quiz": {"question": "What's the formula for being a sweetheart without being a pushover?", "options": ["Warmth only", "Boundaries only", "Warmth + boundaries", "Agreeing with everything"], "answer": 2, "explanation": "Warmth without boundaries makes you a pushover. Boundaries without warmth make you cold. Together, they create strength-based kindness that people respect and adore."}},

    {"day": 16, "week": 3, "title": "The Sweetheart: Practice & Examples", "style": "sweetheart", "type": "practice",
     "duration": "10 min", "xp": 100,
     "lesson": "Today we practice sweetheart techniques. The key exercise is 'active celebration' — when someone shares something good, don't just say 'nice' or 'cool.' Say 'I'm SO proud of you — I saw how hard you worked on this, and it shows.' The pattern: acknowledge the effort, not just the outcome. Also practice 'kind no' — saying no with warmth: 'I care about you, but I can't do this right now. Let me support you another way.' This maintains the relationship while setting a boundary. Practice saying each example aloud with genuine warmth in your voice.",
     "key_takeaway": "Active celebration acknowledges effort, not just outcomes. 'Kind no' maintains warmth while setting boundaries.",
     "exercise": "Practice saying a 'kind no' to 3 different requests. Use the pattern: 'I care about you, but I can't do this right now. Let me support you another way.'",
     "reflection": "How did it feel to say no kindly? Was it harder or easier than you expected?",
     "quiz": {"question": "What's the key to a 'kind no'?", "options": ["Apologize profusely", "Acknowledge the relationship, state the boundary, offer an alternative way to support", "Just say no firmly", "Say yes but don't follow through"], "answer": 1, "explanation": "A kind no has three parts: affirming the relationship, clearly stating the boundary, and offering an alternative. This preserves warmth while being honest."}},

    {"day": 17, "week": 3, "title": "The Storyteller: Principles of Captivation", "style": "storyteller", "type": "learn",
     "duration": "8 min", "xp": 75,
     "lesson": "The storyteller turns ordinary moments into adventures. The core principle: start with a hook that's impossible to ignore. 'So picture this...' beats 'My day was okay...' every time. Use the rule of three: setup, tension, payoff. Show, don't tell — describe feelings, not just facts. Vary your pacing: slow down for tension, speed up for excitement. And most importantly: end with a punchline or a lesson. Never let a story fizzle out. The best storytellers make mundane experiences feel cinematic by focusing on the unexpected, the embarrassing, and the specific.",
     "key_takeaway": "Every story needs: a hook (impossible to ignore first line), the rule of three (setup, tension, payoff), and a punchline ending.",
     "exercise": "Take the most boring thing that happened to you today and turn it into a 60-second story with a hook, tension, and a payoff.",
     "reflection": "Who's the best storyteller you know? What makes their stories so engaging? What techniques can you borrow from them?",
     "quiz": {"question": "What's the 'rule of three' in storytelling?", "options": ["Tell three stories in a row", "Setup, tension, payoff — the three-act structure", "Use three characters", "Speak for three minutes maximum"], "answer": 1, "explanation": "The rule of three is the three-act structure: setup (establish the scene), tension (introduce conflict or surprise), and payoff (the resolution or punchline)."}},

    {"day": 18, "week": 3, "title": "The Storyteller: Practice & Examples", "style": "storyteller", "type": "practice",
     "duration": "10 min", "xp": 100,
     "lesson": "Today we practice storytelling. The key technique is 'sensory specificity' — adding vivid details that make stories believable. 'The coffee was cold' beats 'the coffee was bad.' 'I was holding cheese I can't pronounce' beats 'I was confused.' Also practice the 'pause for effect' — before the punchline, pause for 1-2 seconds. This creates anticipation and makes the payoff land harder. Listen to the examples and notice how the storyteller uses specific, vivid details to paint a picture that makes you lean in.",
     "key_takeaway": "Sensory specificity (vivid, specific details) makes stories believable and engaging. Pauses before punchlines create anticipation.",
     "exercise": "Tell a story about something embarrassing that happened to you. Use at least 3 specific sensory details. Practice pausing before the punchline.",
     "reflection": "How did adding specific details change the story? Did the pause before the punchline feel natural or awkward?",
     "quiz": {"question": "Why does 'the coffee was cold' beat 'the coffee was bad'?", "options": ["It uses fewer words", "It's a specific sensory detail that the listener can feel and imagine", "It's more grammatically correct", "Cold coffee is worse than bad coffee"], "answer": 1, "explanation": "Specific sensory details engage the listener's imagination. They can feel 'cold' coffee. 'Bad' is abstract and forgettable. Sensory details make stories vivid and memorable."}},

    {"day": 19, "week": 3, "title": "Week 3 Review: Sweetheart & Storyteller", "style": None, "type": "review",
     "duration": "8 min", "xp": 125,
     "lesson": "This week you learned two styles that make people love being around you. The Sweetheart creates safety and warmth through active celebration, kind boundaries, and genuine care. The Storyteller creates engagement through hooks, sensory specificity, and well-timed pauses. Together, they make you someone people never want to stop talking to — you're both safe (sweetheart) and exciting (storyteller). This combination is rare and magnetic. Most people are either warm but boring, or exciting but exhausting. Being both is the sweet spot.",
     "key_takeaway": "Sweetheart (safety + warmth) + Storyteller (engagement + excitement) = someone people never want to stop talking to.",
     "exercise": "Tell a story that also demonstrates sweetheart qualities — celebrate someone in the story, show genuine care, and use vivid, engaging details.",
     "reflection": "Which style from this week resonated more with you? How can you combine warmth with engagement in your daily conversations?",
     "quiz": {"question": "Why is the combination of Sweetheart + Storyteller so powerful?", "options": ["It's not — they conflict", "Most people are either warm but boring, or exciting but exhausting. Being both is rare and magnetic", "It uses two styles at once which saves time", "It works for all audiences"], "answer": 1, "explanation": "Warmth without engagement is boring. Engagement without warmth is exhausting. Combining both creates a rare dynamic that makes people feel both safe and captivated."}},

    {"day": 20, "week": 3, "title": "The Diplomat: Principles of Persuasion", "style": "diplomat", "type": "learn",
     "duration": "8 min", "xp": 75,
     "lesson": "Diplomatic communication is the art of getting what you want while making the other person feel like they won too. The core principle: seek to understand before seeking to be understood. The key technique is the 'yes-and pivot' — instead of saying 'no, but' (which triggers defensiveness), say 'yes, and' (which builds on their idea). Also master the phrase 'Help me understand...' — it disarms defensiveness instantly because it positions you as a learner, not an opponent. Frame your asks in terms of mutual benefit, stay calm under pressure, and always offer options, not ultimatums.",
     "key_takeaway": "Diplomacy = seek to understand first + 'yes-and' instead of 'no-but' + frame asks as mutual benefit + offer options, not ultimatums.",
     "exercise": "Think of a recent disagreement. Rewrite your side using 'yes-and' language and the 'help me understand' technique.",
     "reflection": "When was the last time you won an argument but lost the relationship? How could diplomatic communication have changed the outcome?",
     "quiz": {"question": "Why is 'yes, and' more effective than 'no, but'?", "options": ["It's more polite", "It builds on the other person's idea instead of rejecting it, preventing defensiveness", "It uses fewer words", "It's grammatically superior"], "answer": 1, "explanation": "'No, but' immediately signals opposition and triggers defensiveness. 'Yes, and' acknowledges their point and builds on it, keeping the conversation collaborative instead of confrontational."}},

    {"day": 21, "week": 3, "title": "The Diplomat: Practice & Examples", "style": "diplomat", "type": "practice",
     "duration": "10 min", "xp": 100,
     "lesson": "Today we practice diplomatic techniques. The key exercise is the 'collaborative reframe' — taking any demand and making it collaborative. 'I need this done now' becomes 'I know you have a lot on your plate. This one's time-sensitive though — can we figure out a way to prioritize it together?' Notice the pattern: acknowledge their situation, state the need, frame it as a joint problem. Also practice the 'steel man' technique: argue the other person's position better than they did, then respond. This proves you understand them and makes your counter-argument much more powerful.",
     "key_takeaway": "The collaborative reframe: acknowledge their situation + state the need + frame as joint problem. The steel man: argue their side better than they did.",
     "exercise": "Write a diplomatic email asking for something you need. Use only collaborative language — no demands, no ultimatums, only 'how might we' and 'can we figure out' framing.",
     "reflection": "How did reframing demands as collaborative questions change the tone? Did it feel more or less effective?",
     "quiz": {"question": "What's the 'steel man' technique?", "options": ["Be tough and unyielding", "Argue the other person's position better than they did, then respond", "Use iron-clad logic", "Never compromise"], "answer": 1, "explanation": "The steel man is the opposite of a straw man. Instead of misrepresenting their argument, you present it in its strongest form. This proves you understand them and makes your response more credible."}},

    # Week 4: Mastery & Integration
    {"day": 22, "week": 4, "title": "Diplomat Review & Advanced Persuasion", "style": "diplomat", "type": "review",
     "duration": "8 min", "xp": 125,
     "lesson": "You've now learned all 7 styles. The Diplomat is the most nuanced — it requires emotional regulation, strategic empathy, and the ability to hold opposing views without getting triggered. Advanced persuasion involves understanding that people decide based on emotion and justify with logic. So address both: lead with the emotional benefit ('This will make your team's life easier'), then back it with logic ('because it reduces processing time by 40%'). Also master silence — after asking a question, don't rush to fill the silence. Let them process and respond. Silence is one of the most powerful tools in diplomatic communication.",
     "key_takeaway": "People decide with emotion and justify with logic — address both. Silence after a question is a powerful diplomatic tool.",
     "exercise": "Practice the 'emotional-then-logical' structure: make a request that starts with the emotional benefit, then supports it with logic. Do this for 3 different scenarios.",
     "reflection": "Which diplomatic technique was hardest for you to practice? What would make it easier?",
     "quiz": {"question": "How should you structure a persuasive argument?", "options": ["Logic only — facts speak for themselves", "Emotion only — feelings drive action", "Lead with the emotional benefit, then support with logic — because people decide with emotion and justify with logic", "Alternate between emotion and logic"], "answer": 2, "explanation": "Research shows people make decisions emotionally and then rationalize them logically. Addressing both — leading with emotion, supporting with logic — is the most effective persuasion structure."}},

    {"day": 23, "week": 4, "title": "Style Switching: Reading the Room", "style": None, "type": "integration",
     "duration": "8 min", "xp": 100,
     "lesson": "Today we master the most advanced skill: style switching. This is the ability to read a situation and shift your communication style in real time. In a job interview? Blend Leader + Diplomat. On a first date? Blend Charmer + Flirt. Comforting a friend? Switch to Sweetheart. Giving a toast? Storyteller mode. The key is calibration — paying attention to the other person's energy, mood, and needs, then matching your style accordingly. Practice this: in your next conversation, ask yourself 'what does this person need right now?' before you speak. Authority? Warmth? Playfulness? Sincerity? Choose accordingly.",
     "key_takeaway": "Style switching = reading the room + asking 'what does this person need?' + choosing the right style blend for the moment.",
     "exercise": "For each of these scenarios, write down which style blend you'd use: a job interview, a first date, comforting a stressed friend, giving a wedding toast, negotiating a raise.",
     "reflection": "Which style switch is hardest for you? Going from playful to serious? From authoritative to warm? Why?",
     "quiz": {"question": "What's the first step in style switching?", "options": ["Talk louder", "Ask yourself 'what does this person need right now?' and choose your style accordingly", "Mirror their body language exactly", "Wait for them to speak first"], "answer": 1, "explanation": "Before you speak, assess what the other person needs — authority, warmth, playfulness, or sincerity. This assessment drives your style choice and makes your communication feel naturally calibrated."}},

    {"day": 24, "week": 4, "title": "Real-World Scenarios", "style": None, "type": "practice",
     "duration": "10 min", "xp": 125,
     "lesson": "Today we apply everything to real-world scenarios. Scenario 1: Your boss criticizes your work. (Diplomat + Leader — acknowledge their perspective, take responsibility, present a solution). Scenario 2: You're at a party where you know no one. (Charmer + Storyteller — be curious, share engaging stories). Scenario 3: Your partner is upset with you. (Sweetheart + Romantic — listen actively, validate their feelings, be specific about what you appreciate). Scenario 4: You need to say no to a friend's request. (Sweetheart boundary — 'I care about you, but I can't right now. Let me support you another way'). For each scenario, practice the specific phrases and techniques from the relevant styles.",
     "key_takeaway": "Every real-world scenario has an optimal style blend. The key is identifying the situation, then deploying the right combination of techniques.",
     "exercise": "Pick one scenario from today that you're likely to face this week. Write out exactly what you'd say, word for word. Practice it aloud.",
     "reflection": "Which scenario felt most challenging? What would make it easier?",
     "quiz": {"question": "If your boss criticizes your work, what's the best style blend?", "options": ["Leader only — defend yourself strongly", "Diplomat + Leader — acknowledge their perspective, take responsibility, present a solution", "Charmer — charm your way out of it", "Storyteller — tell a story about why it happened"], "answer": 1, "explanation": "Diplomacy helps you acknowledge their perspective without being defensive, while leadership helps you take responsibility and present a solution. This combination shows maturity and competence."}},

    {"day": 25, "week": 4, "title": "Advanced Practice: Multi-Style Conversations", "style": None, "type": "practice",
     "duration": "10 min", "xp": 150,
     "lesson": "Today we practice the hardest skill: switching styles WITHIN a single conversation. A great conversation isn't one style — it flows. Start with Charmer to build rapport, switch to Storyteller to engage, shift to Romantic to deepen, then close with Sweetheart to leave them feeling valued. The transitions should be invisible — you're not changing characters, you're adapting to the flow of the conversation. Practice this flow: open with curiosity (charmer), share a vivid story (storyteller), express something sincere (romantic), and close with warmth (sweetheart). This is what master communicators do naturally.",
     "key_takeaway": "Master communicators flow between styles within a single conversation: charm to open, story to engage, sincerity to deepen, warmth to close.",
     "exercise": "Write a 6-line conversation where you use 4 different styles in sequence: Charmer (open), Storyteller (engage), Romantic (deepen), Sweetheart (close).",
     "reflection": "Was it hard to switch styles within a single conversation? How can you make the transitions smoother?",
     "quiz": {"question": "What's the ideal style flow for a deep conversation?", "options": ["Stay in one style the whole time", "Charm to open, story to engage, sincerity to deepen, warmth to close", "Start serious, then get playful", "Use whatever style feels right randomly"], "answer": 1, "explanation": "The ideal flow builds naturally: charm opens the door, stories create engagement, romantic sincerity deepens the connection, and sweetheart warmth leaves them feeling valued. Each style builds on the previous one."}},

    {"day": 26, "week": 4, "title": "Final Quiz: All 7 Styles", "style": None, "type": "review",
     "duration": "10 min", "xp": 200,
     "lesson": "Today is your comprehensive review of all 7 styles. Leader: authority through commitment and vision. Charmer: magnetism through curiosity and specific compliments. Flirt: attraction through push-pull and playfulness. Romantic: depth through vulnerability and specificity. Sweetheart: warmth through active celebration and kind boundaries. Storyteller: engagement through hooks and sensory detail. Diplomat: persuasion through understanding and 'yes-and' pivots. You now have 7 distinct tools in your communication toolkit. Tomorrow, you'll audit your own communication and identify your strengths and growth areas.",
     "key_takeaway": "You now have 7 communication tools. The mastery is not in knowing each one, but in knowing which to use, when, and how to blend them.",
     "exercise": "Write down all 7 styles. Next to each, rate yourself 1-10 on how comfortable you are with it. Identify your top 2 strengths and bottom 2 growth areas.",
     "reflection": "Looking back at Day 1, how has your communication awareness changed? What surprised you most about yourself?",
     "quiz": {"question": "What's the true mark of a master communicator?", "options": ["Being perfect at all 7 styles", "Knowing which style to use, when, and how to blend them seamlessly", "Talking more than anyone else", "Never making mistakes"], "answer": 1, "explanation": "No one is perfect at all styles. Mastery is about adaptability — reading situations and deploying the right style or blend at the right time. Even master communicators have preferred styles; they just know when to step outside them."}},

    {"day": 27, "week": 4, "title": "Personal Communication Audit", "style": None, "type": "reflection",
     "duration": "8 min", "xp": 100,
     "lesson": "Today you audit your own communication. Think about the past week. When did you communicate well? When did you struggle? Which styles came naturally, and which required effort? The goal isn't to judge yourself — it's to build self-awareness. Research shows that self-awareness is the #1 predictor of communication improvement. People who can accurately identify their communication strengths and weaknesses improve 3x faster than those who can't. Be honest, be specific, and be kind to yourself. This is about growth, not perfection.",
     "key_takeaway": "Self-awareness is the #1 predictor of communication improvement. Honest self-audit accelerates growth 3x.",
     "exercise": "Complete this sentence 5 times: 'I communicated well when I ___.' Then complete this 5 times: 'I struggled when I ___.' Be specific.",
     "reflection": "What's the #1 communication habit you want to build next? What's the #1 habit you want to break?",
     "quiz": {"question": "What's the #1 predictor of communication improvement?", "options": ["Natural talent", "Self-awareness — the ability to accurately identify your strengths and weaknesses", "Practice hours", "Reading books about communication"], "answer": 1, "explanation": "Research shows that self-awareness predicts improvement better than any other factor. People who can accurately assess their communication are 3x more likely to improve because they know exactly what to work on."}},

    {"day": 28, "week": 4, "title": "Creating Your Communication Plan", "style": None, "type": "integration",
     "duration": "8 min", "xp": 125,
     "lesson": "Today you create a personal communication development plan. Based on your audit, identify your top 2 strengths and top 2 growth areas. For each growth area, write one specific, actionable goal. Example: 'I will practice Leader-style commitment language in my next 3 work meetings by replacing 'maybe we should' with 'I recommend.' Make your goals SMART: Specific, Measurable, Achievable, Relevant, Time-bound. Also identify your 'default style' — the one you naturally fall back on — and your 'stretch style' — the one that challenges you most. Commit to practicing your stretch style in low-stakes situations this week.",
     "key_takeaway": "A communication plan has: 2 strengths to leverage, 2 growth areas with SMART goals, a default style to be aware of, and a stretch style to practice.",
     "exercise": "Write your communication plan: 2 strengths, 2 growth areas with SMART goals, your default style, and your stretch style.",
     "reflection": "How will you hold yourself accountable to this plan? Who in your life can support you?",
     "quiz": {"question": "What makes a good communication development goal?", "options": ["It should be vague so you don't feel pressured", "It should be SMART: Specific, Measurable, Achievable, Relevant, Time-bound", "It should focus on weaknesses only", "It should be something you can do perfectly"], "answer": 1, "explanation": "SMART goals are specific enough to act on, measurable enough to track, achievable enough to stay motivated, relevant to your real life, and time-bound so they don't drift. Vague goals like 'communicate better' rarely lead to change."}},

    {"day": 29, "week": 4, "title": "Final Practice Session", "style": None, "type": "practice",
     "duration": "10 min", "xp": 150,
     "lesson": "This is your final practice session. We'll simulate a complex social scenario where you need to use multiple styles. Imagine: You're at a networking event. You approach someone you want to impress. You need to introduce yourself (Charmer), share what you do in an engaging way (Storyteller), navigate a disagreement about your field (Diplomat), express genuine appreciation for their perspective (Sweetheart), and close with something memorable (Leader). Walk through this scenario step by step. Write out what you'd say at each stage. Then practice the whole flow aloud. This is the integration test — everything you've learned in one conversation.",
     "key_takeaway": "The integration test: can you flow through 5 styles in a single conversation? This is what master communicators do.",
     "exercise": "Write and practice aloud the networking scenario: Charmer (intro), Storyteller (what you do), Diplomat (disagreement), Sweetheart (appreciation), Leader (close).",
     "reflection": "Did the flow feel natural? Which transition was hardest? What would you do differently in a real situation?",
     "quiz": {"question": "What's the purpose of the final practice session?", "options": ["To memorize all 7 styles", "To test your ability to integrate multiple styles into a single, natural conversation", "To find your favorite style", "To pass a test"], "answer": 1, "explanation": "The goal isn't memorization — it's integration. Can you flow naturally between styles in a real conversation? This is what separates knowing about communication from being a master communicator."}},

    {"day": 30, "week": 4, "title": "Graduation & Next Steps", "style": None, "type": "graduation",
     "duration": "5 min", "xp": 300,
     "lesson": "Congratulations. You've completed 30 days of communication training. You've learned 7 distinct styles, practiced each one, learned to blend them, and created a personal development plan. But this is just the beginning. Communication mastery is a lifelong practice. Your next steps: 1) Revisit your weakest style once a week. 2) Practice style switching in real conversations daily. 3) Journal about your communication wins and challenges weekly. 4) Come back to this curriculum whenever you need a refresher. The skills you've learned here will compound over time — every conversation is now an opportunity to practice. Go forth and communicate with intention.",
     "key_takeaway": "Communication mastery is a lifelong practice. Use your 7 tools daily, revisit weak areas weekly, and journal about your progress.",
     "exercise": "Write a letter to your future self: 'In 6 months, I want my communication to be ___.' Be specific about what you want to achieve.",
     "reflection": "What's the single most important thing you learned in these 30 days? How will you carry it forward?",
     "quiz": {"question": "What's the most important thing to do after completing this course?", "options": ["Nothing — you're done", "Practice daily. Communication mastery is a lifelong practice that compounds over time", "Take another course immediately", "Only practice your strongest style"], "answer": 1, "explanation": "Like any skill, communication compounds with practice. The 30 days gave you the tools and awareness; daily real-world practice is what will make you a master. Every conversation is now an opportunity to grow."}},
]

# ---------------------------------------------------------------------------
# Achievement Badges
# ---------------------------------------------------------------------------

BADGES = [
    {"id": "first_step", "name": "First Step", "icon": "👣", "description": "Complete your first lesson", "condition": {"type": "lessons_completed", "value": 1}},
    {"id": "week1_done", "name": "Week 1 Warrior", "icon": "⚔️", "description": "Complete all Week 1 lessons", "condition": {"type": "week_completed", "value": 1}},
    {"id": "week2_done", "name": "Emotional Explorer", "icon": "💎", "description": "Complete all Week 2 lessons", "condition": {"type": "week_completed", "value": 2}},
    {"id": "week3_done", "name": "Expression Master", "icon": "🎭", "description": "Complete all Week 3 lessons", "condition": {"type": "week_completed", "value": 3}},
    {"id": "streak_7", "name": "7-Day Streak", "icon": "🔥", "description": "Maintain a 7-day streak", "condition": {"type": "streak", "value": 7}},
    {"id": "streak_14", "name": "Two Week Crusher", "icon": "⚡", "description": "Maintain a 14-day streak", "condition": {"type": "streak", "value": 14}},
    {"id": "streak_30", "name": "Unstoppable", "icon": "🚀", "description": "Maintain a 30-day streak", "condition": {"type": "streak", "value": 30}},
    {"id": "xp_500", "name": "Rising Star", "icon": "⭐", "description": "Earn 500 XP", "condition": {"type": "xp", "value": 500}},
    {"id": "xp_1000", "name": "Communication Pro", "icon": "🏅", "description": "Earn 1000 XP", "condition": {"type": "xp", "value": 1000}},
    {"id": "xp_2000", "name": "Communication Master", "icon": "👑", "description": "Earn 2000 XP", "condition": {"type": "xp", "value": 2000}},
    {"id": "quiz_master", "name": "Quiz Master", "icon": "🧠", "description": "Answer 20 quiz questions correctly", "condition": {"type": "quiz_correct", "value": 20}},
    {"id": "all_styles", "name": "Renaissance Communicator", "icon": "🌟", "description": "Complete lessons for all 7 styles", "condition": {"type": "all_styles", "value": 7}},
    {"id": "graduated", "name": "TalkMaster Graduate", "icon": "🎓", "description": "Complete all 30 days", "condition": {"type": "lessons_completed", "value": 30}},
]

# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    return render_template("index.html", styles=STYLES, curriculum=CURRICULUM, badges=BADGES)

@app.route("/learn/<style_id>")
def learn(style_id):
    style = STYLES.get(style_id)
    if not style:
        return render_template("not_found.html"), 404
    return render_template("learn.html", style=style, style_id=style_id)

@app.route("/curriculum")
def curriculum_overview():
    return render_template("curriculum.html", curriculum=CURRICULUM)

@app.route("/day/<int:day_num>")
def day_lesson(day_num):
    if day_num < 1 or day_num > 30:
        return render_template("not_found.html"), 404
    lesson = CURRICULUM[day_num - 1]
    style = STYLES.get(lesson["style"]) if lesson["style"] else None
    prev_day = day_num - 1 if day_num > 1 else None
    next_day = day_num + 1 if day_num < 30 else None
    return render_template("day.html", lesson=lesson, style=style, prev_day=prev_day, next_day=next_day, total_days=30)

@app.route("/api/quiz/<style_id>")
def quiz(style_id):
    style = STYLES.get(style_id)
    if not style:
        return jsonify({"error": "Style not found"}), 404
    examples = style["examples"]
    pick = random.choice(examples)
    if random.random() > 0.5:
        return jsonify({"question": "What's wrong with this way of speaking?", "example": pick["bad"], "answer": f"Here's a better version: \"{pick['good']}\"", "type": "fix"})
    else:
        return jsonify({"question": "What makes this way of speaking effective?", "example": pick["good"], "answer": f"Compare with the weak version: \"{pick['bad']}\"", "type": "analyze"})

@app.route("/api/practice/<style_id>")
def practice(style_id):
    style = STYLES.get(style_id)
    if not style:
        return jsonify({"error": "Style not found"}), 404
    exercise = random.choice(style["exercises"])
    tip = random.choice(style["tips"])
    return jsonify({"exercise": exercise, "tip": tip})

@app.route("/api/curriculum")
def api_curriculum():
    return jsonify({"curriculum": CURRICULUM, "badges": BADGES})

@app.route("/health")
def health():
    return jsonify({"status": "ok", "styles": len(STYLES), "curriculum_days": len(CURRICULUM), "badges": len(BADGES)})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
