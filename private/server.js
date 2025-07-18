// server.js
const express = require('express');
const http = require('http');
const WebSocket = require('ws');
const path = require('path');

const app = express();
const server = http.createServer(app);
const wss = new WebSocket.Server({ server });

// Serve static files from the current directory (ws/)
app.use(express.static(path.join(__dirname)));

// Broadcast a message every 5 seconds to all connected clients
setInterval(() => {
  const message = `Message at ${new Date().toLocaleTimeString()}`;
  wss.clients.forEach(client => {
    if (client.readyState === WebSocket.OPEN) {
      client.send(message);
    }
  });
}, 1000);

wss.on('connection', ws => {
  console.log('WebSocket client connected');
  ws.send('Welcome to the WebXR WebSocket server!');
});

const PORT = 8081;
server.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}/`);
});
