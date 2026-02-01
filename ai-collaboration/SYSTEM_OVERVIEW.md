# SYSTEM OVERVIEW

Complete architecture documentation for HarrisWildlands.com / BruceOps integrated system.

## 🏗️ High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    INTEGRATION LAYER                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐              │
│  │   OpenClaw  │  │     MCP     │  │Claude Code  │              │
│  │   (Discord) │  │   (Desktop) │  │   (VS Code) │              │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘              │
└─────────┼────────────────┼────────────────┼──────────────────────┘
          │                │                │
          ▼                ▼                ▼
┌─────────────────────────────────────────────────────────────────┐
│                      EXPRESS SERVER                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐              │
│  │  Middleware │──│   Routes    │──│   Storage   │              │
│  │    Chain    │  │  (routes.ts)│  │(storage.ts) │              │
│  └─────────────┘  └─────────────┘  └─────────────┘              │
│                                                                  │
│  Dual Auth: Session + Token                                      │
│  Rate Limiting: General + AI-specific                            │
│  Validation: Zod schemas                                         │
└────────────────────────────┬────────────────────────────────────┘
                             │
         ┌───────────────────┼───────────────────┐
         ▼                   ▼                   ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│ PostgreSQL  │     │     AI      │     │   Google    │
│  Database   │     │  Providers  │     │    Drive    │
│  (Drizzle)  │     │ Gemini/OR   │     │    API      │
└─────────────┘     └─────────────┘     └─────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    REACT FRONTEND                                │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐              │
│  │   React     │  │  TanStack   │  │   Wouter    │              │
│  │ Components  │──│   Query     │──│   Router    │              │
│  └─────────────┘  └─────────────┘  └─────────────┘              │
└─────────────────────────────────────────────────────────────────┘
```

## 🎯 Core Components

### 1. Backend (Express + TypeScript)

**Location**: `harriswildlands/server/`

**Key Files**:
- `routes.ts` (69KB) - All 50+ API endpoints
- `storage.ts` (18KB) - Database abstraction layer
- `db.ts` - PostgreSQL connection via Drizzle
- `index.ts` - Express server setup
- `replit_integrations/auth/` - Dual authentication

**Architecture Pattern**:
```
Request → Middleware → Route Handler → Storage → Database
              ↓              ↓             ↓
         Session/Token    Validation   User-scoped
         Rate Limit       Zod          Queries
```

**Authentication Modes**:
1. **Session-based** (Web UI): Cookie-based with Passport.js
2. **Token-based** (MCP/API): Bearer token for external access

### 2. Frontend (React + Vite)

**Location**: `harriswildlands/client/`

**Key Directories**:
- `src/pages/` - Page components (Dashboard, LifeOps, ThinkOps, Goals)
- `src/components/` - Reusable UI components
- `src/hooks/` - Custom React hooks (use-demo.tsx, etc.)
- `src/lib/` - Utilities, query client, API helpers

**Tech Stack**:
- **React 18** - Component library
- **Vite 7** - Build tool with HMR
- **TanStack Query** - Data fetching and caching
- **Wouter** - Routing (lightweight alternative to React Router)
- **Tailwind CSS** - Styling
- **Radix UI** - Headless UI components

### 3. Database (PostgreSQL + Drizzle)

**Location**: `harriswildlands/shared/schema.ts`

**Core Tables**:
- `logs` - Daily LifeOps entries (energy, stress, mood, vices)
- `ideas` - ThinkOps pipeline (draft → reality_check → promoted)
- `goals` - Weekly goals across 8 domains
- `checkins` - Daily goal progress tracking
- `transcripts` - Brainstorming session analysis
- `api_tokens` - Bearer tokens for external access
- `users` - User accounts (Replit Auth or standalone)

**Key Features**:
- User-scoped data (every query filtered by userId)
- Type-safe with Drizzle ORM
- Zod validation for all inputs
- Automatic migrations with drizzle-kit

### 4. AI Integration Layer

**AI Provider Ladder**:
```
1. Google Gemini (primary)
2. OpenRouter GPT-4o-mini (fallback)
3. Off (if no keys configured)
```

**AI Features**:
- **LifeOps Insights**: Pattern detection in daily logs
- **Reality Checks**: AI analysis of ideas before promotion
- **Teaching Assistant**: Lesson plan generation for 5th/6th grade
- **Weekly Synthesis**: Narrative summaries of goal progress
- **Smart Search**: Natural language queries across logs

**Caching**: 24-hour cache with SHA-256 keys to reduce API costs

## 🔗 Integration Points

### OpenClaw (Discord Bot)

**Location**: `integrations/openclaw/`

**Components**:
- `bruceops/` - Custom skill with 8 tools
- `openclaw.json` - Gateway and Discord configuration
- `.env` - Environment variables (Discord token, API keys)

**How It Works**:
1. Discord message triggers OpenClaw gateway
2. Gateway routes to BruceOps skill
3. Skill calls API endpoints via HTTP
4. Response formatted and sent back to Discord

**Available Commands**:
```
@Bruce bruceops-health          # Check API status
@Bruce bruceops-dashboard        # Quick stats
@Bruce bruceops-logs --limit=5   # Recent logs
@Bruce bruceops-ideas            # Idea pipeline
@Bruce bruceops-goals            # Active goals
@Bruce bruceops-weekly-review    # Weekly summary
@Bruce bruceops-ai-search --query="high energy days"
```

### MCP Server (Claude Desktop)

**Location**: `integrations/mcp/`

**Components**:
- `bruceops_mcp_server_v1.2.py` - Python-based MCP server
- `README.md` - Setup instructions
- `SETUP_INSTRUCTIONS.md` - Detailed configuration

**How It Works**:
1. Claude Desktop loads MCP server via configuration
2. Server exposes tools as functions
3. Claude can call tools to interact with BruceOps
4. Token-based authentication for security

**Capabilities**:
- Read logs, ideas, goals
- Create new entries
- Run AI analysis
- Generate reports

### Claude Code (VS Code Extension)

**Location**: `ai-collaboration/claude/`

**Purpose**:
- Development assistance
- Code review and refactoring
- Documentation generation
- Architecture decisions

**Integration**:
- Direct access to source code
- Can run npm commands
- Can modify files
- Full project context via AGENTS.md

## 📊 Data Flow

### Example: Creating a Daily Log

```
1. User Input
   └── Discord: "@Bruce log energy 8 stress 3"
   
