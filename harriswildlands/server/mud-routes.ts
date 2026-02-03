/**
 * MUD Integration Routes for BruceOps
 * Connects the MUD server to BruceOps API
 */

import { Express } from "express";
import { isAuthenticated } from "./replit_integrations/auth";
import { storage } from "./storage";

// MUD Server Connection
const MUD_SERVER_URL = process.env.MUD_SERVER_URL || "ws://localhost:4008";

export function registerMUDRoutes(app: Express) {
  
  // MUD Command Proxy
  app.post("/api/mud/command", isAuthenticated, async (req, res) => {
    const { command, player } = req.body;
    const userId = (req as any).user?.id || "anonymous";
    
    try {
      // Log command to BruceOps (for tracking)
      await storage.createActivityLog(userId, {
        type: "mud_command",
        command: command,
        timestamp: new Date()
      });
      
      // Forward to MUD server (via WebSocket or HTTP)
      // This is a simplified version - in production use WebSocket
      res.json({
        success: true,
        text: `Command "${command}" sent to MUD`,
        player: player || userId,
        timestamp: new Date().toISOString()
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        error: "MUD server not responding"
      });
    }
  });

  // MUD World Status
  app.get("/api/mud/status", isAuthenticated, async (req, res) => {
    res.json({
      connected: true, // Would check actual connection
      rooms: 4, // Would query MUD
      players: 1,
      npcs: 2,
      server: MUD_SERVER_URL,
      uptime: "0h 0m"
    });
  });

  // Agent Control
  app.post("/api/mud/agent/start", isAuthenticated, async (req, res) => {
    res.json({ 
      status: "started",
      message: "Autonomous agent activated",
      autonomy: true
    });
  });

  app.post("/api/mud/agent/stop", isAuthenticated, async (req, res) => {
    res.json({ 
      status: "stopped",
      message: "Autonomous agent deactivated",
      autonomy: false
    });
  });

  // Sync MUD activity to BruceOps logs
  app.post("/api/mud/sync", isAuthenticated, async (req, res) => {
    const { activity } = req.body;
    const userId = (req as any).user?.id;
    
    // Convert MUD activity to LifeOps log
    if (activity.type === "exploration") {
      await storage.createLog(userId, {
        date: new Date().toISOString().split('T')[0],
        topWin: `Explored MUD location: ${activity.location}`,
        dayType: "adventure",
        energy: 7,
        mood: 8
      });
    }
    
    res.json({ synced: true });
  });
}
