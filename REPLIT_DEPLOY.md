# Replit Deployment Guide

Deploy the complete Harris Wilderness MUD + BruceOps system on Replit.

## 🚀 Quick Deploy

### Step 1: Import to Replit
1. Go to [Replit](https://replit.com)
2. Click **"Create"** → **"Import from GitHub"**
3. Enter: `https://github.com/buckjoewild/harriswildlands.com`
4. Click **"Import from GitHub"**

### Step 2: Configure Secrets
In Replit's **Secrets** tool (left sidebar), add:

```
OPENAI_API_KEY = your-openai-key
BRUCEOPS_API_TOKEN = your-bruceops-token
DISCORD_BOT_TOKEN = your-discord-token
```

### Step 3: Run
Click the **"Run"** button (big green button at top)

Replit will automatically:
- Install all dependencies
- Start BruceOps on port 5000
- Start MUD Server on port 4008
- Start MUD Terminal on port 8080

## 🌐 Access URLs

After deployment, your app will be available at:

- **Main App**: `https://your-project-name.your-username.replit.app`
- **MUD Terminal**: `https://your-project-name.your-username.replit.app:3000`
- **WebSocket**: `wss://your-project-name.your-username.replit.app:8080`

## 🎮 Using the MUD

### Web Terminal
Open the MUD Terminal URL in your browser for the retro green-on-black interface.

### Discord
Use commands like:
```
@bruce mud-look
@bruce mud-go north
@bruce mud-autopilot on
```

## 🔧 Troubleshooting

### Port Already in Use
If you see "Port already in use", click **"Stop"** then **"Run"** again.

### Dependencies Not Installing
Open Shell and run:
```bash
cd harriswildlands && npm install
cd ../mud-server && pip install websockets
```

### WebSocket Connection Failed
Make sure all three services show green checkmarks in the Ports panel.

## 📊 Monitoring

Check the **Console** and **Shell** tabs to see:
- BruceOps server logs
- MUD server activity
- Agent decisions
- Player connections

## 🔄 Auto-Deploy

Replit automatically deploys on every push to GitHub main branch.

## 📝 Notes

- **Free Tier**: All three services fit within Replit's free tier limits
- **Sleeping**: Free repls sleep after inactivity - just click Run to wake
- **Database**: Uses Replit's built-in PostgreSQL (automatically configured)

## 🆘 Support

If deployment fails:
1. Check Secrets are configured
2. Verify all files are present in structure/
3. Check Replit's **System Logs** for errors
4. Run `start-replit.sh` manually in Shell

Happy exploring! 🎮
