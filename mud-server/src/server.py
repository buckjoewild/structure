#!/usr/bin/env python3
"""
Harris Wilderness MUD Server
A retro text-based multiplayer world with OpenClaw autonomous integration
"""

import asyncio
import json
import logging
import random
import sys
import time
from datetime import datetime
from typing import Dict, List, Optional, Set
import websockets
import sqlite3
from pathlib import Path

# Configure logging with retro style
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)

class Room:
    """A room in the MUD world"""
    def __init__(self, id: str, name: str, description: str):
        self.id = id
        self.name = name
        self.description = description
        self.exits = {}  # direction -> room_id
        self.objects = []
        self.npcs = []
        self.players = set()
        self.created_at = datetime.now()
        self.created_by = "system"
        
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "exits": self.exits,
            "objects": self.objects,
            "npcs": [npc.to_dict() for npc in self.npcs],
            "players": list(self.players),
            "created_by": self.created_by
        }

class NPC:
    """Non-player character"""
    def __init__(self, id: str, name: str, description: str, npc_type: str = "wanderer"):
        self.id = id
        self.name = name
        self.description = description
        self.type = npc_type
        self.room_id = None
        self.dialogue = []
        self.inventory = []
        self.ai_mood = random.choice(["friendly", "neutral", "mysterious", "helpful"])
        
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "type": self.type,
            "mood": self.ai_mood,
            "room": self.room_id
        }

class Player:
    """Player or Agent in the MUD"""
    def __init__(self, name: str, is_agent: bool = False):
        self.name = name
        self.room_id = "spawn"
        self.inventory = []
        self.is_agent = is_agent
        self.websocket = None
        self.connected_at = datetime.now()
        self.explored_rooms = set()
        self.stats = {
            "health": 100,
            "energy": 100,
            "mood": "curious"
        }
        
    def to_dict(self):
        return {
            "name": self.name,
            "room": self.room_id,
            "is_agent": self.is_agent,
            "inventory": self.inventory,
            "stats": self.stats,
            "explored": len(self.explored_rooms)
        }

