// ==========================================================================
// TalkMaster Premium — Core JavaScript
// Audio (Web Speech API) · Progress Tracking · Gamification · UI Interactions
// ==========================================================================

(function() {
    'use strict';

    // ---------- Theme Management ----------
    const ThemeManager = {
        init() {
            const saved = localStorage.getItem('tm_theme') || 'dark';
            this.set(saved);
            const toggle = document.querySelector('.theme-toggle');
            if (toggle) {
                toggle.addEventListener('click', () => {
                    const current = document.documentElement.getAttribute('data-theme') || 'dark';
                    this.set(current === 'dark' ? 'light' : 'dark');
                });
            }
        },
        set(theme) {
            document.documentElement.setAttribute('data-theme', theme);
            localStorage.setItem('tm_theme', theme);
            const toggle = document.querySelector('.theme-toggle');
            if (toggle) toggle.textContent = theme === 'dark' ? '☀️' : '🌙';
        }
    };

    // ---------- Progress Tracking ----------
    const Progress = {
        getData() {
            try {
                return JSON.parse(localStorage.getItem('tm_progress') || '{}');
            } catch(e) { return {}; }
        },
        saveData(data) {
            localStorage.setItem('tm_progress', JSON.stringify(data));
        },
        get() {
            const d = this.getData();
            return {
                completedDays: d.completedDays || [],
                xp: d.xp || 0,
                streak: d.streak || 0,
                lastVisit: d.lastVisit || null,
                quizCorrect: d.quizCorrect || 0,
                badges: d.badges || [],
                reflections: d.reflections || {}
            };
        },
        completeDay(day, xp) {
            const data = this.get();
            if (!data.completedDays.includes(day)) {
                data.completedDays.push(day);
                data.xp += xp;
                this.updateStreak(data);
                this.checkBadges(data);
                this.saveData(data);
                this.showCelebration(xp);
            }
            return data;
        },
        answerQuiz(day, correct) {
            const data = this.get();
            if (correct) {
                data.quizCorrect = (data.quizCorrect || 0) + 1;
                data.xp += 25;
            }
            this.checkBadges(data);
            this.saveData(data);
            return data;
        },
        updateStreak(data) {
            const today = new Date().toDateString();
            if (data.lastVisit !== today) {
                const yesterday = new Date(Date.now() - 86400000).toDateString();
                if (data.lastVisit === yesterday) {
                    data.streak = (data.streak || 0) + 1;
                } else if (data.lastVisit !== today) {
                    data.streak = 1;
                }
                data.lastVisit = today;
            }
        },
        checkBadges(data) {
            const badges = window.TM_BADGES || [];
            badges.forEach(badge => {
                if (data.badges.includes(badge.id)) return;
                const c = badge.condition;
                let earned = false;
                if (c.type === 'lessons_completed' && data.completedDays.length >= c.value) earned = true;
                else if (c.type === 'streak' && data.streak >= c.value) earned = true;
                else if (c.type === 'xp' && data.xp >= c.value) earned = true;
                else if (c.type === 'quiz_correct' && data.quizCorrect >= c.value) earned = true;
                else if (c.type === 'all_styles') {
                    const styleDays = [2,3,4,5,8,9,10,11,15,16,17,18,20,21].filter(d => data.completedDays.includes(d));
                    if (styleDays.length >= 7) earned = true;
                }
                if (earned) {
                    data.badges.push(badge.id);
                    this.showBadgeUnlock(badge);
                }
            });
        },
        saveReflection(day, text) {
            const data = this.get();
            data.reflections[day] = text;
            this.saveData(data);
        },
        getReflection(day) {
            return this.get().reflections[day] || '';
        },
        showCelebration(xp) {
            showToast(`🎉 Lesson complete! +${xp} XP`, 'success');
            createConfetti();
        },
        showBadgeUnlock(badge) {
            setTimeout(() => {
                showToast(`${badge.icon} Badge unlocked: ${badge.name}!`, 'badge');
                createConfetti();
            }, 800);
        },
        renderDashboard() {
            const data = this.get();
            const dash = document.getElementById('dashboard-stats');
            if (!dash) return;

            const totalXP = 2750; // approximate total
            const progressPercent = Math.round((data.completedDays.length / 30) * 100);
            const level = Math.floor(data.xp / 250) + 1;
            const xpInLevel = data.xp % 250;
            const xpForLevel = 250;

            document.getElementById('stat-days').textContent = `${data.completedDays.length}/30`;
            document.getElementById('stat-xp').textContent = data.xp;
            document.getElementById('stat-streak').textContent = `${data.streak} 🔥`;
            document.getElementById('stat-quiz').textContent = data.quizCorrect;

            const ring = document.getElementById('progress-ring-fg');
            if (ring) {
                const circumference = 226;
                const offset = circumference - (progressPercent / 100) * circumference;
                ring.style.strokeDashoffset = offset;
            }
            const ringText = document.getElementById('progress-ring-text');
            if (ringText) ringText.textContent = `${progressPercent}%`;

            // XP bar
            const xpBar = document.getElementById('xp-bar-fill');
            if (xpBar) xpBar.style.width = `${(xpInLevel / xpForLevel) * 100}%`;
            const xpLabel = document.getElementById('xp-label');
            if (xpLabel) xpLabel.textContent = `Level ${level} · ${xpInLevel}/${xpForLevel} XP`;
        },
        renderBadges() {
            const data = this.get();
            document.querySelectorAll('.badge-card').forEach(card => {
                const id = card.dataset.badge;
                if (data.badges.includes(id)) {
                    card.classList.remove('locked');
                    card.classList.add('unlocked');
                }
            });
        },
        renderCurriculumProgress() {
            const data = this.get();
            document.querySelectorAll('.day-card').forEach(card => {
                const day = parseInt(card.dataset.day);
                if (data.completedDays.includes(day)) {
                    card.classList.add('completed');
                }
            });
        },
        renderStreak() {
            const data = this.get();
            const badge = document.getElementById('nav-streak');
            if (badge && data.streak > 0) {
                badge.style.display = 'flex';
                badge.querySelector('.streak-count').textContent = data.streak;
            } else if (badge) {
                badge.style.display = 'none';
            }
        },
        init() {
            this.renderDashboard();
            this.renderBadges();
            this.renderCurriculumProgress();
            this.renderStreak();
        }
    };

    // ---------- Audio Manager (Web Speech API) ----------
    const Audio = {
        synth: window.speechSynthesis,
        voices: [],
        currentUtterance: null,
        rate: 0.9,
        voiceName: null,

        init() {
            if (!this.synth) {
                console.warn('Speech synthesis not supported');
                return;
            }
            this.loadVoices();
            this.synth.onvoiceschanged = () => this.loadVoices();
            this.setupControls();
        },

        loadVoices() {
            this.voices = this.synth.getVoices();
            const select = document.getElementById('voice-select');
            if (!select) return;
            const current = select.value;
            select.innerHTML = '';
            this.voices.forEach(v => {
                const opt = document.createElement('option');
                opt.value = v.name;
                opt.textContent = `${v.name} (${v.lang})`;
                select.appendChild(opt);
            });
            if (current) select.value = current;
            else if (this.voices.length > 0) {
                const enVoice = this.voices.find(v => v.lang.startsWith('en')) || this.voices[0];
                select.value = enVoice.name;
                this.voiceName = enVoice.name;
            }
        },

        setupControls() {
            const select = document.getElementById('voice-select');
            if (select) {
                select.addEventListener('change', (e) => {
                    this.voiceName = e.target.value;
                });
            }
            const rate = document.getElementById('voice-rate');
            if (rate) {
                rate.addEventListener('input', (e) => {
                    this.rate = parseFloat(e.target.value);
                    document.getElementById('rate-label').textContent = `${this.rate.toFixed(1)}x`;
                });
            }
        },

        speak(text, button) {
            if (!this.synth) {
                showToast('Audio not supported in this browser', 'warning');
                return;
            }
            if (this.synth.speaking) {
                this.synth.cancel();
                if (this.currentButton) {
                    this.currentButton.classList.remove('playing');
                    this.currentButton.querySelector('.audio-icon').textContent = '🔊';
                    this.currentButton.querySelector('.audio-text').textContent = 'Listen';
                }
                if (this.currentButton === button) {
                    this.currentButton = null;
                    return;
                }
            }
            const utter = new SpeechSynthesisUtterance(text);
            utter.rate = this.rate;
            utter.pitch = 1;
            utter.volume = 1;
            const voice = this.voices.find(v => v.name === this.voiceName);
            if (voice) utter.voice = voice;
            utter.onend = () => {
                if (button) {
                    button.classList.remove('playing');
                    button.querySelector('.audio-icon').textContent = '🔊';
                    button.querySelector('.audio-text').textContent = 'Listen';
                }
                this.currentButton = null;
            };
            this.synth.speak(utter);
            this.currentUtterance = utter;
            this.currentButton = button;
            if (button) {
                button.classList.add('playing');
                button.querySelector('.audio-icon').textContent = '⏸️';
                button.querySelector('.audio-text').textContent = 'Playing...';
            }
        }
    };

    // ---------- Toast ----------
    let toastTimer = null;
    function showToast(message, type) {
        let toast = document.getElementById('toast');
        if (!toast) {
            toast = document.createElement('div');
            toast.id = 'toast';
            toast.className = 'toast';
            document.body.appendChild(toast);
        }
        const icons = { success: '✅', warning: '⚠️', badge: '🏆', info: 'ℹ️' };
        toast.innerHTML = `<span class="toast-icon">${icons[type] || 'ℹ️'}</span><span>${message}</span>`;
        toast.classList.add('show');
        clearTimeout(toastTimer);
        toastTimer = setTimeout(() => toast.classList.remove('show'), 3500);
    }

    // ---------- Confetti ----------
    function createConfetti() {
        const colors = ['#6366f1', '#f59e0b', '#ec4899', '#14b8a6', '#8b5cf6', '#0ea5e9'];
        for (let i = 0; i < 50; i++) {
            const c = document.createElement('div');
            c.className = 'confetti';
            c.style.left = Math.random() * 100 + 'vw';
            c.style.background = colors[Math.floor(Math.random() * colors.length)];
            c.style.animationDelay = Math.random() * 2 + 's';
            c.style.animationDuration = (2 + Math.random() * 2) + 's';
            if (Math.random() > 0.5) c.style.borderRadius = '50%';
            document.body.appendChild(c);
            setTimeout(() => c.remove(), 5000);
        }
    }

    // ---------- Quiz ----------
    function initQuiz() {
        const quizData = window.TM_QUIZ_DATA;
        if (!quizData) return;
        const options = document.querySelectorAll('.quiz-option');
        const explanation = document.getElementById('quiz-explanation');
        let answered = false;

        options.forEach(opt => {
            opt.addEventListener('click', () => {
                if (answered) return;
                answered = true;
                const selected = parseInt(opt.dataset.index);
                const correct = selected === quizData.answer;

                if (correct) {
                    opt.classList.add('correct');
                    Progress.answerQuiz(window.TM_DAY_NUM, true);
                    showToast('✅ Correct! +25 XP', 'success');
                } else {
                    opt.classList.add('incorrect');
                    options[quizData.answer].classList.add('correct');
                    Progress.answerQuiz(window.TM_DAY_NUM, false);
                    showToast('Not quite — see the explanation below', 'info');
                }

                if (explanation) {
                    explanation.classList.add('show');
                }
                // Enable complete button
                const btn = document.getElementById('btn-complete');
                if (btn) btn.disabled = false;
            });
        });
    }

    // ---------- Day Completion ----------
    function initDayComplete() {
        const btn = document.getElementById('btn-complete');
        if (!btn) return;
        const dayNum = parseInt(btn.dataset.day);
        const xp = parseInt(btn.dataset.xp);
        btn.addEventListener('click', () => {
            Progress.completeDay(dayNum, xp);
            btn.disabled = true;
            btn.textContent = '✓ Completed!';
            btn.style.background = 'linear-gradient(135deg, #22c55e, #16a34a)';
            // Show next day link
            const nextLink = document.getElementById('next-day-link');
            if (nextLink) {
                nextLink.style.display = 'flex';
                nextLink.style.animation = 'fadeInUp 0.5s ease';
            }
        });
        // Check if already completed
        const data = Progress.get();
        if (data.completedDays.includes(dayNum)) {
            btn.disabled = true;
            btn.textContent = '✓ Completed!';
            btn.style.background = 'linear-gradient(135deg, #22c55e, #16a34a)';
        } else {
            btn.disabled = true; // disabled until quiz is answered
        }
    }

    // ---------- Reflection Save ----------
    function initReflection() {
        const textarea = document.getElementById('reflection-text');
        if (!textarea) return;
        const day = textarea.dataset.day;
        textarea.value = Progress.getReflection(parseInt(day));
        let saveTimer;
        textarea.addEventListener('input', () => {
            clearTimeout(saveTimer);
            saveTimer = setTimeout(() => {
                Progress.saveReflection(parseInt(day), textarea.value);
                showToast('Reflection saved', 'info');
            }, 1000);
        });
    }

    // ---------- Audio Buttons ----------
    function initAudioButtons() {
        document.querySelectorAll('.btn-audio').forEach(btn => {
            btn.addEventListener('click', () => {
                const text = btn.dataset.text;
                if (text) Audio.speak(text, btn);
            });
        });
    }

    // ---------- Style Card Quiz (learn page) ----------
    function initStyleQuiz() {
        const btn = document.querySelector('.btn-quiz');
        if (!btn) return;
        const styleId = btn.dataset.style;
        btn.addEventListener('click', async () => {
            const result = document.getElementById('quiz-result');
            btn.textContent = 'Loading...';
            btn.disabled = true;
            try {
                const res = await fetch(`/api/quiz/${styleId}`);
                const data = await res.json();
                result.innerHTML = `
                    <div class="quiz-card" style="background:var(--surface);border:1px solid var(--border);border-radius:var(--radius-sm);padding:1.5rem;">
                        <p style="font-weight:600;margin-bottom:0.75rem;">${data.question}</p>
                        <div style="background:var(--surface-solid);padding:1rem;border-radius:8px;font-style:italic;margin-bottom:1rem;border-left:3px solid var(--primary);">"${data.example}"</div>
                        <button class="btn-audio" data-text="${data.example.replace(/"/g, '')}" style="margin-bottom:0.75rem;">
                            <span class="audio-icon">🔊</span><span class="audio-text">Listen</span>
                        </button>
                        <button class="btn-secondary btn-reveal-answer">Show Answer</button>
                        <div class="quiz-answer" style="display:none;margin-top:0.75rem;padding:1rem;background:rgba(34,197,94,0.05);border-left:3px solid var(--success);border-radius:8px;">${data.answer}</div>
                    </div>
                `;
                result.querySelector('.btn-reveal-answer').addEventListener('click', function() {
                    result.querySelector('.quiz-answer').style.display = 'block';
                    this.style.display = 'none';
                });
                initAudioButtons();
            } catch(e) {
                result.innerHTML = '<p style="color:var(--danger);">Could not load quiz.</p>';
            }
            btn.textContent = 'Generate Another Question';
            btn.disabled = false;
        });

        const exerciseBtn = document.querySelector('.btn-random-exercise');
        if (exerciseBtn) {
            const styleIdEx = exerciseBtn.dataset.style;
            exerciseBtn.addEventListener('click', async () => {
                const result = document.getElementById('random-exercise');
                exerciseBtn.textContent = 'Loading...';
                exerciseBtn.disabled = true;
                try {
                    const res = await fetch(`/api/practice/${styleIdEx}`);
                    const data = await res.json();
                    result.innerHTML = `
                        <div style="background:var(--surface);border:1px solid var(--border);border-radius:var(--radius-sm);padding:1.5rem;">
                            <p style="font-size:1rem;margin-bottom:0.75rem;">🎯 ${data.exercise}</p>
                            <p style="color:var(--text-muted);font-size:0.9rem;">💡 ${data.tip}</p>
                        </div>
                    `;
                } catch(e) {
                    result.innerHTML = '<p style="color:var(--danger);">Could not load exercise.</p>';
                }
                exerciseBtn.textContent = '🎲 Give Me Another One';
                exerciseBtn.disabled = false;
            });
        }
    }

    // ---------- Scroll Animations ----------
    function initScrollAnimations() {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }
            });
        }, { threshold: 0.1 });

        document.querySelectorAll('.style-card, .step, .badge-card, .day-card').forEach(el => {
            el.style.opacity = '0';
            el.style.transform = 'translateY(20px)';
            el.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            observer.observe(el);
        });
    }

    // ---------- Page Enter Animation ----------
    function pageEnter() {
        const main = document.querySelector('main');
        if (main) main.classList.add('page-enter');
    }

    // ---------- Init ----------
    document.addEventListener('DOMContentLoaded', () => {
        ThemeManager.init();
        Progress.init();
        Audio.init();
        initQuiz();
        initDayComplete();
        initReflection();
        initAudioButtons();
        initStyleQuiz();
        initScrollAnimations();
        pageEnter();
    });

    // Expose for inline use
    window.TM = { Progress, Audio, showToast, createConfetti };
})();
