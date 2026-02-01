# MUD/AI Artifact Collection Index

This folder contains organized artifacts from the Harris Wildlands AI-MUD project ecosystem.

**Collection Date:** 2026-01-19 (updated 2026-02-01)
**Total Files:** 180+
**Total Size:** ~12MB (excluding Mudlet logs ~9MB)

---

## Folder Structure

```
COLLECTED/
├── 01_MUD_SERVER_CODE/      # Python MUD server implementations
├── 02_BRUCEOPS_AI_AGENTS/   # Bruce AI agent system & MCP servers
├── 03_AVENDAR_LORE_DATA/    # JSON lore databases & conversation exports
├── 04_DOCUMENTATION/        # Project docs, READMEs, vision documents
├── 05_MUDLET_PANTHEON_LOGS/ # Raw MUD session logs (Avendar gameplay)
├── 06_HARRISWILDLANDS_WEB/  # Web platform configs & deployment guides
├── 07_NEO4J_KNOWLEDGE_GRAPH/# Graph database driver & setup
├── 08_BRUCEOPS_TECHNICAL_DOCS/ # 18-vol technical manual, user/operator/dev guides
├── 09_CLAUDE_INTEGRATION/   # Claude Desktop integration & MCP setup guides
└── 10_AI_COLLAB/            # AI collaboration setup, cost analysis, roadmap
```

---

## Instructions for Claude Desktop

### Quick Start
1. Point Claude Desktop to this `COLLECTED/` folder as a project directory
2. Start with `04_DOCUMENTATION/MASTER_BUILD_DOCUMENT.md` for system overview
3. Reference `03_AVENDAR_LORE_DATA/avendar_wiki_lore.json` for world lore

### Key Entry Points by Task

**To understand the MUD server architecture:**
```
Read: 01_MUD_SERVER_CODE/server.py
Read: 01_MUD_SERVER_CODE/harriswildlands_ai.py
Read: 04_DOCUMENTATION/CLAUDE.md
```

**To understand the Bruce AI agent system:**
```
Read: 02_BRUCEOPS_AI_AGENTS/bruce_agent.py
Read: 02_BRUCEOPS_AI_AGENTS/BRUCEOPS_COMPLETE_SYSTEM_GUIDE.md
Read: 02_BRUCEOPS_AI_AGENTS/bruceops_mcp_server_v1.2.py
```

**To work with Avendar lore/world data:**
```
Read: 03_AVENDAR_LORE_DATA/avendar_wiki_lore.json
Read: 05_MUDLET_PANTHEON_LOGS/ (any .txt file for raw gameplay)
```

**To understand the knowledge graph system:**
```
Read: 07_NEO4J_KNOWLEDGE_GRAPH/neo4j_driver.py
Read: 02_BRUCEOPS_AI_AGENTS/ingest_canon.py
Read: 02_BRUCEOPS_AI_AGENTS/validate_fact.py
```

**To deploy or extend the web platform:**
```
Read: 06_HARRISWILDLANDS_WEB/DEPLOYMENT_CHECKLIST.md
Read: 06_HARRISWILDLANDS_WEB/REPLIT_UPDATE_PROMPT.md
Read: 06_HARRISWILDLANDS_WEB/openapi.json
Read: 06_HARRISWILDLANDS_WEB/brucebruce_codex/MCP_v1_README.md
```

**To read the comprehensive technical manual:**
```
Read: 08_BRUCEOPS_TECHNICAL_DOCS/00-start-here/00-overview-and-reading-paths.md
Read: 08_BRUCEOPS_TECHNICAL_DOCS/manual/TECHNICAL_MANUAL.md
Read: 08_BRUCEOPS_TECHNICAL_DOCS/manual/VOL01_EXECUTIVE_OVERVIEW.md (through VOL18)
```

**To set up Claude Desktop integration:**
```
Read: 09_CLAUDE_INTEGRATION/READ_THIS_FIRST.md
Read: 09_CLAUDE_INTEGRATION/INSTALLATION_GUIDE.md
Read: 09_CLAUDE_INTEGRATION/QUICK_START_CHECKLIST.md
```

**To understand AI collaboration setup:**
```
Read: 10_AI_COLLAB/DUAL_ACCESS_SETUP.md
Read: 10_AI_COLLAB/COST_ANALYSIS_CLAUDE_DESKTOP.md
Read: 10_AI_COLLAB/UPGRADE_ROADMAP_v1.0.md
```

**To understand the Neo4j schema:**
```
Read: 07_NEO4J_KNOWLEDGE_GRAPH/create_schema.cypher
Read: 07_NEO4J_KNOWLEDGE_GRAPH/neo4j_driver.py
```

---

## Top 30 Artifacts Ranked by Importance