2. OpenClaw Processing
   └── Skill: bruceops-log-create
   └── Tool: bruceops-log-create.js
   
3. API Request
   └── POST /api/logs
   └── Headers: Authorization: Bearer <token>
   └── Body: { energy: 8, stress: 3, ... }
   
4. Server Processing
   └── Middleware: isAuthenticated
   └── Validation: Zod schema
   └── Storage: storage.createLog()
   └── Database: INSERT INTO logs
   
5. Response
   └── JSON: { success: true, log: {...} }
   └── Discord: "✅ Log created for 2025-02-01"
```

### Example: AI Reality Check on Idea

```
1. User Input
   └── Discord: "@Bruce reality-check ideaId=123"
   
2. OpenClaw Processing
   └── Skill: bruceops-reality-check
   
3. API Request
   └── POST /api/ideas/123/reality-check
   
4. Server Processing
   └── Fetch idea details from database
   └── Build prompt with idea context
   └── Call AI provider (Gemini → OpenRouter)
   └── Cache result for 24 hours
   └── Store analysis in database
   
5. Response
   └── JSON: { realityCheck: "...", verdict: "promising" }
   └── Discord: Formatted analysis with emoji verdict
```

## 🔐 Security Architecture

### Authentication
- **Dual Mode**: Session (web) + Token (API/MCP)
- **Token Generation**: In Settings page, stored hashed in database
- **Session Storage**: PostgreSQL (production) or Memory (dev)

### Authorization
- **User Scoping**: All queries filtered by userId
- **No Cross-User Data**: Impossible to access other users' data
- **Rate Limiting**: 100 requests/15min general, 10 AI calls/day

### Secrets Management
- **Environment Variables**: All keys in .env files
- **No Hardcoded Secrets**: Never commit keys to git
- **Token Rotation**: API tokens can be regenerated anytime

## 🚀 Deployment Options

### 1. Development (Local)
```bash
npm install
npm run dev
# Server: http://localhost:5000
```

### 2. Docker (Standalone)
```bash
docker-compose up --build
# Includes PostgreSQL + app container
```

### 3. Replit (Cloud)
- Built-in support via `.replit` config
- Automatic environment setup

## 📈 Scalability Considerations

### Current Limits
- **Rate Limiting**: Prevents abuse
- **AI Quota**: 100 calls/day to control costs
- **Caching**: Reduces redundant AI calls

### Scaling Strategies
- **Database**: Can migrate to managed PostgreSQL
- **AI**: Can add more providers to ladder
- **Caching**: Can add Redis for distributed cache
- **CDN**: Can add CloudFront for static assets

## 🔧 Extension Points

### Adding New API Endpoint
1. Add route in `server/routes.ts`
2. Add schema validation in `shared/schema.ts`
3. Add storage method in `server/storage.ts`
4. Test with `npm run dev`

### Adding OpenClaw Skill Tool
1. Create tool in `integrations/openclaw/bruceops/tools/`
2. Update `SKILL.md` with documentation
3. Reload with `openclaw skills reload`

### Adding Database Table
1. Add table in `shared/schema.ts`
2. Run `npm run db:push`
3. Add storage methods
4. Create API endpoints

## 📚 Further Reading

- **API Reference**: `ai-collaboration/API_REFERENCE.md`
- **Database Schema**: `ai-collaboration/DATABASE_SCHEMA.md`
- **Integration Guide**: `ai-collaboration/INTEGRATION_GUIDE.md`
- **Full Manual**: `harriswildlands/docs/manual/` (18 volumes)

---

**Architecture Version**: 1.0  
**Last Updated**: 2026-02-01  
**Status**: Production Ready
