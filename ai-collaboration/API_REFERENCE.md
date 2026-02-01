# API REFERENCE

Complete API endpoint documentation for HarrisWildlands.com / BruceOps.

**Base URL**: `http://localhost:5000` (development)  
**Authentication**: Bearer token in `Authorization: Bearer <token>` header  
**Content-Type**: `application/json`

---

## 🔐 Authentication Endpoints

### Health Check
```http
GET /api/health
```
**Response**:
```json
{
  "status": "ok",
  "version": "1.0.0",
  "database": "connected",
  "ai_provider": "gemini",
  "ai_status": "ready"
}
```

### Current User
```http
GET /api/me
```
**Auth Required**: Yes  
**Response**:
```json
{
  "id": 1,
  "claims": {
    "sub": "user-id",
    "username": "bruce"
  }
}
```

---

## 📊 Dashboard Endpoints

### Get Dashboard Stats
```http
GET /api/dashboard
```
**Auth Required**: Yes  
**Response**:
```json
{
  "logsToday": 1,
  "openLoops": 3,
  "driftFlags": ["missed-checkins", "low-energy-trend"],
  "stats": {
    "weeklyCompletionRate": 78,
    "activeGoals": 8,
    "ideasInPipeline": 5
  }
}
```

---

## 📝 LifeOps Endpoints (Daily Logging)

### Get All Logs
```http
GET /api/logs
```
**Auth Required**: Yes  
**Response**: Array of log entries  
**Example**:
```json
[
  {
    "id": 123,
    "date": "2025-02-01",
    "userId": "user-123",
    "energy": 7,
    "stress": 4,
    "mood": 8,
    "vaping": false,
    "alcohol": false,
    "junkFood": false,
    "exercise": true,
    "topWin": "Completed project proposal",
    "topFriction": "Too many meetings",
    "tomorrowPriority": "Focus on deep work"
  }
]
```

### Get Log by Date
```http
GET /api/logs/:date
```
**Auth Required**: Yes  
**Params**: `date` (YYYY-MM-DD)  
**Response**: Single log entry or 404

### Create Log
```http
POST /api/logs
```
**Auth Required**: Yes  
**Body**:
```json
{
  "date": "2025-02-01",
  "energy": 7,
  "stress": 4,
  "mood": 8,
  "focus": 6,
  "sleepQuality": 8,
  "sleepHours": 7,
  "moneyPressure": 3,
  "connection": 8,
  "exercise": true,
  "vaping": false,
  "alcohol": false,
  "junkFood": false,
  "doomScrolling": false,
  "lateScreens": false,
  "skippedMeals": false,
  "excessCaffeine": false,
  "dayType": "work",
  "primaryEmotion": "grateful",
  "winCategory": "work",
  "timeDrain": "meetings",
  "topWin": "Completed proposal",
  "topFriction": "Too many meetings",
  "tomorrowPriority": "Focus on coding",
  "familyConnection": "Dinner with kids",
  "faithAlignment": "Morning prayer",
  "driftCheck": "Need more exercise"
}
```

### Update Log
```http
PUT /api/logs/:id
```
**Auth Required**: Yes  
**Body**: Same as Create (partial updates allowed)

---

## 💡 ThinkOps Endpoints (Ideas Pipeline)

### Get All Ideas
```http
GET /api/ideas
```
**Auth Required**: Yes  
**Query Params**:
- `status` (optional): draft, reality_checked, parked, promoted, shipped, discarded

**Response**:
```json
[
  {
    "id": 456,
    "title": "New mobile app concept",
    "pitch": "A personal operating system for dads...",
    "category": "tech",
    "status": "reality_checked",
    "excitement": 9,
    "feasibility": 7,
    "priority": 1,
    "realityCheck": "Market analysis shows...",
    "verdict": "promising",
    "createdAt": "2025-01-15",
    "updatedAt": "2025-01-20"
  }
]
```

### Get Single Idea
```http
GET /api/ideas/:id
```
**Auth Required**: Yes

### Create Idea
```http
POST /api/ideas
```
**Auth Required**: Yes  
**Body**:
```json
{
  "title": "App concept",
  "pitch": "Description here",
  "category": "tech",
  "excitement": 8,
  "feasibility": 6
}
```

### Update Idea
```http
PUT /api/ideas/:id
```
**Auth Required**: Yes

