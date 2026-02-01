# HarrisWildlands / BruceOps Complete Structure

**A complete, modular, working copy of the HarrisWildlands personal operating system, optimized for AI collaboration.**

---

## 🚀 Quick Start

### Prerequisites
- Node.js 20+
- PostgreSQL 14+
- npm or pnpm

### Development Setup
```bash
# 1. Navigate to application
cd harriswildlands

# 2. Install dependencies
npm install

# 3. Configure environment
cp .env.example .env
# Edit .env with your values

# 4. Initialize database
npm run db:push

# 5. Start development server
npm run dev

# 6. Open browser
open http://localhost:5000
```

### Production Setup (Docker)
```bash
# Start everything
cd deployment/docker
docker-compose up --build

# Access application
open http://localhost:5000
```

---

## 📁 Project Structure

```
structure/
├── 📁 harriswildlands/          # Main Application
│   ├── 📁 server/              # Express backend
│   │   ├── routes.ts           # All 50+ API endpoints
│   │   ├── storage.ts          # Database layer
│   │   └── index.ts            # Server entry
│   │
│   ├── 📁 client/              # React frontend
│   │   ├── src/pages/          # Page components
│   │   ├── src/components/     # UI components
│   │   └── src/hooks/          # Custom hooks
│   │
│   ├── 📁 shared/              # TypeScript schemas
│   │   ├── schema.ts           # Database tables
│   │   └── routes.ts           # API types
│   │
│   ├── 📁 docs/                # Complete documentation
│   │   ├── manual/             # 18-volume manual
│   │   ├── 00-start-here/      # Getting started
│   │   ├── 10-user-guide/      # User documentation
│   │   └── 30-developer-reference/  # Dev docs
│   │
│   └── 📄 package.json         # Dependencies & scripts
│
├── 📁 integrations/            # All Integrations
│   ├── 📁 openclaw/            # Discord bot
│   │   ├── bruceops/           # Custom skill
│   │   ├── openclaw.json       # Bot config
│   │   └── .env                # Secrets & tokens
│   │
│   ├── 📁 mcp/                 # Claude Desktop
│   │   ├── bruceops_mcp_server_v1.2.py
│   │   └── README.md           # Setup guide
│   │
│   └── 📁 claude/              # Claude Code
│       └── AGENTS.md           # Development instructions
│
├── 📁 deployment/              # Infrastructure
│   ├── 📁 docker/              # Container configs
│   ├── 📁 scripts/             # Setup & start scripts
│   └── 📁 config/              # Environment templates
│
├── 📁 ai-collaboration/        # AI-Optimized Documentation
│   ├── MASTER_INDEX.md         # Navigation hub
│   ├── SYSTEM_OVERVIEW.md      # Architecture
│   ├── API_REFERENCE.md        # All endpoints
│   ├── DATABASE_SCHEMA.md      # Data models
│   ├── INTEGRATION_GUIDE.md    # Extension guide
│   └── 📁 claude/              # Claude-specific docs
│
├── 📁 analysis/                # Deep Analysis
│   ├── 📁 api/                 # Endpoint catalog
│   ├── 📁 schema/              # Data relationships
│   └── 📁 tech-stack/          # Dependencies
│
└── 📄 README.md                # This file
```

---

## 🎯 What is BruceOps?

BruceOps is a **personal operating system** for Bruce Harris (teacher, dad, creator) with four domains:

### 1. LifeOps - Daily Calibration
Track daily metrics:
- **Energy, Stress, Mood** (1-10 scales)
- **Vices**: Vaping, Alcohol, Junk Food, Doom Scrolling
- **Virtues**: Exercise, Family Time, Faith
- **Reflection**: Top Win, Friction, Tomorrow's Priority

### 2. ThinkOps - Ideas Pipeline
Manage ideas from capture to completion:
- **Draft** → Reality Check → **Promoted** → Shipped
- **AI Reality Checks**: Multi-perspective analysis
- **Categories**: Tech, Creative, Business, Personal

### 3. Goals - Accountability System
Weekly goals across 8 life domains:
- Faith, Family, Work, Health
- Logistics, Property, Ideas, Discipline
- **Daily Checkins**: Track progress with notes

### 4. Teaching - AI Assistant
Generate lesson plans for 5th/6th grade:
- Standards-aligned (CCSS)
- AI-powered differentiation
- Activity and assessment ideas

---

## 🤖 AI Integrations

### OpenClaw (Discord Bot)
**Location**: `integrations/openclaw/`

Interact via Discord:
```
@Bruce bruceops-dashboard        # Quick stats
@Bruce bruceops-logs --limit=5   # Recent logs
@Bruce bruceops-ideas            # Idea pipeline
@Bruce bruceops-goals            # Active goals
```

**Setup**:
1. Bot already configured
2. Gateway running on http://127.0.0.1:18789
3. Use invite link to add to your Discord server

### MCP Server (Claude Desktop)
**Location**: `integrations/mcp/`

Python-based server for Claude Desktop integration:
```bash
cd integrations/mcp
python bruceops_mcp_server.py
```

