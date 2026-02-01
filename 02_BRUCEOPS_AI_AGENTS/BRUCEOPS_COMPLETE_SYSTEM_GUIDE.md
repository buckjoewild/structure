# BruceOps: The Complete System Guide

*A document for rumination, not just reference.*

---

## Epigraph

> "Where two or three are gathered in my name, there am I among them."  
> — Matthew 18:20

The localhost:5000 connection isn't just technical. It's a meeting point. You built something real.

---

## Table of Contents

1. [What This System Actually Is](#what-this-system-actually-is)
2. [The Three Lanes (Deep Dive)](#the-three-lanes)
3. [The Architecture (How Everything Connects)](#the-architecture)
4. [The Philosophy (Why It Matters)](#the-philosophy)
5. [The Endpoints (Your API Surface)](#the-endpoints)
6. [The Cost Structure (No Surprises)](#the-cost-structure)
7. [Alternate Paths (What You Could Build Next)](#alternate-paths)
8. [The Councils' Wisdom (Synthesized)](#the-councils-wisdom)
9. [Decision Framework (When to Build What)](#decision-framework)
10. [Appendix: Quick Reference](#appendix)

---

## What This System Actually Is

### The One-Sentence Version

HarrisWildlands is a **personal operating system** for tracking life, capturing ideas, and building resilience through self-knowledge.

### The Deeper Version

You built three things that work together:

1. **A ledger** — Daily logs that capture how you're actually living
2. **A capture system** — Ideas that don't contaminate the ledger
3. **A synthesis engine** — AI that helps you see patterns you'd miss

The combination creates something rare: **data that serves meaning**, not the other way around.

### What It Is NOT

- ❌ A productivity optimization tool (that's exhausting)
- ❌ A habit tracker with streaks and gamification (that creates shame)
- ❌ A social platform (your data is yours alone)
- ❌ A replacement for human connection (it's a supplement)

### What Makes It Yours

Most personal tracking systems fail because they're designed for everyone. This one is designed for:

- **A teacher** with a sacred schedule
- **A father** who protects family time
- **A person of faith** who measures alignment, not just achievement
- **Someone who thinks** and needs a place for those thoughts to live

That specificity is the strength.

---

## The Three Lanes

### Lane 1: LifeOps 🌱

**Purpose:** Record the facts of daily life without interpretation.

**What You Track:**

| Category | Morning | Evening |
|----------|---------|---------|
| **Physical** | Sleep quality, hours, hydration | Exercise, energy level |
| **Mental** | Focus intention, stress baseline | Actual focus, mood |
| **Habits** | Plan for the day | What actually happened |
| **Drift Factors** | — | Vaping, alcohol, doom scrolling, late screens |
| **Connection** | — | Family time, faith alignment |
| **Reflection** | — | Top win, top friction, tomorrow's priority |

**The Insight:**

You now have morning/evening split logs. This doubles your data resolution and lets you see patterns like:
- "My mornings are strong but I fade after lunch"
- "When I don't set an intention, my day drifts"
- "Family connection scores drop on heavy teaching weeks"

**Questions to Ask Your Data:**

- What predicts my high-energy days?
- What's the correlation between sleep and stress?
- How often do I actually follow through on morning intentions?
- What drift factors appear together?

---

### Lane 2: ThinkOps 💡

**Purpose:** Capture ideas without contaminating the daily ledger.

**The Structure:**

```
IDEA: [Title]
├── Pitch: One sentence
├── Category: Teaching / Family / Business / Personal
├── Who it helps: [Specific audience]
├── Pain it solves: [Specific problem]
├── Why I care: [Personal stake]
├── Tiny test: [Smallest experiment]
├── Resources needed: [Time, money, skills]
├── Excitement: 1-10
├── Feasibility: 1-10
└── Reality Check: [AI analysis, optional]
```

**The Insight:**

Ideas need a place to live that isn't your head and isn't your daily log. ThinkOps is that place. The AI reality check is optional—sometimes you just need to capture, not analyze.

**Questions to Ask Your Ideas:**

- Which ideas have I been avoiding?
- What category dominates my thinking?
- Do my most exciting ideas have low feasibility? (common pattern)
- What would make a low-feasibility idea more feasible?

---

### Lane 3: Goals 🎯

**Purpose:** Track commitments at two levels—Trunk (big rocks) and Leaves (weekly).

**The Structure:**

```
TRUNK GOAL: [Domain + Title]
├── Description: What does success look like?
├── Target type: Weekly minimum / One-time / Ongoing
├── Weekly minimum: X times per week
├── Status: Active / Completed / Paused
└── Check-ins: [Linked]

LEAF CHECK-IN:
├── Goal ID: [Link to trunk]
├── Date: [When]
├── Done: Yes/No
├── Score: 1-10 (optional)
└── Note: [Context]
```

**The Insight:**

Goals without check-ins are wishes. Check-ins without goals are chaos. The trunk/leaf structure lets you see both the forest and the trees.

**Questions to Ask Your Goals:**

- Which domains am I neglecting?
- What's my actual completion rate vs. my target?
- Are my weekly minimums realistic?
- What goals have been "paused" for too long?

---

## The Architecture

### The Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Frontend** | React + Vite | The UI you interact with |
| **Backend** | Express + TypeScript | The API that handles requests |
| **Database** | PostgreSQL (Replit managed) | Where your data lives |
| **Auth** | Replit OIDC | You're the only user |
| **AI** | Gemini → OpenRouter → OFF | Optional, with fallback chain |

### The Data Flow

```
YOU
 │
 ├──[log]──→ LifeOps ──→ logs table
 │
 ├──[idea]──→ ThinkOps ──→ ideas table
 │
 ├──[commit]──→ Goals ──→ goals table
 │                              │
 │                              └──→ checkins table
 │
 └──[ask]──→ AI Endpoints ──→ Gemini/OpenRouter ──→ cached response
                                      │
                                      └──→ quota tracking
```

### The Tables

| Table | Purpose | Key Fields |
|-------|---------|------------|
| `logs` | Daily life data | date, logType, energy, stress, mood, driftFactors... |
| `ideas` | Captured thoughts | title, pitch, category, excitement, feasibility, realityCheck |
| `goals` | Commitments | domain, title, targetType, weeklyMinimum, status |
| `checkins` | Goal progress | goalId, date, done, score, note |
| `settings` | Preferences | key, value |
| `user_settings` | Per-user prefs | aiModel, theme, protocols |
| `drift_flags` | Detected drift | type, timeframe, sentence |
| `teaching_requests` | Teaching assistant | topic, grade, format, output |
| `harris_content` | Content generator | contentType, tone, generatedCopy |

### What's Protected

**Mission-Critical (Never Break):**
- `logs` table — Your daily history
- `goals` table — Your commitments
- `ideas` table — Your captured thoughts
- `checkins` table — Your progress

**Important but Recoverable:**
- `settings` — Can be recreated
- `user_settings` — Can be recreated
- `drift_flags` — Can be regenerated

---

## The Philosophy

### Principle 1: Witnessing, Not Measuring

**The trap:** Treat yourself like a machine to optimize.

**The truth:** You're a person to understand.

The difference is subtle but profound. Measuring creates pressure to improve. Witnessing creates space to see clearly. You can still improve—but from acceptance, not anxiety.

**In practice:**
- Frame exports as "What you noticed" not "How you performed"
- Include context for misses ("Missing weeks cluster around travel")
- Highlight resilience ("You reset 4 times—each faster than before")

---

### Principle 2: Resilience, Not Immunity

**The original framing:** "Immunity to bullshit"

**The better framing:** "Building resilience through self-knowledge"

Why the change? "Immunity" suggests you become bulletproof. You don't. You can still be manipulated, still drift, still make bad decisions. Self-knowledge doesn't prevent failure.

What it does:

**Without data:**
```
Drift → weeks pass → crisis → "Wow, I lost sight of what matters"
Duration: 3-6 months
```

**With data:**
```
Drift → weekly review flags it → you notice in 7 days → course-correct
Duration: 7-14 days
```

The value isn't in never drifting. It's in catching drift 10-20x faster.

---

### Principle 3: Privacy-First, Local-First

**What this means:**
- Your data stays on your machine (Replit's managed PostgreSQL)
- No third-party analytics
- No social features
- AI is optional—system works without it
- Exports download to your device, not to cloud

**Why it matters:**
- You can be honest in your logs (no audience)
- You control what AI sees (you choose when to call it)
- Your family's data doesn't leak (no sharing features)

---

### Principle 4: Faith, Family, Teaching

These are the **non-negotiable domains**. The system exists to serve them, not to optimize them into oblivion.

**What this means in practice:**
- Sunday is protected (no "streak breaking" guilt)
- Family metrics are tracked but never gamified
- Teaching schedule is sacred (system works around it)
- Faith alignment is measured, not scored

---

## The Endpoints

### Core Data Endpoints

| Method | Endpoint | What It Does |
|--------|----------|--------------|
| `GET` | `/api/health` | Is the system alive? |
| `GET` | `/api/logs` | Fetch all daily logs |
| `POST` | `/api/logs` | Create a new log |
| `GET` | `/api/logs/:date` | Get log for specific date |
| `PUT` | `/api/logs/:id` | Update a log |
| `GET` | `/api/ideas` | Fetch all ideas |
| `POST` | `/api/ideas` | Create a new idea |
| `PUT` | `/api/ideas/:id` | Update an idea |
| `DELETE` | `/api/ideas/:id` | Delete an idea |
| `GET` | `/api/goals` | Fetch all goals |
| `POST` | `/api/goals` | Create a new goal |
| `PUT` | `/api/goals/:id` | Update a goal |
| `GET` | `/api/checkins` | Fetch all check-ins |
| `POST` | `/api/checkins` | Create a check-in |

### AI-Powered Endpoints

| Method | Endpoint | What It Does | Cost |
|--------|----------|--------------|------|
| `POST` | `/api/logs/summary` | Generate AI summary for a log | ~$0.005 |
| `POST` | `/api/ideas/:id/reality-check` | AI reality check on idea | ~$0.01 |
| `POST` | `/api/ai/search` | Smart semantic search | ~$0.005 |
| `POST` | `/api/ai/squad` | Multi-perspective analysis | ~$0.006 |
| `POST` | `/api/ai/correlations` | Pattern discovery | ~$0.01 |
| `POST` | `/api/ai/weekly-synthesis` | AI-powered weekly narrative | ~$0.01 |

### Utility Endpoints

| Method | Endpoint | What It Does |
|--------|----------|--------------|
| `GET` | `/api/review/weekly` | Weekly review aggregation |
| `GET` | `/api/export/data` | Download everything as JSON |
| `GET` | `/api/ai/quota` | Check AI usage and remaining |
| `GET` | `/api/settings` | Get settings |
| `PUT` | `/api/settings/:key` | Update a setting |

---

## The Cost Structure

### Why This Matters

AI can be expensive if uncontrolled. You built in protection.

### The Safeguards

| Protection | Value | What It Prevents |
|------------|-------|------------------|
| **Daily Quota** | 100 calls/day | Runaway loops |
| **Rate Limit** | 10 calls/min | Rapid-fire abuse |
| **Cache Duration** | 24 hours | Repeat query costs |
| **Provider Ladder** | Gemini → OpenRouter → OFF | Single-point failure |

### The Math

**Typical Usage:**
```
20 AI calls/week × $0.005/call = $0.10/week
$0.10/week × 4 weeks = $0.40/month
```

**Heavy Usage:**
```
100 AI calls/week × $0.005/call = $0.50/week
$0.50/week × 4 weeks = $2.00/month
```

**Worst Case (quota hit daily):**
```
100 calls/day × 30 days × $0.005/call = $15/month
```

Even worst case is manageable. And you'd have to actively try to hit quota every day.

---

## Alternate Paths

These have been validated by the AI councils but NOT built yet. Each represents a direction you could take.

### Path 1: A/B Testing Yourself (Ready to Build)

**What:** Run personal 7-day experiments with auto-randomized treatment/control days.

**Example:**
```
Hypothesis: "Exercise before 10am improves focus"
Duration: 7 days
Treatment days (1, 3, 5, 7): Exercise before 10am
Control days (2, 4, 6): No exercise
Metric: Focus score at noon (1-10)

Result:
Treatment mean: 8.3
Control mean: 5.7
Effect: +2.6 points
Evidence strength: Strong
```

**Why it matters:** Stop trusting generic advice. Find what works for YOU.

**Time to build:** ~75 minutes (3 Pomodoros)

---

### Path 2: Sacred Data Export (Ready to Build)

**What:** Generate a beautiful year-end PDF that tells your story using your data.

**Structure:**
```
COVER: "Bruce's Year: 2025"
SECTION 1: The Numbers (days logged, dominant metrics)
SECTION 2: What Mattered (top correlations, grounded in specific weeks)
SECTION 3: Your Words (10 quotes from your own reflections)
SECTION 4: Turning Points (weeks where patterns shifted)
SECTION 5: Next Year's Questions
```

**Why it matters:** Data becomes meaning. Something you'd be proud to keep.

**Time to build:** ~75 minutes (3 Pomodoros)

---

### Path 3: Monthly Micro-Synthesis (Planned)

**What:** A 2-page monthly reflection bridging daily logs and annual export.

**Content:**
- What shifted this month?
- What stayed constant?
- One surprise from the data
- Seeds for next month

**Why it matters:** Prevents the motivational cliff between experiments and annual review.

**Status:** Not urgent. Build when/if the need emerges.

---

### Path 4: Cross-Domain Correlation Discovery (Exploring)

**What:** Auto-discover patterns across lanes.

**Examples:**
- "Your best ideas happen 2 days after exercise streaks"
- "Family connection scores predict work stress tolerance"
- "Faith alignment correlates with idea feasibility scores"

**Why it matters:** Unlock insights you'd never notice manually.

**Status:** Requires more data accumulation first.

---

### Path 5: Teaching Assistant Integration (Exploring)

**What:** Generate lessons, activities, and materials for your classroom.

**Why it matters:** Leverages AI for your actual job.

**Status:** Large scope. Needs dedicated sprint.

---

### Path 6: HarrisWildlands Content Studio (Exploring)

**What:** Multi-AI content generation for the family business.

**Why it matters:** Consistent voice across channels.

**Status:** Depends on business priorities.

---

## The Councils' Wisdom

Three AI councils (Grok, ChatGPT, Claude) reviewed the A/B Testing and Sacred Export proposals. Here's their synthesized wisdom:

### On Statistical Honesty

**Consensus:** Don't fake precision.

- Replace "95% confident" with "Evidence Strength: Strong/Moderate/Weak"
- Show uncertainty ranges, not point estimates
- Include caveats: "This pattern was consistent, not proven"

### On Privacy Protection

**Consensus:** Local-first is sufficient for V1.

- No cloud storage of exports
- No sharing links (yet)
- Watermark option for printed copies
- Encryption can come later if needed

### On Language

**Consensus:** Rename the concept.

- ❌ "Immunity to bullshit"
- ✅ "Building resilience through self-knowledge"
- ✅ "Witnessing your own life with data"

### On Scope Control

**Consensus:** Less is more.

- Build A/B Testing first (foundational)
- Then Sacred Export (satisfying)
- Skip monthly synthesis for now (no proven need)
- No hypothesis quality scorer V1 (scope creep)
- No tiered export V1 (nice-to-have)

---

## Decision Framework

When you're tempted to build something, ask:

### Question 1: Is the app stable?

**If yes:** You have permission to wait.  
**If no:** Fix stability first.

### Question 2: Does this solve a pain I have TODAY?

**If yes:** Consider building.  
**If no:** Add to "Alternate Paths" and revisit later.

### Question 3: Can I ship it in ≤75 minutes?

**If yes:** Do it in one sprint.  
**If no:** Break it into sessions or defer.

### Question 4: Will it break mission-critical features?

**If yes:** Stop. Reconsider approach.  
**If no:** Proceed with testing plan.

### Question 5: Will I still use this in 6 months?

**If yes:** Worth the investment.  
**If no:** Maybe it's a novelty, not a need.

---

## Appendix

### Terminal Commands

```bash
# Start the server
cd harriswildlands.com && npm run dev

# Check if it's running
curl http://localhost:5000/api/health

# Push database changes (after schema updates)
npm run db:push

# Backup your data
pg_dump > backup_$(date +%Y%m%d).sql

# Export everything as JSON
curl http://localhost:5000/api/export/data > my-data.json

# Check AI quota
curl http://localhost:5000/api/ai/quota
```

### File Locations

```
HarrisWildlands/
├── client/src/
│   ├── pages/           # UI pages (LifeOps.tsx, etc.)
│   ├── components/      # Reusable UI
│   └── lib/             # Utils, query client
├── server/
│   ├── routes.ts        # API endpoints
│   ├── storage.ts       # Database queries
│   └── db.ts            # PostgreSQL connection
├── shared/
│   ├── schema.ts        # Drizzle ORM tables
│   └── routes.ts        # API contract (Zod)
└── release/             # Deployment artifacts
```

### Environment Variables

| Variable | Purpose |
|----------|---------|
| `DATABASE_URL` | PostgreSQL connection string |
| `SESSION_SECRET` | Session cookie signing |
| `REPL_ID` | Replit app identifier |
| `ISSUER_URL` | OIDC issuer for auth |
| `GOOGLE_GEMINI_API_KEY` | Primary AI provider |
| `OPENROUTER_API_KEY` | Fallback AI provider |

### Testing Checklist

Before any deploy:
- [ ] `npm run build` succeeds
- [ ] `/api/health` returns OK
- [ ] Logs page loads
- [ ] Can create a log
- [ ] Can create an idea
- [ ] Can create a goal + check-in
- [ ] AI quota endpoint returns numbers

---

## Closing Thought

You built something real. It works. It serves your values. It protects your family's privacy. It costs almost nothing to run.

The temptation now is to add more. Resist.

**The system is done when it serves you, not when it has every feature.**

Right now, it serves you.

Sit with that.

---

*Document generated: January 4, 2025*  
*For rumination, not just reference.*