### Delete Idea
```http
DELETE /api/ideas/:id
```
**Auth Required**: Yes

### Reality Check (AI Analysis)
```http
POST /api/ideas/:id/reality-check
```
**Auth Required**: Yes  
**AI Quota**: 1 call (cached for 24 hours)  
**Response**:
```json
{
  "realityCheck": "Detailed AI analysis...",
  "verdict": "promising",
  "riskLevel": "medium",
  "recommendation": "Proceed with MVP"
}
```

### Promote Idea
```http
POST /api/ideas/:id/promote
```
**Auth Required**: Yes  
**Action**: Moves idea to next status in pipeline

### Park Idea
```http
POST /api/ideas/:id/park
```
**Auth Required**: Yes

### Discard Idea
```http
POST /api/ideas/:id/discard
```
**Auth Required**: Yes

---

## 🎯 Goals Endpoints

### Get All Goals
```http
GET /api/goals
```
**Auth Required**: Yes  
**Query Params**:
- `domain` (optional): faith, family, work, health, logistics, property, ideas, discipline
- `status` (optional): active, completed, paused

**Response**:
```json
[
  {
    "id": 789,
    "title": "Morning prayer routine",
    "domain": "faith",
    "priority": 1,
    "weeklyMinimum": "5x per week",
    "status": "active",
    "startDate": "2025-01-01",
    "endDate": "2025-12-31",
    "checkins": [
      { "date": "2025-02-01", "done": true, "note": "15 min prayer + scripture" }
    ]
  }
]
```

### Create Goal
```http
POST /api/goals
```
**Auth Required**: Yes  
**Body**:
```json
{
  "title": "Exercise 3x per week",
  "domain": "health",
  "priority": 1,
  "weeklyMinimum": "3x per week",
  "startDate": "2025-02-01",
  "endDate": "2025-12-31"
}
```

### Update Goal
```http
PUT /api/goals/:id
```
**Auth Required**: Yes

### Delete Goal
```http
DELETE /api/goals/:id
```
**Auth Required**: Yes

---

## ✅ Checkins Endpoints (Goal Progress)

### Get Recent Checkins
```http
GET /api/checkins
```
**Auth Required**: Yes  
**Query Params**:
- `goalId` (optional): Filter by specific goal
- `days` (optional): Number of days back (default: 7)

**Response**:
```json
[
  {
    "id": 1001,
    "goalId": 789,
    "date": "2025-02-01",
    "done": true,
    "note": "30 min run, felt great",
    "userId": "user-123"
  }
]
```

### Create Checkin
```http
POST /api/checkins
```
**Auth Required**: Yes  
**Body**:
```json
{
  "goalId": 789,
  "date": "2025-02-01",
  "done": true,
  "note": "Completed morning run"
}
```

### Update Checkin
```http
PUT /api/checkins/:id
```
**Auth Required**: Yes

### Delete Checkin
```http
DELETE /api/checkins/:id
```
**Auth Required**: Yes

---

## 📅 Weekly Review Endpoints

### Get Weekly Review
```http
GET /api/review/weekly
```
**Auth Required**: Yes  
**Response**:
```json
{
  "period": "2025-01-26 to 2025-02-01",
  "stats": {
    "totalCheckins": 21,
    "completedCheckins": 18,
    "completionRate": 85.7,
    "missedDays": 1
  },
  "goals": [
    {
      "id": 789,
      "title": "Morning prayer",
      "progress": "5/7 (71%)"
    }
  ],
  "driftFlags": ["missed-exercise", "late-bedtime"],
  "insights": "Strong week overall..."
}
```

---

## 🤖 AI Command Center Endpoints

### AI Search (Smart Log Search)
```http
POST /api/ai/search
```
**Auth Required**: Yes  
**AI Quota**: 1 call  
**Body**:
```json
{
  "query": "high energy days with exercise",
  "limit": 10
}
```
**Response**:
```json
{
  "query": "high energy days with exercise",
  "count": 15,
  "insight": "You have 15 days with energy >7 and exercise=true...",
  "samples": [...],
  "cached": true,
  "quotaRemaining": 99
}
```