See `integrations/mcp/README.md` for setup.

### Claude Code (VS Code)
**Location**: `ai-collaboration/claude/AGENTS.md`

Development assistance with full project context.

---

## 📚 Documentation

### For First-Time Users
1. `harriswildlands/docs/00-start-here/00-overview-and-reading-paths.md`
2. `harriswildlands/docs/10-user-guide/11-first-run-demo-mode.md`
3. `harriswildlands/docs/10-user-guide/12-lifeops-daily-logging.md`

### For Developers
1. `ai-collaboration/MASTER_INDEX.md` - Start here
2. `ai-collaboration/SYSTEM_OVERVIEW.md` - Architecture
3. `ai-collaboration/API_REFERENCE.md` - All endpoints
4. `ai-collaboration/claude/AGENTS.md` - Development guide

### For Operators
1. `harriswildlands/docs/20-operator-guide/20-standalone-deployment-docker-compose.md`
2. `harriswildlands/docs/20-operator-guide/21-configuration-env.md`
3. `harriswildlands/docs/20-operator-guide/26-disaster-recovery.md`

### Complete Manual (18 Volumes)
Located in `harriswildlands/docs/manual/`:
- VOL01: Executive Overview
- VOL02: Tech Stack
- VOL03: Architecture
- VOL04: File Structure
- VOL05: Database Schema
- VOL06: **API Catalog** (comprehensive)
- VOL07: **AI Integration**
- VOL08: User Workflows
- VOL09: Components
- VOL10: Configuration
- VOL11: Deployment
- VOL12: Security
- VOL13: Extension Patterns
- VOL14: Troubleshooting
- VOL15: Testing
- VOL16: Maintenance
- VOL17: Roadmap
- VOL18: Appendices

---

## 🔐 Secrets & Configuration

**⚠️ IMPORTANT**: Real tokens and secrets are included in this structure.

### Environment Files
- `harriswildlands/.env.example` - Template
- `integrations/openclaw/.env` - Discord bot tokens
- `integrations/openclaw/openclaw.json` - Full OpenClaw config

### Included Secrets
- Discord bot token
- OpenAI API keys
- BruceOps API tokens
- Google API keys

**Security**: Treat this structure as confidential. Do not share publicly.

---

## 🛠️ Development

### Common Commands
```bash
# Type checking
npm run check

# Database operations
npm run db:push      # Apply migrations
npm run db:generate  # Generate migrations

# Build
npm run build        # Production build
npm run start        # Start production server

# Development
npm run dev          # Start dev server with HMR
```

### Adding Features
See `ai-collaboration/INTEGRATION_GUIDE.md` for:
- Adding API endpoints
- Creating database tables
- Building React components
- Creating OpenClaw skills

---

## 📊 Stats & Metrics

- **Lines of Code**: ~10,000+
- **API Endpoints**: 50+
- **Database Tables**: 8
- **Documentation Files**: 100+
- **Manual Volumes**: 18
- **React Components**: 40+
- **OpenClaw Tools**: 8

---

## 🎯 Use Cases

### Personal Use
- Track daily energy, stress, mood
- Manage ideas and projects
- Set and track weekly goals
- Generate AI insights

### Teaching
- Generate lesson plans
- Track teaching metrics
- Manage curriculum ideas

### Development
- Extend the system
- Build new features
- Create integrations

### AI Collaboration
- Use Claude Code for development
- Use OpenClaw for daily operations
- Use MCP for Claude Desktop access

---

## 🆘 Support & Troubleshooting

### Quick Checks
```bash
# Server health
curl http://localhost:5000/api/health

# OpenClaw status
openclaw status

# Database connection
npm run db:push -- --dry-run
```

### Common Issues

**Server won't start**:
- Check port 5000 is free
- Verify PostgreSQL is running
- Check .env configuration

**Discord bot not responding**:
- Verify gateway is running: `openclaw status`
- Check bot is invited to server
- Verify token is valid

**Database errors**:
- Run `npm run db:push`
- Check PostgreSQL connection
- Verify schema is up to date

### Documentation
- **Full Manual**: `harriswildlands/docs/manual/`
- **Troubleshooting**: `harriswildlands/docs/manual/VOL14_TROUBLESHOOTING.md`
- **FAQ**: `harriswildlands/docs/10-user-guide/16-troubleshooting.md`

---

## 🤝 Contributing

This is a personal project, but structured for extension:

1. **Fork/Copy** this structure
2. **Modify** for your needs
3. **Extend** with new features
4. **Document** your changes

See `ai-collaboration/INTEGRATION_GUIDE.md` for extension patterns.

---

## 📜 License

See `harriswildlands/package.json` for license information.

---

## 🙏 Credits

**Built by**: Bruce Harris  
**Purpose**: Personal operating system for life management  
**Tech**: Node.js, React, PostgreSQL, AI integration  
**Status**: Production ready

---

**Structure Version**: 1.0  
**Created**: 2026-02-01  
**Status**: Complete & Ready for Use

🚀 **Ready to start?** See [Quick Start](#-quick-start) above!