| Rank | File | What It Is | Why It Matters |
|------|------|------------|----------------|
| 1 | `01_MUD_SERVER_CODE/server.py` | Main MUD server (35KB) | Core game loop, rooms, NPCs, AI integration |
| 2 | `02_BRUCEOPS_AI_AGENTS/bruce_agent.py` | Bruce AI agent (15KB) | Autonomous AI companion with Neo4j memory |
| 3 | `03_AVENDAR_LORE_DATA/avendar_wiki_lore.json` | Lore database (47KB) | Room descriptions, NPC data, class info |
| 4 | `04_DOCUMENTATION/MASTER_BUILD_DOCUMENT.md` | Build guide (14KB) | System architecture & setup instructions |
| 5 | `02_BRUCEOPS_AI_AGENTS/bruceops_mcp_server_v1.2.py` | MCP server (21KB) | Claude Desktop integration endpoint |
| 6 | `02_BRUCEOPS_AI_AGENTS/BRUCEOPS_COMPLETE_SYSTEM_GUIDE.md` | System guide (18KB) | Full BruceOps architecture documentation |
| 7 | `04_DOCUMENTATION/PROJECT_OVERVIEW.md` | Project overview (21KB) | High-level system description |
| 8 | `07_NEO4J_KNOWLEDGE_GRAPH/neo4j_driver.py` | Graph driver (10KB) | Knowledge graph CRUD operations |
| 9 | `02_BRUCEOPS_AI_AGENTS/distillation_cron.py` | Memory distiller (11KB) | Compresses conversation history |
| 10 | `01_MUD_SERVER_CODE/harriswildlands_ai.py` | AI game loop (8KB) | Simplified AI-focused MUD version |
| 11 | `02_BRUCEOPS_AI_AGENTS/ingest_canon.py` | Canon ingester (7KB) | Imports lore into knowledge graph |
| 12 | `02_BRUCEOPS_AI_AGENTS/validate_fact.py` | Fact validator (8KB) | Checks facts against canon |
| 13 | `04_DOCUMENTATION/HARRISWILDLANDS_AMBIENT_WITNESS_MASTER_VISION_v3.md` | Vision doc (29KB) | Long-term project vision |
| 14 | `04_DOCUMENTATION/BruceOps_Codebase_Reference.md` | Code reference (36KB) | Detailed codebase documentation |
| 15 | `04_DOCUMENTATION/BruceOps_Architecture_Documentation.md` | Architecture (26KB) | System design patterns |
| 16 | `01_MUD_SERVER_CODE/patched_server.py` | Patched server (35KB) | Bug-fixed server version |
| 17 | `02_BRUCEOPS_AI_AGENTS/BruceBruce_Project_Closeout.md` | Closeout doc (19KB) | Project status & learnings |
| 18 | `02_BRUCEOPS_AI_AGENTS/bruceops_mcp_server.py` | MCP v1 (19KB) | Earlier MCP server version |
| 19 | `01_MUD_SERVER_CODE/avendar_offline.py` | Wiki scraper (9KB) | Generates offline lore database |
| 20 | `04_DOCUMENTATION/EXECUTIVE_SUMMARY.md` | Executive summary (10KB) | Quick project overview |
| 21 | `02_BRUCEOPS_AI_AGENTS/bruceops-ai-endpoints.ts` | AI endpoints (11KB) | TypeScript API definitions |
| 22 | `04_DOCUMENTATION/DOCUMENTATION_INDEX.md` | Doc index (10KB) | Documentation navigation |
| 23 | `06_HARRISWILDLANDS_WEB/REPLIT_UPDATE_PROMPT.md` | Replit prompt (14KB) | Web deployment instructions |
| 24 | `03_AVENDAR_LORE_DATA/group_chats.json` | Chat export (185KB) | Historical Bruce conversations |
| 25 | `02_BRUCEOPS_AI_AGENTS/INTEGRATION_PATCH.py` | Integration (6KB) | System integration helpers |
| 26 | `06_HARRISWILDLANDS_WEB/MORNING_BRIEFING_SETUP.md` | Briefing setup (10KB) | Daily AI briefing config |
| 27 | `01_MUD_SERVER_CODE/Harris_Wildlands_Server.py` | Modular server (8KB) | Cleaner server architecture |
| 28 | `04_DOCUMENTATION/CLAUDE.md` | Claude guide (4KB) | AI assistant context file |
| 29 | `06_HARRISWILDLANDS_WEB/brucebruce_codex/MCP_v1_README.md` | MCP readme (6KB) | MCP setup documentation |
| 30 | `04_DOCUMENTATION/requirements.txt` | Dependencies (501B) | Python package requirements |

---

## Timeline (Based on File Timestamps)

| Period | Activity |
|--------|----------|
| **Jul-Aug 2025** | Initial Mudlet/PANTHEON gameplay sessions, Avendar exploration |
| **Dec 2025** | BruceBruce conversation exports, early AI integration |
| **Jan 1-4 2026** | Major BruceOps development, MCP server creation, web platform |
| **Jan 5-6 2026** | AI MUD playground setup, server patches, lore JSON creation |
| **Jan 17-18 2026** | Neo4j integration, knowledge graph setup, bruce_agent refinement |

---

## Linkages Between Components

