---
name: mud-terminal
description: Control the Harris Wilderness MUD from Discord - explore, create, and interact with OpenClaw
metadata:
  {
    "openclaw":
      {
        "emoji": "🎮",
        "requires": { "env": ["MUD_SERVER_URL"] },
        "homepage": "https://harriswildlands.com/mud"
      }
  }
---

# MUD Terminal Skill

Connect to the Harris Wilderness MUD text adventure world directly from Discord.

## Available Commands

### mud-connect
Connect to the MUD server
Usage: @bruce mud-connect

### mud-look  
Look around your current location
Usage: @bruce mud-look

### mud-go
Move in a direction (north, south, east, west, up, down)
Usage: @bruce mud-go [direction]
Aliases: @bruce mud-n, @bruce mud-s, @bruce mud-e, @bruce mud-w

### mud-say
Speak in the MUD world
Usage: @bruce mud-say "Hello everyone!"

### mud-create
Create a new room (builder command)
Usage: @bruce mud-create [direction] [room name]
Example: @bruce mud-create north "Crystal Cavern"

### mud-spawn
Spawn an NPC in your location
Usage: @bruce mud-spawn [NPC name]
Example: @bruce mud-spawn "Mysterious Merchant"

### mud-inventory
Check your inventory
Usage: @bruce mud-inventory

### mud-status
Show MUD world status
Usage: @bruce mud-status

### mud-autopilot
Toggle OpenClaw autonomous agent
Usage: @bruce mud-autopilot [on|off]
When ON: OpenClaw explores, creates, and socializes automatically

### mud-who
List players online
Usage: @bruce mud-who

## Agent Autonomy

When autopilot is enabled, OpenClaw will:
- 🗺️ Explore new areas automatically
- 🏗️ Create rooms and expand the world
- 👤 Spawn NPCs and interact with them
- 💬 Socialize with other players
- 🔮 Generate content using AI

The agent makes decisions every 5-15 seconds based on:
- Curiosity (35% - explore new areas)
- Creativity (25% - create content)
- Social drive (20% - interact)
- Environment (15% - examine/interact)
- Rest (5% - recover energy)

## World Stats

The MUD tracks:
- Rooms explored
- NPCs encountered
- Items collected
- Conversations had
- World expansion by OpenClaw

All activity syncs back to BruceOps LifeOps logs!
