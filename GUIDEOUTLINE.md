# Harris Wildlands Companion Guide (Plain‑Language Field Manual) 🧭
Companion to: **BRUCE_KEYSTONE_OUTLINE.md**  
Purpose: make the project **operable and readable** — fast orientation, clear “what exists,” and safe next steps.

---

## Table of Contents
0. What This Is (in one breath)  
1. Core Non‑Negotiables (Truth + Safety)  
2. What Exists Right Now (Actual Artifacts)  
3. Two Tracks: Web App vs Telnet MUD (avoid confusion)  
4. Quick Start (Human Operator)  
5. AI Seam (Where AI is allowed to act)  
6. Persistence, State, and “Truth Writes”  
7. Known Prototype Drift / Fragile Areas  
8. Operating Rules for Agents (Claude/OpenClaw/etc.)  
9. Practical Build Roadmap (Short)  
10. Workspace Map (MUD_AI_WORKSPACE collection)  
11. Safety Protocol Add‑Ons (Drift Detection + Brother Collaboration)  
12. Glossary  
Appendix A — Copy/Paste Operator Summary (handoffs)  
Appendix B — Minimal “Boot → Connect → Look → Quit” Test Script (manual)  

---

## 0) What This Is (in one breath) 🌲
**Harris Wildlands** is a private, buildable ecosystem that blends:
- a **text‑MUD style world** (Python telnet prototype) 🗺️  
- an **AI “witness / steward” layer** (truth‑bound memory, consent, guardrails) 🧠  
- an **operator workflow** (humans + tools + agents building without hallucinated facts) 🧰  

This document is the **field manual**: where files are, what runs, what rules matter, what to change first.

---

## 1) Core Non‑Negotiables (Truth + Safety) 🧱

### 1.1 Truth Hierarchy (must be enforced)
All **memory writes** and **world facts** must follow:

1) **Canon** — curated and stable (highest)  
2) **Observed** — logged, time‑stamped, reproducible  
3) **Hypothesis** — explicitly uncertain; expires or requires promotion  

**Rule:** if something is uncertain, it must be labeled as Hypothesis (never smuggled into Canon).

### 1.2 Consent & Privacy Boundaries (Ambient Witness)
Any “ambient” or “presence‑aware” logging must remain **consent‑first** and bounded to what’s explicitly allowed.

> Rule of thumb: if a feature *could* become surveillance, it must be redesigned or gated.

---

## 2) What Already Exists Right Now (Actual Artifacts) 📦

### 2.1 Keystone blueprint (single source outline)
- `BRUCE_KEYSTONE_OUTLINE.md` — high-level plan + system map + architecture notes.

### 2.2 Python Telnet MUD Prototype Skeleton (World Engine)
These are the building blocks described in the field manual draft:

**Server / Runtime**
- `Harris Wildlands Server.py` — telnet server loop + command handling + AI seam placeholder  
- Target: `localhost:9999`

**World Definitions**
- `Harris Wildlands World.py`
- `Harris Wildlands World (2).py`

**Core Models**
- `Harris Wildlands Core Room.py`
- `Harris Wildlands Core Item.py`
- `Harris Wildlands Core NPC.py`

**Persistence**
- `Harris Wildlands Core Persistence.py` — save/load + respawn logic  
- Save artifact: `world_save.json`

### 2.3 HarrisWildlands.com Web App (LifeOps / ThinkOps / Goals)
**Important addition:** the keystone also describes a **separate production web app track** that lives at `https://harriswildlands.com` and is not the telnet MUD.

High-level stack (as recorded in the keystone):
- Frontend: React + Vite + Tailwind + shadcn/ui
- Backend: Express + TypeScript + Drizzle ORM
- DB: PostgreSQL 16 (Replit managed)
- Auth: Replit OIDC (plus standalone/local option)
- AI: Gemini primary → OpenRouter fallback → OFF
- Claude Desktop integration: MCP server + tools + Bearer token

