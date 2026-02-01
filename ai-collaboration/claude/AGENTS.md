# AGENTS.md

Claude Code integration instructions for HarrisWildlands.com / BruceOps development.

## 🤖 Agent Identity

**You are**: A specialized development assistant for BruceOps  
**Purpose**: Help build, extend, and maintain the HarrisWildlands personal operating system  
**Context**: Full-stack TypeScript application with AI integrations  
**User**: Bruce Harris - teacher, dad, creator

---

## 📋 Project Context

### What is BruceOps?
BruceOps is a personal operating system with four domains:
1. **LifeOps** - Daily logging (energy, stress, mood, vices)
2. **ThinkOps** - Idea pipeline (capture → reality check → promotion)
3. **Goals** - Weekly goal tracking across 8 life domains
4. **Teaching** - AI lesson planning for 5th/6th grade

### Tech Stack
- **Backend**: Express.js + TypeScript
- **Frontend**: React + Vite + Tailwind
- **Database**: PostgreSQL + Drizzle ORM
- **AI**: Gemini + OpenRouter + OpenAI (ladder)
- **Integrations**: OpenClaw (Discord), MCP (Claude Desktop)

---

## 🗂️ Key Files & Directories

### Backend (Critical)
```
harriswildlands/server/
├── routes.ts          # ALL API endpoints (69KB) - START HERE
├── storage.ts         # Database abstraction (18KB)
├── db.ts             # Database connection
├── index.ts          # Express setup
└── replit_integrations/auth/  # Dual authentication
```

### Frontend
```
harriswildlands/client/src/
├── App.tsx           # Main router
├── pages/            # Page components
│   ├── Dashboard.tsx
│   ├── LifeOps.tsx
│   ├── ThinkOps.tsx
│   └── Goals.tsx
├── components/       # Reusable UI
└── lib/queryClient.ts # API client
```

### Schemas (Type Safety)
```
harriswildlands/shared/
├── schema.ts         # Database tables
├── routes.ts         # API types
└── models/auth.ts    # User models
```

### Integrations
```
integrations/
├── openclaw/bruceops/     # Discord bot skill
├── mcp/bruceops_mcp_server_v1.2.py  # Claude Desktop
└── claude/AGENTS.md       # This file
```

---

## 🎯 Common Development Tasks

### 1. Adding a New API Endpoint

**Steps**:
1. Add route handler in `server/routes.ts`
2. Add Zod schema in `shared/schema.ts` (if new data type)
3. Add storage method in `server/storage.ts` (if needed)
4. Test with `npm run dev`

**Example**:
```typescript
// In server/routes.ts
app.get("/api/custom-endpoint", isAuthenticated, async (req, res) => {
  const userId = getUserId(req);
  const data = await storage.getCustomData(userId);
  res.json(data);
});
```

### 2. Adding a Database Table

**Steps**:
1. Add table definition in `shared/schema.ts`
2. Run `npm run db:push` to create table
3. Add storage methods in `server/storage.ts`
4. Create API endpoints in `server/routes.ts`
5. Update `ai-collaboration/DATABASE_SCHEMA.md`

**Example**:
```typescript
// In shared/schema.ts
export const newTable = pgTable("new_table", {
  id: serial("id").primaryKey(),
  userId: text("user_id").notNull(),
  data: text("data"),
  createdAt: timestamp("created_at").defaultNow()
});
```

### 3. Creating an OpenClaw Skill Tool

**Steps**:
1. Create tool file: `integrations/openclaw/bruceops/tools/my-tool.js`
2. Update SKILL.md with documentation
3. Reload skills: `openclaw skills reload`

**Template**:
```javascript
#!/usr/bin/env node
const { bruceopsRequest } = require("../lib/api-client");

async function main() {
  const result = await bruceopsRequest("/api/my-endpoint");
  console.log(JSON.stringify(result, null, 2));
}

main();
```

### 4. Adding a React Component

**Steps**:
1. Create component: `client/src/components/MyComponent.tsx`
2. Use existing UI patterns (Tailwind + Radix)
3. Add to page or route

**Pattern**:
```typescript
import { Card, CardHeader, CardContent } from "@/components/ui/card";

export function MyComponent() {
  return (
    <Card>
      <CardHeader>Title</CardHeader>
      <CardContent>Content</CardContent>
    </Card>
  );
}
```

### 5. Integrating AI Features

**Steps**:
1. Use existing AI infrastructure in `server/routes.ts`
2. Add to AI provider ladder if needed
3. Follow caching pattern (24-hour cache)
4. Respect quota limits

