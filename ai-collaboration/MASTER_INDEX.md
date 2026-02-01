# MASTER INDEX

Complete navigation and quick reference for the HarrisWildlands/BruceOps integrated system.

## 🚀 Quick Start

### For Development:
```bash
cd harriswildlands
npm install
npm run dev
```

### For OpenClaw/Discord:
```bash
cd integrations/openclaw
# Gateway already configured at http://127.0.0.1:18789
```

### For Claude Desktop (MCP):
```bash
cd integrations/mcp
python bruceops_mcp_server.py
```

## 📁 Directory Structure

```
structure/
├── harriswildlands/          # Main application
│   ├── server/              # Express backend
│   ├── client/              # React frontend  
│   ├── shared/              # TypeScript schemas
│   ├── docs/manual/         # 18-volume manual
│   └── database/            # Schema & config
│
├── integrations/            # All integrations
│   ├── openclaw/            # Discord bot
│   ├── mcp/                 # Claude Desktop server
│   └── claude/              # Claude Code configs
│
├── deployment/              # Infrastructure
│   ├── docker/              # Container configs
│   ├── scripts/             # Setup scripts
│   └── config/              # Environment templates
│
├── ai-collaboration/        # AI-optimized docs
│   ├── MASTER_INDEX.md      # This file
│   ├── SYSTEM_OVERVIEW.md   # Architecture
│   ├── API_REFERENCE.md     # All endpoints
│   ├── DATABASE_SCHEMA.md   # Data models
│   └── INTEGRATION_GUIDE.md # How to extend
│
└── analysis/                # Deep analysis
    ├── api/                 # Endpoint catalog
    ├── schema/              # Data relationships
    └── tech-stack/          # Dependencies
```

## 📚 Documentation Guide

### For First-Time Setup:
1. Read: `harriswildlands/docs/README.md`
2. Setup: `deployment/scripts/setup.sh`
3. Start: `npm run dev`

### For Development:
1. Architecture: `ai-collaboration/SYSTEM_OVERVIEW.md`
2. API Reference: `ai-collaboration/API_REFERENCE.md`
3. Database: `ai-collaboration/DATABASE_SCHEMA.md`

### For Integration:
1. OpenClaw: `integrations/openclaw/bruceops/SKILL.md`
2. MCP: `integrations/mcp/README.md`
3. Claude Code: `ai-collaboration/claude/AGENTS.md`

### For Operations:
1. User Guide: `harriswildlands/docs/10-user-guide/`
2. Operator Guide: `harriswildlands/docs/20-operator-guide/`
3. Manual (18 vol): `harriswildlands/docs/manual/`

## 🔗 Quick Links

### Core Application
- **Backend**: `harriswildlands/server/routes.ts` (69KB - all endpoints)
- **Frontend**: `harriswildlands/client/src/App.tsx`
- **Schema**: `harriswildlands/shared/schema.ts`
- **Config**: `harriswildlands/package.json`

### Integrations
- **Discord Bot**: `integrations/openclaw/openclaw.json`
- **MCP Server**: `integrations/mcp/bruceops_mcp_server_v1.2.py`
- **Skills**: `integrations/openclaw/bruceops/SKILL.md`

### Documentation
- **Manual Vol 01**: `harriswildlands/docs/manual/VOL01_EXECUTIVE_OVERVIEW.md`
- **API Catalog**: `harriswildlands/docs/manual/VOL06_API_CATALOG.md`
- **AI Integration**: `harriswildlands/docs/manual/VOL07_AI_INTEGRATION.md`

## 🎯 Common Tasks

### Add New API Endpoint
1. Edit: `harriswildlands/server/routes.ts`
2. Add schema: `harriswildlands/shared/schema.ts`
3. Update docs: `ai-collaboration/API_REFERENCE.md`
4. Test: `npm run dev`

### Create OpenClaw Skill
1. Create tool: `integrations/openclaw/bruceops/tools/`
2. Update SKILL.md: `integrations/openclaw/bruceops/SKILL.md`
3. Reload: `openclaw skills reload`

### Database Migration
1. Edit schema: `harriswildlands/shared/schema.ts`
2. Run: `npm run db:push`
3. Update: `ai-collaboration/DATABASE_SCHEMA.md`

## 🔐 Secrets & Configuration

**Environment Variables** (in respective .env files):
- OpenAI API Key
- Discord Bot Token
- BruceOps API Token
- Database connection strings

**Config Files**:
- `harriswildlands/.env.example`
- `integrations/openclaw/.env`
- `integrations/openclaw/openclaw.json`

## 🧠 AI Context

### For Claude Code:
- Primary instructions: `ai-collaboration/claude/AGENTS.md`
- Development workflows: `ai-collaboration/INTEGRATION_GUIDE.md`

### For OpenClaw:
- Skill definition: `integrations/openclaw/bruceops/SKILL.md`
- Available tools: `integrations/openclaw/bruceops/tools/`

## 📊 Statistics

- **Documentation**: 100+ markdown files
- **Manual**: 18 volumes
- **API Endpoints**: 50+ (in routes.ts)
- **Database Tables**: 8+ entities
- **Lines of Code**: ~10,000+ (excluding docs)

## 🆘 Support

- **OpenClaw Docs**: https://docs.openclaw.ai/
- **Dashboard**: http://127.0.0.1:18789
- **BruceOps**: http://localhost:5000

---

**Version**: 1.0  
**Last Updated**: 2026-02-01  
**Status**: Production Ready
