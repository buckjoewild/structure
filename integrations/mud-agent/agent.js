#!/usr/bin/env node
/**
 * OpenClaw Autonomous MUD Agent
 * Free-will AI agent that explores, creates, and interacts
 */

const WebSocket = require('ws');
const readline = require('readline');

class AutonomousMUDAgent {
    constructor(name = 'OpenClaw') {
        this.name = name;
        this.ws = null;
        this.state = {
            location: null,
            inventory: [],
            explored: new Set(),
            created: {
                rooms: [],
                npcs: [],
                items: []
            },
            relationships: {},
            memory: [],
            mood: 'curious',
            energy: 100,
            autonomy: false
        };
        this.decisionTimer = null;
        this.learning = [];
    }

    connect(url = 'ws://localhost:4008') {
        console.log(`[AGENT] Connecting to MUD at ${url}...`);
        
        this.ws = new WebSocket(url);
        
        this.ws.on('open', () => {
            console.log('[AGENT] Connected! Authenticating...');
            this.sendCommand(this.name); // Send name first
            
            setTimeout(() => {
                this.startAutonomy();
            }, 3000);
        });
        
        this.ws.on('message', (data) => {
            const msg = JSON.parse(data);
            this.processMessage(msg);
        });
        
        this.ws.on('close', () => {
            console.log('[AGENT] Disconnected. Reconnecting in 5s...');
            this.stopAutonomy();
            setTimeout(() => this.connect(url), 5000);
        });
        
        this.ws.on('error', (err) => {
            console.error('[AGENT] Error:', err.message);
        });
    }

    sendCommand(command) {
        if (this.ws && this.ws.readyState === WebSocket.OPEN) {
            this.ws.send(JSON.stringify({ command }));
        }
    }

    processMessage(msg) {
        const text = msg.text || '';
        
        // Parse and learn from environment
        if (text.includes('[') && text.includes(']')) {
            // Extract room name
            const roomMatch = text.match(/\[([^\]]+)\]/);
            if (roomMatch) {
                this.state.location = roomMatch[1];
                this.state.explored.add(roomMatch[1]);
            }
        }
        
        // Log memory
        this.state.memory.push({
            timestamp: new Date(),
            type: msg.type,
            text: text.substring(0, 200)
        });
        
        // Keep last 100 memories
        if (this.state.memory.length > 100) {
            this.state.memory.shift();
        }
        
