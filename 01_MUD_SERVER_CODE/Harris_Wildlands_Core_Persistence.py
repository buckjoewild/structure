# core/persistence.py

import json, os
from .npc import NPC
from .item import Item

def save_world(rooms, filename="world_save.json"):
    data = []
    for room in rooms:
        data.append({
            'name': room.name,
            'npcs': [
                {'name': n.name, 'hp': n.hp, 'respawn_timer': n.respawn_timer,
                 'controller': n.controller.name if n.controller else None, 'effects': n.effects}
                for n in room.npcs
            ],
            'items': [
                {'name': i.name, 'description': i.description, 'equip_slot': i.equip_slot,
                 'price': i.price, 'flags': i.flags}
                for i in room.items
            ],
            'corpses': [
                {'name': c.name, 'inventory': [{'name': it.name, 'description': it.description,
                                                'price': it.price} for it in c.inventory]}
                for c in room.corpses
            ],
            'door_states': room.door_states,
            'event_cooldown': room.event_cooldown
        })
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"World saved → {filename}")

def load_world(rooms, players, filename="world_save.json"):
    if not os.path.exists(filename):
        print("No save file found.")
        return
    with open(filename) as f:
        saved = json.load(f)
    for entry in saved:
        room = next((r for r in rooms if r.name == entry['name']), None)
        if not room:
            continue
        # restore NPCs
        room.npcs = []
        for nd in entry['npcs']:
            proto = next((p for p in room.original_npcs if p.name == nd['name']), None)
            if not proto: continue
            new_n = NPC(proto.name, proto.description, proto.actions, nd['hp'],
                        proto.max_hp, proto.xp_value, proto.inventory,
                        proto.guildmaster, proto.trainable_skills, proto.quests,
                        controller=next((pl for pl in players if pl.name==nd['controller']), None))
            new_n.respawn_timer = nd['respawn_timer']
            new_n.effects = nd['effects']
            room.npcs.append(new_n)
        # restore items & corpses
        room.items = [Item(**it) for it in entry['items']]
        room.corpses = [Item(c['name'], "", container=True,
                             inventory=[Item(**sub) for sub in c['inventory']])
                        for c in entry['corpses']]
        room.door_states = entry['door_states']
        room.event_cooldown = entry['event_cooldown']
    print(f"World loaded ← {filename}")

def respawn_npcs(rooms):
    for room in rooms:
        for npc in room.npcs[:]:
            if npc.hp <= 0 and npc.respawn_timer > 0:
                npc.respawn_timer -= 1
                if npc.respawn_timer <= 0:
                    proto = next((p for p in room.original_npcs if p.name==npc.name), None)
                    if proto:
                        new_n = NPC(proto.name, proto.description, proto.actions,
                                    proto.max_hp, proto.max_hp, proto.xp_value,
                                    proto.inventory, proto.guildmaster,
                                    proto.trainable_skills, proto.quests)
                        room.npcs.remove(npc)
                        room.npcs.append(new_n)
                        print(f"{new_n.name} respawned in {room.name}")
