# DATABASE SCHEMA

Complete database documentation for HarrisWildlands.com / BruceOps.

**Database**: PostgreSQL  
**ORM**: Drizzle ORM  
**Type Safety**: Zod validation  
**Migrations**: drizzle-kit

---

## 📊 Entity Relationship Diagram

```
┌─────────────┐       ┌─────────────┐       ┌─────────────┐
│    USERS    │       │    LOGS     │       │   IDEAS     │
├─────────────┤       ├─────────────┤       ├─────────────┤
│ id          │◄──────┤ userId      │       │ userId      │
│ username    │       │ date        │       │ title       │
│ email       │       │ energy      │       │ pitch       │
│ createdAt   │       │ stress      │       │ category    │
└─────────────┘       │ mood        │       │ status      │
                      │ exercise    │       │ excitement  │
                      │ vices...    │       │ feasibility │
                      └─────────────┘       │ priority    │
                                            └─────────────┘
                                                   │
                            ┌──────────────────────┘
                            │
                      ┌─────────────┐
                      │GOAL_CHECKINS│
                      ├─────────────┤
                      │ goalId      │
                      │ date        │
                      │ done        │
                      │ note        │
                      └─────────────┘
                            │
                            ▼
                      ┌─────────────┐
                      │    GOALS    │
                      ├─────────────┤
                      │ userId      │
                      │ title       │
                      │ domain      │
                      │ priority    │
                      │ status      │
                      └─────────────┘
```

---

## 👤 Users Table

**Purpose**: User authentication and profile data  
**Location**: `shared/models/auth.ts` (Replit Auth) or standalone

### Schema
```typescript
users: {
  id: serial("id").primaryKey(),
  username: text("username").notNull(),
  email: text("email"),
  passwordHash: text("password_hash"),  // For standalone mode
  createdAt: timestamp("created_at").defaultNow(),
  updatedAt: timestamp("updated_at").defaultNow()
}
```

**Relationships**:
- One-to-Many with `logs`
- One-to-Many with `ideas`
- One-to-Many with `goals`
- One-to-Many with `checkins`

---

## 📝 Logs Table (LifeOps)

**Purpose**: Daily calibration and life tracking  
**Domain**: LifeOps - Personal metrics and reflection

### Schema
```typescript
logs: {
  // Primary
  id: serial("id").primaryKey(),
  userId: text("user_id").notNull(),
  date: text("date").notNull(),  // YYYY-MM-DD
  
  // Vices (boolean toggles)
  vaping: boolean("vaping").default(false),
  alcohol: boolean("alcohol").default(false),
  junkFood: boolean("junk_food").default(false),
  doomScrolling: boolean("doom_scrolling").default(false),
  lateScreens: boolean("late_screens").default(false),
  skippedMeals: boolean("skipped_meals").default(false),
  excessCaffeine: boolean("excess_caffeine").default(false),
  
  // Virtues
  exercise: boolean("exercise").default(false),
  
  // Life Metrics (1-10 scales)
  energy: integer("energy"),        // 1=crashed, 10=unstoppable
  stress: integer("stress"),        // 1=zen, 10=maxed out
  mood: integer("mood"),            // 1=dark, 10=grateful
  focus: integer("focus"),          // 1=scattered, 10=locked in
  sleepQuality: integer("sleep_quality"),  // 1=terrible, 10=restorative
  sleepHours: integer("sleep_hours"),
  moneyPressure: integer("money_pressure"), // 1=stable, 10=crushing
  connection: integer("connection"), // 1=isolated, 10=connected
  
  // Quick Context (enums)
  dayType: text("day_type"),        // work, rest, family, mixed, chaos
  primaryEmotion: text("primary_emotion"),  // grateful, anxious, hopeful...
  winCategory: text("win_category"), // family, work, health, faith...
  timeDrain: text("time_drain"),    // meetings, distractions, emergencies...
  
  // Reflection Prompts (free text)
  topWin: text("top_win"),
  topFriction: text("top_friction"),
  tomorrowPriority: text("tomorrow_priority"),
  
  // Optional Deep Dives
  familyConnection: text("family_connection"),
  faithAlignment: text("faith_alignment"),
  driftCheck: text("drift_check")
}
```

**Indexes**:
- `userId + date` (unique constraint - one log per day)
- `userId` (for fast user-scoped queries)

**Zod Validation**:
```typescript
insertLogSchema = z.object({
  date: z.string(),
  energy: z.number().min(1).max(10).optional(),
  stress: z.number().min(1).max(10).optional(),
  mood: z.number().min(1).max(10).optional(),
  // ... other fields
})
```