class MUDWorld:
    """The game world"""
    def __init__(self):
        self.rooms: Dict[str, Room] = {}
        self.players: Dict[str, Player] = {}
        self.npcs: Dict[str, NPC] = {}
        self.connections: Set = set()
        self.command_handlers = {
            "look": self.cmd_look,
            "go": self.cmd_go,
            "north": lambda p, args: self.cmd_go(p, ["north"]),
            "south": lambda p, args: self.cmd_go(p, ["south"]),
            "east": lambda p, args: self.cmd_go(p, ["east"]),
            "west": lambda p, args: self.cmd_go(p, ["west"]),
            "up": lambda p, args: self.cmd_go(p, ["up"]),
            "down": lambda p, args: self.cmd_go(p, ["down"]),
            "n": lambda p, args: self.cmd_go(p, ["north"]),
            "s": lambda p, args: self.cmd_go(p, ["south"]),
            "e": lambda p, args: self.cmd_go(p, ["east"]),
            "w": lambda p, args: self.cmd_go(p, ["west"]),
            "say": self.cmd_say,
            "inventory": self.cmd_inventory,
            "help": self.cmd_help,
            "who": self.cmd_who,
            "create": self.cmd_create,
            "spawn": self.cmd_spawn,
            "examine": self.cmd_examine,
            "take": self.cmd_take,
            "drop": self.cmd_drop,
            "status": self.cmd_status,
        }
        self.init_world()
        
    def init_world(self):
        """Initialize the starting world"""
        # Spawn point
        spawn = Room("spawn", "The Clearing", 
            "A mossy clearing surrounded by ancient pines. Sunlight filters through the canopy, "
            "casting dancing shadows on the forest floor. A weathered stone altar stands in the center.")
        spawn.objects = ["stone altar", "glowing mushrooms", "weathered sign"]
        
        # Create initial rooms
        rooms_data = [
            ("forest_north", "Whispering Pines", 
             "Tall pine trees whisper secrets in the wind. The air smells of sap and wilderness."),
            ("forest_east", "Misty Ravine", 
             "A narrow ravine shrouded in perpetual mist. Strange sounds echo from the depths."),
            ("forest_south", "Crystal Stream", 
             "A clear stream babbles over smooth stones. The water sparkles with an otherworldly light."),
            ("forest_west", "Ancient Grove", 
             "Circle of ancient oaks older than memory. Their bark is etched with mysterious symbols."),
        ]
        
        for room_id, name, desc in rooms_data:
            self.rooms[room_id] = Room(room_id, name, desc)
        
        # Connect rooms
        spawn.exits = {"north": "forest_north", "east": "forest_east", 
                       "south": "forest_south", "west": "forest_west"}
        self.rooms["forest_north"].exits = {"south": "spawn"}
        self.rooms["forest_east"].exits = {"west": "spawn"}
        self.rooms["forest_south"].exits = {"north": "spawn"}
        self.rooms["forest_west"].exits = {"east": "spawn"}
        
        self.rooms["spawn"] = spawn
        
        # Create some NPCs
        npcs_data = [
            ("elder_willow", "Elder Willow", "An ancient mystic who tends the forest", "mystic", "spawn"),
            ("wanderer_jack", "Jack the Wanderer", "A curious traveler with many stories", "wanderer", "forest_north"),
        ]
        
        for npc_id, name, desc, npc_type, room_id in npcs_data:
            npc = NPC(npc_id, name, desc, npc_type)
            npc.room_id = room_id
            self.npcs[npc_id] = npc
            self.rooms[room_id].npcs.append(npc)
        
        logger.info("🌲 World initialized with %d rooms and %d NPCs", len(self.rooms), len(self.npcs))
    
    async def handle_command(self, player: Player, command_line: str) -> str:
        """Process a player command"""
        parts = command_line.strip().split()
        if not parts:
            return ""
            
        cmd = parts[0].lower()
        args = parts[1:]
        
        if cmd in self.command_handlers:
            try:
                return await self.command_handlers[cmd](player, args)
            except Exception as e:
                logger.error(f"Command error: {e}")
                return "Something went wrong. The forest spirits are confused."
        else:
            return f"Unknown command: '{cmd}'. Type 'help' for available commands."
    
    async def cmd_look(self, player: Player, args: List[str]) -> str:
        """Look around the room"""
        room = self.rooms.get(player.room_id)
        if not room:
            return "You are nowhere. This is concerning."
        
        # Mark as explored
        player.explored_rooms.add(room.id)
        
        result = f"\n[{room.name}]\n{room.description}\n\n"
        
        if room.objects:
            result += f"You see: {', '.join(room.objects)}\n"
        
        if room.npcs:
            npc_names = [npc.name for npc in room.npcs]
            result += f"NPCs: {', '.join(npc_names)}\n"
        
        other_players = [p.name for p in self.players.values() 
                        if p.room_id == room.id and p.name != player.name]
        if other_players:
            result += f"Players here: {', '.join(other_players)}\n"
        
        if room.exits:
            exits = [f"{dir} ({self.rooms.get(rid, Room('', 'Unknown', '')).name})" 
                    for dir, rid in room.exits.items()]
            result += f"\nExits: {', '.join(exits)}\n"
        
        return result
    
    async def cmd_go(self, player: Player, args: List[str]) -> str:
        """Move to another room"""
        if not args:
            return "Go where? (north, south, east, west, up, down)"
        
        direction = args[0].lower()
        room = self.rooms.get(player.room_id)
        
        if direction not in room.exits:
            return f"You can't go {direction} from here."
        
        new_room_id = room.exits[direction]
        
        # Remove from old room
        room.players.discard(player.name)
        
        # Move player
        player.room_id = new_room_id
        new_room = self.rooms[new_room_id]
        new_room.players.add(player.name)
        
        # Notify others
        await self.broadcast(f"{player.name} arrives from the {self.opposite_dir(direction)}.", 
                           new_room_id, exclude=player.name)
        
        return f"You go {direction}.\n{await self.cmd_look(player, [])}"
    
    async def cmd_say(self, player: Player, args: List[str]) -> str:
        """Say something to the room"""
        if not args:
            return "Say what?"
        
        message = ' '.join(args)
        room_id = player.room_id
        
        await self.broadcast(f"{player.name} says: \"{message}\"", room_id, exclude=player.name)
        
        return f"You say: \"{message}\""
    
    async def cmd_create(self, player: Player, args: List[str]) -> str:
        """Create new room (builder command)"""
        if len(args) < 2:
            return "Usage: create <direction> <room name>"
        
        direction = args[0].lower()
        room_name = ' '.join(args[1:])
        
        current_room = self.rooms[player.room_id]
        
        if direction in current_room.exits:
            return f"There's already something to the {direction}!"
        
        # Create new room
        room_id = f"room_{int(time.time())}_{random.randint(1000,9999)}"
        new_room = Room(room_id, room_name, 
            f"A newly formed space in the wilderness. It smells of possibility.")
        new_room.created_by = player.name
        
        # Connect rooms
        current_room.exits[direction] = room_id
        new_room.exits[self.opposite_dir(direction)] = player.room_id
        
        self.rooms[room_id] = new_room
        
        # Notify
        await self.broadcast(f"The world shifts! A new area opens to the {direction}!", 
                           player.room_id)
        
        logger.info(f"🏗️  {player.name} created room: {room_name} ({room_id})")
        
        return f"You create a new realm: {room_name}\nIt lies to the {direction}."
    
    async def cmd_spawn(self, player: Player, args: List[str]) -> str:
        """Spawn an NPC"""
        if not args:
            return "Usage: spawn <npc name>"
        
        npc_name = ' '.join(args)
        npc_id = f"npc_{int(time.time())}_{random.randint(1000,9999)}"
        
        npc = NPC(npc_id, npc_name, f"A mysterious figure named {npc_name}", "wanderer")
        npc.room_id = player.room_id
        
        self.npcs[npc_id] = npc
        self.rooms[player.room_id].npcs.append(npc)
        
        await self.broadcast(f"A shimmering form coalesces into {npc_name}!", 
                           player.room_id)
        
        logger.info(f"👤 {player.name} spawned NPC: {npc_name}")
        
        return f"You summon {npc_name} into existence."
    
    async def cmd_inventory(self, player: Player, args: List[str]) -> str:
        """Check inventory"""
        if not player.inventory:
            return "Your inventory is empty."
        return f"You carry: {', '.join(player.inventory)}"
    
    async def cmd_who(self, player: Player, args: List[str]) -> str:
        """List online players"""
        players = [p.name + (" (AI)" if p.is_agent else "") for p in self.players.values()]
        return f"Online ({len(players)}): {', '.join(players)}"
    
    async def cmd_help(self, player: Player, args: List[str]) -> str:
        """Show help"""
        return """
Available Commands:
------------------
look           - Look around
[n/s/e/w/u/d]  - Move in a direction
go <dir>       - Move direction
say <text>     - Speak to room
create <dir> <name> - Create new room (builder)
spawn <name>   - Spawn NPC
examine <obj>  - Look at object
inventory      - Check inventory
take <item>    - Take item
drop <item>    - Drop item
who            - List players
help           - Show this help
status         - Show world status

Directions: north (n), south (s), east (e), west (w), up (u), down (d)
        """
    
    async def cmd_status(self, player: Player, args: List[str]) -> str:
        """Show world status"""
        return f"""
World Status:
-------------
Rooms: {len(self.rooms)}
NPCs: {len(self.npcs)}
Players Online: {len(self.players)}
Your Location: {self.rooms[player.room_id].name}
Explored: {len(player.explored_rooms)} rooms
        """
    
    async def cmd_examine(self, player: Player, args: List[str]) -> str:
        """Examine something"""
        if not args:
            return "Examine what?"
        target = ' '.join(args).lower()
        room = self.rooms[player.room_id]
        
        for obj in room.objects:
            if target in obj.lower():
                return f"You examine the {obj}. It's interesting but reveals no secrets."
        
        for npc in room.npcs:
            if target in npc.name.lower():
                return f"{npc.name}: {npc.description}\nMood: {npc.ai_mood}"
        
        return f"You don't see '{target}' here."
    
    async def cmd_take(self, player: Player, args: List[str]) -> str:
        """Take an object"""
        if not args:
            return "Take what?"
        target = ' '.join(args).lower()
        room = self.rooms[player.room_id]
        
        for obj in room.objects[:]:
            if target in obj.lower():
                room.objects.remove(obj)
                player.inventory.append(obj)
                return f"You take the {obj}."
        
        return f"You can't take '{target}'."
    
    async def cmd_drop(self, player: Player, args: List[str]) -> str:
        """Drop an item"""
        if not args:
            return "Drop what?"
        target = ' '.join(args).lower()
        
        for item in player.inventory[:]:
            if target in item.lower():
                player.inventory.remove(item)
                self.rooms[player.room_id].objects.append(item)
                return f"You drop the {item}."
        
        return f"You don't have '{target}'."
    
    def opposite_dir(self, direction: str) -> str:
        """Get opposite direction"""
        opposites = {
            "north": "south", "south": "north",
            "east": "west", "west": "east",
            "up": "down", "down": "up",
            "n": "s", "s": "n", "e": "w", "w": "e",
            "u": "d", "d": "u"
        }
        return opposites.get(direction, "somewhere")
    
    async def broadcast(self, message: str, room_id: str, exclude: str = None):
        """Send message to all players in a room"""
        for player in self.players.values():
            if player.room_id == room_id and player.name != exclude:
                if player.websocket and not player.websocket.closed:
                    try:
                        await player.websocket.send(json.dumps({
                            "type": "broadcast",
                            "text": message,
                            "timestamp": datetime.now().isoformat()
                        }))
                    except:
                        pass