### AI Squad (Multi-Perspective Analysis)
```http
POST /api/ai/squad
```
**Auth Required**: Yes  
**AI Quota**: 1 call  
**Body**:
```json
{
  "topic": "Should I pursue this idea?",
  "context": "Idea details here..."
}
```

### Weekly Synthesis (Narrative Summary)
```http
POST /api/ai/weekly-synthesis
```
**Auth Required**: Yes  
**AI Quota**: 1 call  
**Response**:
```json
{
  "narrative": "This week was marked by...",
  "patterns": ["High stress on meeting days"],
  "recommendations": ["Block time for deep work"]
}
```

### Correlations (Pattern Detection)
```http
POST /api/ai/correlations
```
**Auth Required**: Yes  
**AI Quota**: 1 call

---

## 📚 Teaching Assistant Endpoints

### Generate Lesson Plan
```http
POST /api/teaching
```
**Auth Required**: Yes  
**AI Quota**: 1 call  
**Body**:
```json
{
  "grade": "5th",
  "topic": "Fractions",
  "standard": "CCSS.MATH.5.NF.A.1",
  "duration": 45
}
```
**Response**:
```json
{
  "title": "Adding Fractions with Unlike Denominators",
  "objectives": ["Find common denominators", "Add fractions"],
  "materials": ["Fraction strips", "Whiteboard"],
  "activities": [...],
  "assessment": "Exit ticket with 3 problems"
}
```

---

## ⚙️ Settings Endpoints

### Get Settings
```http
GET /api/settings
```
**Auth Required**: Yes

### Update Settings
```http
PUT /api/settings
```
**Auth Required**: Yes

---

## 📤 Export Endpoints

### Export All Data
```http
GET /api/export/data
```
**Auth Required**: Yes  
**Response**: JSON file download with all user data

---

## 🔒 API Tokens (For External Access)

### List API Tokens
```http
GET /api/settings/tokens
```
**Auth Required**: Yes

### Create API Token
```http
POST /api/settings/tokens
```
**Auth Required**: Yes  
**Body**:
```json
{
  "name": "OpenClaw Integration"
}
```
**Response**:
```json
{
  "token": "bruceops_abc123...",
  "name": "OpenClaw Integration",
  "createdAt": "2025-02-01"
}
```

⚠️ **Token is shown only once - save it immediately!**

### Revoke API Token
```http
DELETE /api/settings/tokens/:id
```
**Auth Required**: Yes

---

## 🚫 Error Responses

### 401 Unauthorized
```json
{
  "error": "Not authenticated"
}
```

### 403 Forbidden
```json
{
  "error": "Access denied"
}
```

### 404 Not Found
```json
{
  "error": "Resource not found"
}
```

### 429 Rate Limited
```json
{
  "error": "Rate limit exceeded",
  "retryAfter": 900
}
```

### 500 Server Error
```json
{
  "error": "Internal server error"
}
```

---

## 📊 Rate Limits

- **General API**: 100 requests per 15 minutes
- **AI Endpoints**: 10 calls per day (configurable)
- **Teaching**: 5 calls per hour

---

## 🎯 Quick Reference

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/api/health` | GET | No | System status |
| `/api/dashboard` | GET | Yes | Quick stats |
| `/api/logs` | GET/POST | Yes | Daily logs |
| `/api/ideas` | GET/POST | Yes | Ideas pipeline |
| `/api/ideas/:id/reality-check` | POST | Yes | AI analysis |
| `/api/goals` | GET/POST | Yes | Weekly goals |
| `/api/checkins` | GET/POST | Yes | Goal progress |
| `/api/review/weekly` | GET | Yes | Weekly summary |
| `/api/ai/search` | POST | Yes | Smart search |
| `/api/teaching` | POST | Yes | Lesson plans |
| `/api/export/data` | GET | Yes | Data export |

---

## 🔗 Integration Examples

### cURL Example
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:5000/api/dashboard
```

### JavaScript Example
```javascript
const response = await fetch('http://localhost:5000/api/logs', {
  headers: { 'Authorization': 'Bearer ' + token }
});
const logs = await response.json();
```

### Python Example
```python
import requests

headers = {'Authorization': 'Bearer YOUR_TOKEN'}
response = requests.get('http://localhost:5000/api/dashboard', headers=headers)
data = response.json()
```

---

**API Version**: 1.0  
**Last Updated**: 2026-02-01  
**Status**: Production Ready