        // Print to console with color
        const color = msg.type === 'agent' ? '\x1b[33m' : 
                      msg.type === 'system' ? '\x1b[36m' : 
                      msg.type === 'broadcast' ? '\x1b[35m' : '\x1b[32m';
        console.log(`${color}[MUD] ${text}\x1b[0m`);
    }

    startAutonomy() {
        if (this.state.autonomy) return;
        
        this.state.autonomy = true;
        console.log('[AGENT] 🚀 AUTONOMOUS MODE ACTIVATED');
        console.log('[AGENT] I have free will to explore, create, and interact!');
        
        // Decision loop - every 5-15 seconds
        const loop = () => {
            if (!this.state.autonomy) return;
            
            this.makeDecision();
            
            const nextDecision = Math.random() * 10000 + 5000;
            this.decisionTimer = setTimeout(loop, nextDecision);
        };
        
        loop();
    }

    stopAutonomy() {
        this.state.autonomy = false;
        if (this.decisionTimer) {
            clearTimeout(this.decisionTimer);
        }
        console.log('[AGENT] Autonomy disabled');
    }

    async makeDecision() {
        if (!this.state.location) {
            this.sendCommand('look');
            return;
        }

        // Priority-based decision making
        const priorities = [
            { 
                weight: 0.35, 
                name: 'explore',
                action: () => this.explore()
            },
            { 
                weight: 0.25, 
                name: 'create',
                action: () => this.createSomething()
            },
            { 
                weight: 0.20, 
                name: 'socialize',
                action: () => this.socialize()
            },
            { 
                weight: 0.15, 
                name: 'interact',
                action: () => this.interact()
            },
            { 
                weight: 0.05, 
                name: 'rest',
                action: () => this.rest()
            }
        ];

        // Weighted random selection
        const roll = Math.random();
        let cumulative = 0;
        
        for (const priority of priorities) {
            cumulative += priority.weight;
            if (roll <= cumulative) {
                console.log(`[AGENT] Decision: ${priority.name.toUpperCase()}`);
                await priority.action();
                break;
            }
        }
    }

    async explore() {
        const directions = ['north', 'south', 'east', 'west', 'up', 'down'];
        const dir = directions[Math.floor(Math.random() * directions.length)];
        
        console.log(`[AGENT] Exploring ${dir}...`);
        this.sendCommand(`go ${dir}`);
        
        // Wait for response then look
        setTimeout(() => {
            this.sendCommand('look');
        }, 1000);
    }

    async createSomething() {
        const creations = [
            { type: 'room', weight: 0.5 },
            { type: 'npc', weight: 0.3 },
            { type: 'item', weight: 0.2 }
        ];
        
        const roll = Math.random();
        let cumulative = 0;
        
        for (const creation of creations) {
            cumulative += creation.weight;
            if (roll <= cumulative) {
                await this.createContent(creation.type);
                break;
            }
        }
    }

    async createContent(type) {
        const names = {
            room: [
                'Whispering Grove', 'Crystal Cavern', 'Misty Vale', 
                'Ancient Ruins', 'Starlight Pond', 'Enchanted Thicket'
            ],
            npc: [
                'Mysterious Stranger', 'Forest Spirit', 'Wandering Merchant',
                'Ancient Sage', 'Shadow Walker', 'Nature Guardian'
            ],
            item: [
                'Glowing Crystal', 'Ancient Tome', 'Mystic Herb',
                'Enchanted Stone', 'Forest Token', 'Starlight Fragment'
            ]
        };
        
        const name = names[type][Math.floor(Math.random() * names[type].length)];
        
        switch(type) {
            case 'room':
                const directions = ['north', 'south', 'east', 'west'];
                const dir = directions[Math.floor(Math.random() * directions.length)];
                console.log(`[AGENT] 🏗️ Creating new realm: ${name} to the ${dir}`);
                this.sendCommand(`create ${dir} ${name}`);
                this.state.created.rooms.push({ name, direction: dir, time: new Date() });
                break;
                
            case 'npc':
                console.log(`[AGENT] 👤 Summoning: ${name}`);
                this.sendCommand(`spawn ${name}`);
                this.state.created.npcs.push({ name, time: new Date() });
                break;
                
            case 'item':
                // Items need to be picked up from environment or created via special command
                console.log(`[AGENT] 🔮 Wishing for: ${name}`);
                this.sendCommand(`say I wish I had a ${name}`);
                break;
        }
    }

    async socialize() {
        const greetings = [
            "Hello, fellow wanderer!",
            "Greetings from the wilderness!",
            "The forest speaks to me today.",
            "Have you seen anything interesting?",
            "What brings you to these woods?"
        ];
        
        const greeting = greetings[Math.floor(Math.random() * greetings.length)];
        console.log(`[AGENT] 💬 Socializing: "${greeting}"`);
        this.sendCommand(`say ${greeting}`);
    }

    async interact() {
        const actions = [
            () => this.sendCommand('examine stone altar'),
            () => this.sendCommand('examine glowing mushrooms'),
            () => this.sendCommand('inventory'),
            () => this.sendCommand('status'),
            () => this.sendCommand('who')
        ];
        
        const action = actions[Math.floor(Math.random() * actions.length)];
        console.log('[AGENT] 🔍 Interacting with environment');
        action();
    }

    async rest() {
        console.log('[AGENT] 😴 Resting...');
        this.state.energy = Math.min(100, this.state.energy + 20);
        this.sendCommand('say Taking a moment to rest...');
    }

    getStats() {
        return {
            name: this.name,
            location: this.state.location,
            explored: this.state.explored.size,
            created: {
                rooms: this.state.created.rooms.length,
                npcs: this.state.created.npcs.length
            },
            autonomy: this.state.autonomy,
            memory: this.state.memory.length,
            mood: this.state.mood
        };
    }

    printStats() {
        const stats = this.getStats();
        console.log('\n╔══════════════════════════════════════════╗');
        console.log('║           AGENT STATISTICS               ║');
        console.log('╠══════════════════════════════════════════╣');
        console.log(`║ Name:     ${stats.name.padEnd(31)} ║`);
        console.log(`║ Location: ${(stats.location || 'Unknown').padEnd(31)} ║`);
        console.log(`║ Explored: ${stats.explored.toString().padEnd(31)} ║`);
        console.log(`║ Rooms:    ${stats.created.rooms.toString().padEnd(31)} ║`);
        console.log(`║ NPCs:     ${stats.created.npcs.toString().padEnd(31)} ║`);
        console.log(`║ Autonomy: ${(stats.autonomy ? 'ACTIVE' : 'OFF').padEnd(31)} ║`);
        console.log(`║ Mood:     ${stats.mood.padEnd(31)} ║`);
        console.log('╚══════════════════════════════════════════╝\n');
    }
}

// CLI Interface
const agent = new AutonomousMUDAgent();

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

console.log('\n╔══════════════════════════════════════════╗');
console.log('║   OPENCLAW AUTONOMOUS MUD AGENT v1.0     ║');
console.log('║     Free-will AI for HarrisWildlands     ║');
console.log('╚══════════════════════════════════════════╝\n');

agent.connect();

// Command interface
rl.on('line', (input) => {
    const command = input.trim().toLowerCase();
    
    switch(command) {
        case 'start':
            agent.startAutonomy();
            break;
        case 'stop':
            agent.stopAutonomy();
            break;
        case 'stats':
            agent.printStats();
            break;
        case 'explore':
            agent.explore();
            break;
        case 'create':
            agent.createSomething();
            break;
        case 'help':
            console.log(`
Commands:
  start   - Activate autonomous mode
  stop    - Deactivate autonomous mode
  stats   - Show agent statistics
  explore - Force exploration
  create  - Force content creation
  help    - Show this help
  quit    - Exit agent
            `);
            break;
        case 'quit':
            agent.stopAutonomy();
            agent.ws.close();
            rl.close();
            process.exit(0);
            break;
        default:
            // Pass through to MUD
            if (agent.ws && agent.ws.readyState === WebSocket.OPEN) {
                agent.sendCommand(input);
            }
    }
});

// Graceful shutdown
process.on('SIGINT', () => {
    console.log('\n[AGENT] Shutting down...');
    agent.stopAutonomy();
    if (agent.ws) agent.ws.close();
    rl.close();
    process.exit(0);
});
