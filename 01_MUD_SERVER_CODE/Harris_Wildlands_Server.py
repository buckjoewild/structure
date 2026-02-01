import socket
import threading
import argparse
import time
import random
from world import Room, NPC, Item, setup_world, save_world, load_world, respawn_npcs
from player import Player

# --- Mock Bruce™ API ---
class BruceAPI:
    @staticmethod
    def get_action(state):
        # Mock API response based on game state
        if any(npc.hp > 0 and 'attack' in npc.actions for npc in state['room'].npcs):
            target = next((npc for npc in state['room'].npcs if npc.hp > 0 and 'attack' in npc.actions), None)
            return {'action': 'kill', 'target': target.name}
        elif state['player'].following and state['player'].room != state['leader'].room:
            for direction, room in state['room'].exits.items():
                if room == state['leader'].room:
                    return {'action': 'move', 'direction': direction}
        elif random.random() < 0.3:
            return {'action': 'say', 'message': 'Cowabunga! Ready for some action?'}
        return {'action': 'idle'}

# --- Bruce™ AI Class ---
class BruceAI(Player):
    def __init__(self, name="Bruce™"):
        super().__init__(name, hp=150, max_hp=150, mana=120, max_mana=120, mv=120, max_mv=120)
        self.skills.update({'bash': 80, 'trip': 80, 'dirt': 80, 'rescue': 80})
        self.spells.update({'iceshard': 80, 'armor': 80})
        self.group = []
        self.following = None
        self.api = BruceAPI()

    def decide_action(self, leader, world_rooms):
        state = {'player': self, 'leader': leader, 'room': self.room, 'world_rooms': world_rooms}
        action = self.api.get_action(state)
        if action['action'] == 'kill':
            target = next((n for n in self.room.npcs if n.name.lower() == action['target'].lower()), None)
            if target:
                self.kill(target)
        elif action['action'] == 'move':
            self.move(action['direction'])
        elif action['action'] == 'say':
            self.say(action['message'])
        elif action['action'] == 'idle':
            pass
        if leader in self.group and random.random() < 0.2:
            self.rescue(leader.name)

def process_command(player, bruce, command, world_rooms):
    parts = command.split()
    if not parts:
        return " "
    cmd = parts[0].lower()
    args = " ".join(parts[1:]) if len(parts) > 1 else ""
    if cmd in player.aliases:
        cmd, args = player.aliases[cmd].split()[0], " ".join(player.aliases[cmd].split()[1:]) if len(player.aliases[cmd].split()) > 1 else ""

    if cmd == "move":
        player.move(args if args else "north")
        output = f"{player.room.description}\n[Exits: {' '.join(player.room.exits.keys())}]\n"
        for item in player.room.items:
            output += f"     {item.description}\n"
        for npc in player.room.npcs:
            output += f"{npc.description} {npc.name.lower().replace('a ', 'a ').replace('an ', 'an ')}.\n"
        return output
    elif cmd == "say":
        player.say(args)
        return f"You say, '{args}' (in {player.room.name})\n"
    elif cmd == "speak":
        player.speak(args)
        return ""
    elif cmd == "tell":
        target_name = args.split()[0] if args else ""
        message = " ".join(args.split()[1:]) if len(args.split()) > 1 else ""
        target = next((p for r in world_rooms for p in r.players if target_name.lower() in p.name.lower()), None)
        if target:
            player.tell(target, message)
            return f"You tell {target.name}, '{message}'\n"
        return "They're not here.\n"
    elif cmd == "kill":
        target = next((n for n in player.room.npcs if args.lower() in n.name.lower()), None)
        if target:
            player.kill(target)
            return ""
        return "No such target.\n"
    elif cmd == "flee":
        player.flee()
        return ""
    elif cmd == "sleep":
        player.sleep(args)
        return ""
    elif cmd == "areas":
        player.areas()
        return ""
    elif cmd == "exits":
        player.exits()
        return ""
    elif cmd == "examine":
        player.examine(args)
        return ""
    elif cmd == "corpsewhere":
        player.corpsewhere()
        return ""
    elif cmd == "finditems":
        player.finditems()
        return ""
    elif cmd == "findherbs":
        player.findherbs()
        return ""
    elif cmd == "findwater":
        player.findwater()
        return ""
    elif cmd == "huntersense":
        player.huntersense()
        return ""
    elif cmd == "wildmove":
        player.wildmove()
        return ""
    elif cmd == "plant":
        player.plant(args)
        return ""
    elif cmd == "roadblock":
        player.roadblock()
        return ""
    elif cmd == "setambush":
        player.setambush()
        return ""
    elif cmd == "setsnare":
        player.setsnare()
        return ""
    elif cmd == "save":
        player.save()
        save_world(world_rooms)
        return ""
    elif cmd == "load":
        player.load(world_rooms)
        return ""
    return "Unknown command.\n"

def mud_server(players, world_rooms):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 9999))
    server.listen(5)
    print("Harris Wildlands MUD listening on localhost:9999 - connect with telnet!")
    bruce = next((n for r in world_rooms for n in r.npcs if n.name == "Bruce™"), None)

    def handle_client(conn, addr):
        conn.send(b"Welcome to Harris Wildlands! Enter your character name:\n")
        char_name = conn.recv(1024).decode().strip()
        player = Player(char_name)
        players.append(player)
        starting_room, _ = setup_world()
        player.room = starting_room
        starting_room.players.append(player)
        load_world(world_rooms)
        conn.send(f"You open your eyes and cast your gaze upon the land.\n{player.room.name}\n  {player.room.description}\n\n[Exits: {' '.join(player.room.exits.keys())}]\n".encode())
        for item in player.room.items:
            conn.send(f"     {item.description}\n".encode())
        for npc in player.room.npcs:
            conn.send(f"{npc.description} {npc.name.lower().replace('a ', 'a ').replace('an ', 'an ')}.\n".encode())
        conn.send(f"<{player.hp}hp {player.mana}m {player.mv}mv> ".encode())
        conn.send(b"You have no unread notes.\n")

        while True:
            try:
                data = conn.recv(1024).decode().strip()
                if not data:
                    break
                respawn_npcs(world_rooms)  # Check for NPC respawns
                output = process_command(player, bruce, data, world_rooms)
                conn.send(f"{output}<{player.hp}hp {player.mana}m {player.mv}mv> ".encode())
            except Exception as e:
                print(f"Client {addr} disconnected: {e}")
                break
        player.room.players.remove(player)
        players.remove(player)
        conn.close()

    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr)).start()

def game_loop(player, bruce, starting_room, world_rooms):
    player.room = starting_room
    starting_room.players.append(player)
    load_world(world_rooms)
    print(f"Welcome to Harris Wildlands! You start in {player.room.name}.")
    print(player.room.description)
    print(f"[Exits: {' '.join(player.room.exits.keys())}]")
    while True:
        print(f"<{player.hp}hp {player.mana}m {player.mv}mv> ", end="")
        command = input().strip().lower()
        if command == "quit":
            save_world(world_rooms)
            print("Thanks for playing, cowabunga!")
            break
        respawn_npcs(world_rooms)
        output = process_command(player, bruce, command, world_rooms)
        print(output)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--server', action='store_true', help="Run as telnet MUD server on port 9999")
    args = parser.parse_args()

    players = []
    starting_room, world_rooms = setup_world()
    bruce = next((n for r in world_rooms for n in r.npcs if n.name == "Bruce™"), None)
    if args.server:
        mud_server(players, world_rooms)
    else:
        game_loop(Player("Wildlander"), bruce, starting_room, world_rooms)