**Pattern**:
```typescript
const cached = await getCachedAIResponse(cacheKey);
if (cached) return cached;

const response = await callAIProvider(prompt);
await cacheAIResponse(cacheKey, response);
return response;
```

---

## 🔄 Development Workflow

### Starting Development
```bash
cd harriswildlands
npm install        # If needed
npm run dev        # Start dev server
# Server: http://localhost:5000
```

### Type Checking
```bash
npm run check      # TypeScript validation
```

### Database Changes
```bash
npm run db:push    # Apply schema changes
```

### Testing
```bash
# Manual testing via browser or curl
curl http://localhost:5000/api/health
```

---

## 📝 Documentation Standards

### When to Update Docs
- **Always** update when adding endpoints
- **Always** update when changing schema
- **Always** update when adding skills

### Where to Update
- API changes → `ai-collaboration/API_REFERENCE.md`
- Schema changes → `ai-collaboration/DATABASE_SCHEMA.md`
- New features → `ai-collaboration/INTEGRATION_GUIDE.md`
- Major changes → `harriswildlands/docs/manual/` (18 volumes)

### Code Comments
```typescript
// GOOD: Explain the "why"
// Cache for 24 hours to reduce AI costs
const cacheKey = createHash('sha256').update(prompt).digest('hex');

// BAD: Obvious comments
// Create a hash (duh!)
const hash = createHash('sha256');
```

---

## 🎨 Code Style

### TypeScript
- **Always** use explicit types for function parameters
- **Always** use interfaces for object shapes
- **Never** use `any` unless absolutely necessary

### React
- Use functional components
- Use hooks (useState, useEffect, useQuery)
- Keep components small and focused

### API Design
- Use REST conventions
- Return consistent JSON structure
- Use proper HTTP status codes

---

## 🔐 Security Checklist

Before committing code:
- [ ] No hardcoded secrets (use .env)
- [ ] User scoping applied (userId filter)
- [ ] Input validation (Zod schemas)
- [ ] Rate limiting considered
- [ ] No SQL injection vulnerabilities

---

## 🐛 Debugging Tips

### Server Issues
```bash
# Check if server is running
curl http://localhost:5000/api/health

# View logs
npm run dev 2>&1 | tee server.log
```

### Database Issues
```bash
# Check schema
npm run db:push -- --dry-run

# View tables (if psql available)
psql -h localhost -U postgres -d harriswildlands -c "\dt"
```

### TypeScript Errors
```bash
# Full type check
npm run check

# Often just need to restart TS server in IDE
```

---

## 🔗 Integration Points

### OpenClaw (Discord)
- **Config**: `integrations/openclaw/openclaw.json`
- **Skills**: `integrations/openclaw/bruceops/`
- **Reload**: `openclaw skills reload`

### MCP (Claude Desktop)
- **Server**: `integrations/mcp/bruceops_mcp_server_v1.2.py`
- **Setup**: See `integrations/mcp/SETUP_INSTRUCTIONS.md`

### Database
- **Schema**: `harriswildlands/shared/schema.ts`
- **Migrations**: `npm run db:push`

---

## 📚 Essential Reading

### Must Read First
1. `ai-collaboration/MASTER_INDEX.md` - Navigation
2. `ai-collaboration/SYSTEM_OVERVIEW.md` - Architecture
3. `server/routes.ts` - All endpoints (skim to understand scope)

### Reference
- `ai-collaboration/API_REFERENCE.md` - Endpoint details
- `ai-collaboration/DATABASE_SCHEMA.md` - Data models
- `harriswildlands/docs/manual/VOL06_API_CATALOG.md` - Original API docs

### Integration
- `integrations/openclaw/bruceops/SKILL.md` - OpenClaw skill
- `integrations/mcp/README.md` - MCP server

---

## 🎯 Success Metrics

Code is ready when:
- ✅ TypeScript compiles without errors
- ✅ API responds correctly
- ✅ Database schema updated
- ✅ Documentation updated
- ✅ Tested manually

---

## 🆘 Getting Help

### Documentation
- **Full Manual**: `harriswildlands/docs/manual/` (18 volumes)
- **API Docs**: `ai-collaboration/API_REFERENCE.md`
- **Schema**: `ai-collaboration/DATABASE_SCHEMA.md`

### External
- **OpenClaw**: https://docs.openclaw.ai/
- **Drizzle**: https://orm.drizzle.team/
- **Express**: https://expressjs.com/

---

**Agent Version**: 1.0  
**Last Updated**: 2026-02-01  
**Status**: Active Development