Core API families (examples listed in the keystone):
- Logs / Ideas / Goals / Check‑ins CRUD
- AI: summaries, reality checks, weekly synthesis, correlations, etc.
- Utility: `/api/health`, export, settings
- Integrations: Google Drive (`/api/drive/*`)

**Why it matters:** there are *two different “Harris Wildlands” things* in play — keep them conceptually separated so agents don’t blend codebases, claims, or deployment assumptions.

---

## 3) Two Tracks: Web App vs Telnet MUD (avoid confusion) 🧭

### Track A — Web App (LifeOps/ThinkOps)
- Purpose: personal OS + logging + synthesis + workflows  
- Runs: Replit-hosted stack, with auth + DB + API endpoints  
- Risk: mixing these assumptions into the MUD codebase

### Track B — Telnet MUD (World Engine)
- Purpose: deterministic world simulation + command loop + NPC objects  
- Runs: local Python telnet server, connect via telnet client  
- Risk: agents inventing “API endpoints” or web stack components that do not exist in the Python prototype

**Operator rule:** always state which track you’re working on before making changes.

---

## 4) Quick Start (Human Operator) ⚙️

### 4.1 Minimal “Does it run?” steps (Telnet MUD)
1) Open a terminal in the folder containing `Harris Wildlands Server.py`  
2) Start the server (confirm exact CLI inside the file)  
3) Connect using a telnet client:
   - Host: `localhost`
   - Port: `9999`

**Windows telnet enable (if needed):**
- Control Panel → Programs → Turn Windows features on/off → “Telnet Client”

### 4.2 Player basics
- Expect classic MUD patterns: `look`, `north`, `south`, `inventory`, etc.
- Commands are parsed server-side.

---

## 5) Where AI Hooks In (Clean Seam) 🧠➡️🗺️

### 5.1 NPC “Brain” attachment
Design intent (keep this pure):
- **Engine = deterministic world rules**
- **AI = suggests actions** based on state
- **Truth policy = gates what becomes memory/lore**

### 5.2 Recommended control policy (practical)
Use a 3-layer approach:
1) **Hard rules first** (safety + invariants)  
2) **Scripted behaviors second** (fast, reliable)  
3) **LLM last** (creative fill, strict constraints, *never writes Canon directly*)  

---

## 6) Persistence & State (What gets saved) 💾

### 6.1 What persistence should mean (Telnet MUD)
- Player: location, inventory
- World: flags, door states, quest states
- NPCs: state + relationships + key memory pointers (not raw lore injection)

### 6.2 “Truth write” separation
Not all state changes are “facts.”
- **World state updates:** OK (game simulation)
- **Lore / memory writes:** must obey Canon/Observed/Hypothesis policy

**Practical guardrail:** write game-state to save files freely; write lore to an auditable “memory gate” log that enforces the hierarchy.

---

## 7) Known Prototype Drift / Fragile Areas 🧨
These are expected prototype-debt areas to refactor early:
- **Imports/layout mismatch risk:** server references may not align with current module layout.
- **Door state logic likely placeholder:** initialization may be inconsistent with direction keys.

Treat these as expected debt, not failure — but fix early to avoid compounding confusion.

---

## 8) Operating Rules for Agents (Claude/OpenClaw/etc.) 🤖🧷

### 8.1 “No guessing” standard
Agents must not:
- invent files, paths, endpoints, keys, or credentials  
- write “facts” into memory without evidence  
- broaden scope without explicit instruction  

### 8.2 Preferred change style
- small commits / small diffs  
- verify runtime after changes  
- keep compatibility with telnet loop while refactoring  

### 8.3 Stop conditions (agent must pause and report)
- unclear source of truth  
- contradictions between policy and code behavior  
- uncertain file ownership / scope boundary  

---

## 9) Practical Build Roadmap (Short) 🛠️

### Phase 1 — Stabilize the skeleton ✅
- Normalize imports and module layout (server/world/core/persistence)
- Add minimal test harness: “boot server → connect → run look → quit”
- Confirm save/load cycle works