class MUDServer:
    """WebSocket server for MUD"""
    def __init__(self, world: MUDWorld, host: str = "localhost", port: int = 4008):
        self.world = world
        self.host = host
        self.port = port
        
    async def handle_client(self, websocket, path):
        """Handle a client connection"""
        try:
            # Get player name
            await websocket.send(json.dumps({
                "type": "system",
                "text": "=== HARRIS WILDERNESS MUD ===\nEnter your name:"
            }))
            
            name_msg = await websocket.recv()
            name_data = json.loads(name_msg)
            name = name_data.get("command", "Wanderer").strip()
            
            # Check if agent
            is_agent = name.lower() in ["openclaw", "agent", "ai"]
            
            # Create player
            player = Player(name, is_agent)
            player.websocket = websocket
            self.world.players[name] = player
            self.world.connections.add(websocket)
            
            # Welcome
            welcome_msg = f"""
Welcome, {name}! {'[AUTONOMOUS AGENT]' if is_agent else ''}
Type 'help' for commands.
            """
            await websocket.send(json.dumps({
                "type": "system",
                "text": welcome_msg
            }))
            
            # Show initial room
            look_result = await self.world.cmd_look(player, [])
            await websocket.send(json.dumps({
                "type": "room",
                "text": look_result
            }))
            
            # Notify others
            await self.world.broadcast(f"{name} materializes from the void!", "spawn", name)
            
            logger.info(f"👤 Player connected: {name} {'(AI)' if is_agent else ''}")
            
            # Main loop
            async for message in websocket:
                try:
                    data = json.loads(message)
                    command = data.get("command", "").strip()
                    
                    if command:
                        result = await self.world.handle_command(player, command)
                        if result:
                            await websocket.send(json.dumps({
                                "type": "response",
                                "text": result,
                                "timestamp": datetime.now().isoformat()
                            }))
                            
                except json.JSONDecodeError:
                    await websocket.send(json.dumps({
                        "type": "error",
                        "text": "Invalid message format"
                    }))
                    
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            # Cleanup
            if name in self.world.players:
                player = self.world.players[name]
                room = self.world.rooms.get(player.room_id)
                if room:
                    room.players.discard(name)
                del self.world.players[name]
                self.world.connections.discard(websocket)
                await self.world.broadcast(f"{name} fades into the mist...", player.room_id)
                logger.info(f"👋 Player disconnected: {name}")
    
    async def start(self):
        """Start the server"""
        logger.info(f"🚀 MUD Server starting on ws://{self.host}:{self.port}")
        async with websockets.serve(self.handle_client, self.host, self.port):
            logger.info("✅ Server running! Connect with: websocat ws://localhost:4008")
            await asyncio.Future()  # Run forever

def main():
    """Main entry point"""
    print("""
╔══════════════════════════════════════════╗
║      HARRIS WILDERNESS MUD SERVER        ║
║         Retro Text Adventure              ║
╚══════════════════════════════════════════╝
    """)
    
    world = MUDWorld()
    server = MUDServer(world)
    
    try:
        asyncio.run(server.start())
    except KeyboardInterrupt:
        logger.info("\n🛑 Server shutting down...")
        sys.exit(0)

if __name__ == "__main__":
    main()