```
[Mudlet Logs] ──parse──> [avendar_wiki_lore.json] ──load──> [server.py]
                                   │
                                   v
                         [ingest_canon.py] ──write──> [Neo4j Graph]
                                   │
                                   v
                         [bruce_agent.py] ──query──> [validate_fact.py]
                                   │
                                   v
                         [bruceops_mcp_server.py] ──expose──> [Claude Desktop]
```

---

## Missing Gaps (Potential Future Collection)

1. **tbaMUD source** - No tbaMUD codebase found; may be referenced but not present
2. **Brother Bruce/brosephbrucebuckin SPLASH era** - No explicit files found with these names
3. **Original Avendar wiki HTML** - Only parsed JSON exists, raw HTML not collected
4. **Neo4j database dump** - Driver exists but no graph export/backup
5. **Replit full source export** - 159MB tar.gz at `C:\Users\wilds\HARRISWILDLANDS\90_VAULT_RAW\replit\ReplitExport-brosephharris.tar.gz`
6. **Conceptual .docx files** - ThinkOps, LifeOps, Drift Detection, Semantic Memory at `C:\Users\wilds\AI MUD playground\`
7. **Braindump transcripts** - 129KB JSON at `C:\Users\wilds\Desktop\braindump_transcripts_extract.json`
8. **Project reports** - HarrisWildlands_Project_Report.md (39KB), Technical Manual Prompt (29KB) in Downloads

---

## Usage with Claude Desktop MCP

To connect Bruce to Claude Desktop, use the MCP server:

```bash
# Install dependencies
pip install -r 04_DOCUMENTATION/requirements.txt

# Run MCP server
python 02_BRUCEOPS_AI_AGENTS/bruceops_mcp_server_v1.2.py
```

Then configure Claude Desktop's `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "bruceops": {
      "command": "python",
      "args": ["path/to/COLLECTED/02_BRUCEOPS_AI_AGENTS/bruceops_mcp_server_v1.2.py"]
    }
  }
}
```

---

## File Count by Category

| Folder | Files | Size |
|--------|-------|------|
| 01_MUD_SERVER_CODE | 10 | ~122KB |
| 02_BRUCEOPS_AI_AGENTS | 15 | ~160KB |
| 03_AVENDAR_LORE_DATA | 7 | ~326KB |
| 04_DOCUMENTATION | 18 | ~250KB |
| 05_MUDLET_PANTHEON_LOGS | 37 | ~9MB |
| 06_HARRISWILDLANDS_WEB | 11 | ~80KB |
| 07_NEO4J_KNOWLEDGE_GRAPH | 3 | ~15KB |
| 08_BRUCEOPS_TECHNICAL_DOCS | 50+ | ~300KB |
| 09_CLAUDE_INTEGRATION | 12 | ~60KB |
| 10_AI_COLLAB | 6 | ~100KB |

---

## New Folders Added (2026-02-01 Tier 1 Integration)

### 08_BRUCEOPS_TECHNICAL_DOCS/
Comprehensive BruceOps documentation tree from `harriswildlands.com/BRUCE_BRUCE/docs/`:
- `00-start-here/` - Overview and glossary
- `10-user-guide/` - Quickstart, LifeOps, ThinkOps, weekly review, troubleshooting
- `20-operator-guide/` - Deployment, config, security, disaster recovery
- `30-developer-reference/` - Architecture, API routes, DB schema, auth, AI provider ladder
- `40-protocols-and-governance/` - LifeOps/ThinkOps separation, drift detection, privacy, safety
- `50-releases-and-evidence/` - Keystone v1.0, acceptance tests, changelog
- `manual/` - 18-volume technical manual (VOL01 through VOL18)
- Top-level: ARCHITECTURE.md, CODEBASE.md, ENHANCEMENTS.md, STANDALONE.md, etc.

### 09_CLAUDE_INTEGRATION/
Claude Desktop setup and MCP integration guides from `BRUCE_BRUCE/brucebruce codex/CLAUDE/`:
- Installation guide, visual placement guide, quick start checklist
- Replit agent/MCP prompts, master prompts
- AI_ENDPOINTS_COMPLETE.ts (TypeScript endpoint definitions)

### 10_AI_COLLAB/
AI collaboration infrastructure docs from `Desktop/ai collab/`:
- Dual access setup, implementation guide, Replit agent prompt
- Cost analysis for Claude Desktop, upgrade roadmap v1.0

### New files in existing folders:
- **02_BRUCEOPS_AI_AGENTS**: analyze.py (LiDAR), smoke_test.py (MCP hardening), bootstrap_hw_bridge.py (AI bridge)
- **04_DOCUMENTATION**: INTEGRATION_GUIDE.md, CLAUDE_PROJECT_INSTRUCTIONS.md, wilds-directory-map.md, PATCH_v1.0.md
- **06_HARRISWILDLANDS_WEB**: openapi.json (API spec), .env.example, .replit, OPENCLAW_INTEGRATION_GUIDE.md, CHECKIN_GOAL_INTEGRATION_GUIDE.md, COMPLETE_FILE_REFERENCE.md
- **07_NEO4J_KNOWLEDGE_GRAPH**: create_schema.cypher (Neo4j schema definition)

---

*Generated by Claude Code collection task (updated 2026-02-01)*