---

## 💡 Ideas Table (ThinkOps)

**Purpose**: Idea capture and pipeline management  
**Domain**: ThinkOps - Innovation and project pipeline

### Schema
```typescript
ideas: {
  id: serial("id").primaryKey(),
  userId: text("user_id").notNull(),
  
  // Core Idea
  title: text("title").notNull(),
  pitch: text("pitch").notNull(),
  category: text("category"),  // tech, creative, business, personal, other
  
  // Pipeline Status
  status: text("status").default("draft"),
  // draft → reality_checked → parked → promoted → shipped → discarded
  
  // Evaluation Scores (1-10)
  excitement: integer("excitement"),
  feasibility: integer("feasibility"),
  priority: integer("priority"),  // 1=high, 2=medium, 3=low
  
  // AI Analysis
  realityCheck: text("reality_check"),  // AI-generated analysis
  verdict: text("verdict"),  // promising, risky, needs_work, reject
  
  // Metadata
  createdAt: timestamp("created_at").defaultNow(),
  updatedAt: timestamp("updated_at").defaultNow(),
  promotedAt: timestamp("promoted_at")
}
```

**Status Flow**:
```
draft → reality_checked → parked
  ↓           ↓              ↓
promoted → shipped        discarded
```

**Indexes**:
- `userId + status` (for pipeline queries)
- `userId + priority` (for sorting)

---

## 🎯 Goals Table

**Purpose**: Weekly goal tracking across life domains  
**Domain**: Goals - Accountability and progress

### Schema
```typescript
goals: {
  id: serial("id").primaryKey(),
  userId: text("user_id").notNull(),
  
  // Goal Definition
  title: text("title").notNull(),
  domain: text("domain").notNull(),
  // faith, family, work, health, logistics, property, ideas, discipline
  
  priority: integer("priority"),  // 1=high, 2=medium, 3=low
  weeklyMinimum: text("weekly_minimum"),  // e.g., "3x per week"
  
  // Status
  status: text("status").default("active"),  // active, completed, paused
  
  // Timeframe
  startDate: text("start_date"),  // YYYY-MM-DD
  endDate: text("end_date"),      // YYYY-MM-DD
  
  // Metadata
  createdAt: timestamp("created_at").defaultNow(),
  updatedAt: timestamp("updated_at").defaultNow()
}
```

**Domains**:
- ✝️ **faith** - Spiritual practices
- 👨‍👩‍👧‍👦 **family** - Family time and relationships
- 💼 **work** - Professional development
- ❤️ **health** - Physical and mental health
- 📋 **logistics** - Administrative tasks
- 🏠 **property** - Home and maintenance
- 💡 **ideas** - Creative projects
- 🎯 **discipline** - Personal habits

**Indexes**:
- `userId + domain` (for domain grouping)
- `userId + status` (for active goals)

---

## ✅ Checkins Table

**Purpose**: Daily goal progress tracking  
**Relationship**: Child of Goals

### Schema
```typescript
checkins: {
  id: serial("id").primaryKey(),
  userId: text("user_id").notNull(),
  goalId: integer("goal_id").notNull(),  // Foreign key to goals
  
  // Checkin Data
  date: text("date").notNull(),  // YYYY-MM-DD
  done: boolean("done").default(false),
  note: text("note"),  // Optional context
  
  // Metadata
  createdAt: timestamp("created_at").defaultNow()
}
```

**Indexes**:
- `userId + goalId + date` (unique - one checkin per goal per day)
- `userId + date` (for daily summaries)

**Query Patterns**:
```sql
-- Get completion rate for a goal
SELECT 
  COUNT(*) as total,
  SUM(CASE WHEN done THEN 1 ELSE 0 END) as completed,
  (SUM(CASE WHEN done THEN 1 ELSE 0 END) * 100.0 / COUNT(*)) as rate
FROM checkins
WHERE goalId = ? AND userId = ?

-- Get missed days in last 7 days
SELECT date
FROM generate_series(CURRENT_DATE - 7, CURRENT_DATE, '1 day') AS date
LEFT JOIN checkins ON checkins.date = date AND goalId = ?
WHERE checkins.id IS NULL OR checkins.done = false
```

---

## 🎙️ Transcripts Table

**Purpose**: Brainstorming session analysis  
**Domain**: ThinkOps - Voice/idea capture