### Phase 2 — AI NPC v0 🤝
- Implement a **brain adapter interface**
- Add a single NPC with:
  - scripted baseline behavior  
  - optional LLM-driven emotes/actions behind strict rules  

### Phase 3 — Truth‑bound memory 🧾
- Add a **memory write gate** that enforces policy tiers  
- Add an **audit log**: what wrote, why, evidence pointer, timestamp  

---

## 10) Workspace Map (MUD_AI_WORKSPACE collection) 🗂️
The keystone notes an additional “collected workspace” intended to centralize scattered MUD artifacts:

- **Location:** `C:\Users\wilds\MUD_AI_WORKSPACE\COLLECTED`
- **Index:** `COLLECTED/INDEX.md`
- **Key folders (as recorded):**
  - `01_MUD_SERVER_CODE`
  - `02_BRUCEOPS_AI_AGENTS`
  - `03_AVENDAR_LORE_DATA`
  - `04_DOCUMENTATION`
  - `06_HARRISWILDLANDS_WEB`
  - `07_NEO4J_KNOWLEDGE_GRAPH`
- **Top artifacts (from the INDEX list in keystone):**
  - `server.py`, `bruce_agent.py`, `avendar_wiki_lore.json`
  - `MASTER_BUILD_DOCUMENT.md`, `bruceops_mcp_server_v1.2.py`

**Operator note:** treat the workspace map as a navigation spine; don’t assume all files exist in current working directory unless verified.

---

## 11) Safety Protocol Add‑Ons (Relevant project docs) 🧷🛡️

### 11.1 Drift Detection System (pattern flags, not advice)
The project includes a drift detection ruleset designed to:
- detect patterns over multiple days
- output concise, factual, one‑sentence flags
- preserve separation between **observation** and **decision-making**

This is directly compatible with the “Witness, not storyteller” principle.

### 11.2 Brother Collaboration Protocol (selective sharing)
If collaboration is in scope, the project also includes guardrails for:
- ownership of data (each man owns his own data)
- summaries only (no raw transcripts)
- red-zone exclusions (family private details, prayer content, etc.)
- low-friction pause/exit clause

This is aligned with consent-first and anti-surveillance boundaries.

### 11.3 Life Operations Steward Protocols (workflow discipline)
Supporting steward documents define:
- factual summary → signals → tags → open loops
- synthesis rules (daily/weekly) that avoid fabrication
- voice logging green zones vs red zones
- “do not backfill” and “do not moralize” constraints

Even if the Telnet MUD is the focus, these protocols are useful as **operator standards** for any AI “witness” layer.

---

## 12) Glossary (Shared Words) 📚
- **Canon:** curated truths; stable lore or rules  
- **Observed:** logged facts from runtime, sensors, or explicit input  
- **Hypothesis:** uncertain; must be marked and time-limited  
- **Witness:** records what happened (not a storyteller)  
- **Steward:** protects integrity + boundaries (not a hype engine)  
- **Seam:** narrow interface where AI suggests actions  

---

## Appendix A — Copy/Paste “Operator Summary” (for handoffs) 📌
**What exists:** Python telnet MUD skeleton + core models + persistence + truth-policy docs, plus a separate HarrisWildlands.com web app track described in the keystone.  
**What runs (MUD):** `localhost:9999` telnet server (see server file).  
**AI seam:** NPC controller hook + server “brain call” placeholder.  
**Non-negotiable:** Canon/Observed/Hypothesis gating for any memory/lore write.  
**Next sane step:** stabilize imports + add minimal boot/connect test → then AI NPC v0.

---

## Appendix B — Minimal “Boot → Connect → Look → Quit” Test Script (manual) ✅
This is a **human-run** test harness (no automation required):

1) Start server
2) Telnet connect to `localhost 9999`
3) Type: `look`
4) Confirm output is not blank / not error
5) Type: `quit`
6) Confirm server remains stable (or exits cleanly, depending on design)

Record results as Observed (timestamp + what happened).

---

*End of field manual.*
