# OpenCLaw Integration Guide for BruceOps

## Overview
OpenCLaw is a powerful command-line tool that provides Claude AI capabilities directly from your terminal. We'll integrate it with your BruceOps API to enable AI-powered interactions with your personal operating system.

## Prerequisites

1. **OpenCLaw CLI** - Install from [claude.ai](https://claude.ai/download)
2. **API Token** - Generate from BruceOps (once OpenAI is configured)
3. **Node.js** - Should already be installed with BruceOps

---

## Step 1: Install OpenCLaw

### Method 1: Official Installation (Recommended)
```bash
# Using curl (macOS/Linux)
curl -fSL https://claude.ai/claude.sh | sh

# Using PowerShell (Windows)
iwr -useb https://claude.ai/claude.ps1 | Out-File -FilePath claude.ps1 | powershell -ExecutionPolicy Bypass -Scope Process -File claude.ps1
```

### Method 2: Package Manager
```bash
# npm
npm install -g @anthropic-ai/claude-cli

# yarn  
yarn global add @anthropic-ai/claude-cli

# Verify installation
claude --version
```

---

## Step 2: Generate API Token from BruceOps

Since OpenAI is now your primary AI provider, you'll need an API token:

### Option A: Using BruceOps UI
1. Start BruceOps: `npm run dev`
2. Open browser: `http://localhost:3000`
3. Navigate to `/api-docs`
4. Look for token management or API key settings

### Option B: Direct API Call
```bash
# Create new API token for Claude Desktop
curl -X POST http://localhost:3000/api/settings/tokens \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_SESSION_TOKEN" \
  -d '{"name": "Claude Desktop OpenAI", "description": "For Claude CLI integration"}'

# Response will include token
```

---

## Step 3: Configure OpenCLaw

Create/OpenCLaw configuration file:

```bash
# Create config directory and file
mkdir -p ~/.config/claude
cat > ~/.config/claude/claude_desktop_config.json << 'EOF'
{
  "api_key": "YOUR_OPENAI_API_KEY",
  "api_url": "http://localhost:3000",
  "max_retries": 3,
  "timeout": 30,
  "user_agent": "bruceops-claude-cli/1.0"
}
EOF

# Set appropriate permissions
chmod 600 ~/.config/claude/claude_desktop_config.json
```

### Update with your actual API key:
```bash
# Replace YOUR_OPENAI_API_KEY with your actual key
sed -i.bak 's/YOUR_OPENAI_API_KEY/' \
  ~/.config/claude/claude_desktop_config.json

# Or set environment variable
export ANTHROPIC_API_KEY="sk-your-actual-key-here"
```

---

## Step 4: Test the Integration

### Test Basic Connection
```bash
# Test OpenCLaw connection
claude --help

# Should show available commands and confirm connection
```

### Test BruceOps API Integration
```bash
# Test that Claude can access your BruceOps API
claude "Can you access my BruceOps API at localhost:3000 and list my recent logs? Show me the last 3 entries with just the date and energy levels."

# Claude should make API calls to your BruceOps system
```

---

## Step 5: Create Custom OpenCLaw Scripts (Optional)

Create convenience scripts for common BruceOps tasks:

### BruceOps Quick Commands
```bash
# Create scripts directory
mkdir -p ~/scripts/claude

# Daily log script
cat > ~/scripts/claude/daily_log.sh << 'EOF'
#!/bin/bash
claude "Create a new BruceOps daily log entry for today with:
- Energy level (1-10)
- Stress level (1-10) 
- Main accomplishment
- Top priority for tomorrow
Use the actual date today."
EOF

# Make executable
chmod +x ~/scripts/claude/daily_log.sh

# Ideas management script
cat > ~/scripts/claude/ideas.sh << 'EOF'
#!/bin/bash
claude "Show me my current ThinkOps ideas pipeline. List each idea with status, priority (1-5), and suggest the next action I should take."
EOF

chmod +x ~/scripts/claude/ideas.sh

# Weekly review script
cat > ~/scripts/claude/weekly_review.sh << 'EOF'
#!/bin/bash
claude "Generate a comprehensive weekly review of my BruceOps data including:
- Goal completion rates
- AI-generated insights
- Pattern analysis
- Action items for next week
Access all relevant APIs and synthesize into actionable insights."
EOF

chmod +x ~/scripts/claude/weekly_review.sh
```

### Custom OpenCLaw Tools
```bash
# Create custom MCP-style tools for BruceOps
cat > ~/.config/claude/bruceops_tools.json << 'EOF'
{
  "name": "BruceOps Tools",
  "version": "1.0.0",
  "tools": [
    {
      "name": "get_daily_metrics",
      "description": "Get comprehensive daily metrics and patterns from BruceOps",
      "parameters": {
        "days": {
          "type": "integer",
          "description": "Number of days to analyze",
          "default": 7
        },
        "include_ai_insights": {
          "type": "boolean", 
          "description": "Include AI-generated insights",
          "default": true
        }
      }
    },
    {
      "name": "analyze_patterns",
      "description": "Analyze patterns across life metrics, goals, and productivity",
      "parameters": {
        "timeframe": {
          "type": "string",
          "enum": ["week", "month", "quarter"],
          "default": "month"
        },
        "focus_areas": {
          "type": "array",
          "items": {"type": "string", "enum": ["energy", "stress", "goals", "ideas", "teaching"]},
          "description": "Areas to focus analysis on"
        }
      }
    }
  ]
}
EOF
```

---

## Step 6: Aliases for Convenience

```bash
# Add to shell profile (~/.bashrc or ~/.zshrc)
alias bruceops='claude'
alias daily-log='~/scripts/claude/daily_log.sh'
alias weekly-review='~/scripts/claude/weekly_review.sh'
alias ideas='~/scripts/claude/ideas.sh'

# Reload shell configuration
source ~/.bashrc  # or ~/.zshrc
```

---

## Step 7: Troubleshooting

### Common Issues and Solutions

#### Connection Issues
```bash
# Check API availability
curl -f http://localhost:3000/api/health

# Check OpenCLaw configuration
claude --config

# Test with verbose output
claude --verbose "Test message"
```

#### API Token Issues
```bash
# Check if token is valid
curl -H "Authorization: Bearer YOUR_TOKEN" \
     http://localhost:3000/api/me

# Generate new token if needed
curl -X POST http://localhost:3000/api/settings/tokens \
     -H "Content-Type: application/json" \
     -d '{"name": "Claude CLI", "description": "Replacement token"}'
```

#### Port Conflicts
```bash
# Check if BruceOps is running on expected port
netstat -tulpn | grep :3000

# Start BruceOps if not running
npm run dev

# Or specify different port
export PORT=3001
npm run dev
```

---

## Step 8: Security Best Practices

### Protect Your API Keys
```bash
# Use environment variables instead of hardcoded keys
export ANTHROPIC_API_KEY="sk-your-key"

# Set file permissions
chmod 600 ~/.config/claude/claude_desktop_config.json

# Don't commit keys to version control
echo "*.key" >> .gitignore
echo "claude_desktop_config.json" >> .gitignore
```

### Network Security
```bash
# Only use HTTPS in production
# Validate SSL certificates
# Use firewall rules to restrict API access
```

---

## Step 9: Advanced Integration

### Automate Workflows
```bash
# Create automated workflows
cat > ~/scripts/bruceops_morning_routine.sh << 'EOF'
#!/bin/bash
echo "🌅 Good morning, Bruce! Running BruceOps morning routine..."

# 1. Check yesterday's metrics
claude "What were my main metrics from yesterday? Focus on energy, stress, and goal completion."

# 2. Get today's priorities  
claude "Based on my calendar and goals, what are my top 3 priorities for today?"

# 3. Generate daily log template
claude "Create a structured daily log entry template for today with all standard fields."

# 4. Check idea pipeline
claude "Review my ThinkOps ideas pipeline. Which ideas need attention this week?"

echo "✅ BruceOps morning routine complete!"
EOF

chmod +x ~/scripts/bruceops_morning_routine.sh
```

### Integration with Other Tools
```bash
# Example: Combine with task management
claude "Help me integrate my BruceOps goals with my task manager. Create a script that:
1. Syncs goals from BruceOps to my task manager
2. Updates completion status back to BruceOps
3. Provides weekly progress reports
4. Sends notifications for upcoming deadlines"
```

---

## Verification Checklist

Before using OpenCLaw with BruceOps, verify:

- [ ] OpenCLaw CLI installed and working
- [ ] BruceOps API accessible via HTTP
- [ ] API token generated and configured
- [ ] Test Claude command successful
- [ ] Custom scripts created and functional
- [ ] Aliases working in shell
- [ ] Security best practices implemented

---

## Support Commands

```bash
# Quick reference for common tasks
alias bruceops-help='echo "BruceOps + Claude Commands:
daily-log - Create daily log entry
weekly-review - Generate weekly review
ideas - Manage ideas pipeline
metrics - Analyze patterns and trends
sync - Sync with external tools
help - Show this help"'

# Quick status check
alias bruceops-status='claude "Quick status check: Is BruceOps API accessible? Are there any drift flags or urgent items?"'
```

This integration will give you powerful AI assistance directly from your command line, with full access to your BruceOps personal operating system!