### Schema
```typescript
transcripts: {
  id: serial("id").primaryKey(),
  userId: text("user_id").notNull(),
  
  // Session Data
  source: text("source"),  // "voice", "text", "import"
  rawText: text("raw_text"),  // Original transcript
  
  // AI Analysis
  ideasExtracted: jsonb("ideas_extracted"),  // Array of extracted ideas
  summary: text("summary"),  // AI-generated summary
  actionItems: jsonb("action_items"),  // Array of todos
  
  // Metadata
  createdAt: timestamp("created_at").defaultNow(),
  processedAt: timestamp("processed_at")
}
```

**AI Processing**:
- Extract potential ideas from transcript
- Generate summary
- Identify action items
- Link to existing ideas if mentioned

---

## 🔑 API Tokens Table

**Purpose**: Bearer tokens for external access (MCP, OpenClaw)  
**Security**: Tokens hashed, only shown once on creation

### Schema
```typescript
apiTokens: {
  id: serial("id").primaryKey(),
  userId: text("user_id").notNull(),
  
  // Token Data
  name: text("name").notNull(),  // "OpenClaw Integration"
  tokenHash: text("token_hash").notNull(),  // SHA-256 hash
  tokenPrefix: text("token_prefix"),  // First 8 chars for identification
  
  // Status
  isActive: boolean("is_active").default(true),
  lastUsedAt: timestamp("last_used_at"),
  
  // Metadata
  createdAt: timestamp("created_at").defaultNow(),
  revokedAt: timestamp("revoked_at")
}
```

**Security Features**:
- Tokens shown only once on creation
- Hashed with SHA-256 before storage
- Prefix stored for identification
- Revocable at any time
- Last usage tracked

---

## 🔒 Security Model

### User Scoping
Every table has `userId` field. All queries filtered:
```typescript
// Example: Get user's logs only
const logs = await db
  .select()
  .from(logsTable)
  .where(eq(logsTable.userId, userId));  // Always filtered
```

### Data Isolation
- **Impossible to access other users' data** by design
- No admin view of user data
- Each user sees only their own entries

### Audit Trail
- `createdAt` on all tables
- `updatedAt` on mutable tables
- Token `lastUsedAt` for API access

---

## 🔄 Migration Strategy

### Using Drizzle Kit
```bash
# Generate migration
npm run db:generate

# Apply migration
npm run db:push

# For production (safer)
npm run db:migrate
```

### Migration Files Location
```
harriswildlands/
├── drizzle/
│   ├── 0000_initial.sql
│   ├── 0001_add_checkins.sql
│   └── meta/
│       ├── _journal.json
│       └── 0000_snapshot.json
└── drizzle.config.ts
```

---

## 📊 Query Patterns

### Dashboard Stats
```typescript
// Logs today
const logsToday = await db
  .select({ count: count() })
  .from(logs)
  .where(and(
    eq(logs.userId, userId),
    eq(logs.date, today)
  ));

// Open idea loops (draft or reality_checked)
const openLoops = await db
  .select({ count: count() })
  .from(ideas)
  .where(and(
    eq(ideas.userId, userId),
    inArray(ideas.status, ["draft", "reality_checked"])
  ));
```

### Weekly Review
```typescript
// Goals with completion rates
const goalsWithStats = await db
  .select({
    goal: goals,
    totalCheckins: count(checkins.id),
    completedCheckins: count(sql`CASE WHEN ${checkins.done} THEN 1 END`)
  })
  .from(goals)
  .leftJoin(checkins, eq(checkins.goalId, goals.id))
  .where(eq(goals.userId, userId))
  .groupBy(goals.id);
```

---

## 🗄️ Backup & Export

### Database Dump
```bash
# Full backup
pg_dump -h localhost -U postgres harriswildlands > backup.sql

# Schema only
pg_dump -h localhost -U postgres --schema-only harriswildlands > schema.sql

# Data only (specific user)
pg_dump -h localhost -U postgres --data-only --where="user_id='user-123'" harriswildlands > user_data.sql
```

### Application Export
```http
GET /api/export/data
```
Returns JSON with all user's data across all tables.

---

## 📈 Performance Optimization

### Indexes
All queries use indexes on:
- `userId` (every table)
- `userId + date` (logs, checkins)
- `userId + status` (ideas, goals)
- `goalId` (checkins for joins)

### Query Optimization
- User scoping happens at database level
- No full table scans
- Joins use indexed foreign keys

---

**Schema Version**: 1.0  
**Last Updated**: 2026-02-01  
**Status**: Production Ready
