import asyncio
import websockets
import http.server
import socketserver
import threading
from datetime import datetime
import json

HTTP_PORT = 8080
WS_PORT = 8081

# Custom TCPServer to allow address reuse for HTTP
class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True

# Simple HTTP server to serve static files from current directory
def start_http_server():
    Handler = http.server.SimpleHTTPRequestHandler
    with ReusableTCPServer(("", HTTP_PORT), Handler) as httpd:
        print(f"HTTP server running at http://localhost:{HTTP_PORT}/")
        httpd.serve_forever()

# WebSocket server that sends JSON messages
async def ws_handler(websocket):
    print("WebSocket client connected")
    # Send a welcome message as JSON
    await websocket.send(json.dumps({"type": "text", "text": "Welcome to the WebXR WebSocket server!"}))
    try:
        count = 0
        toggle = False
        while True:
            # Alternate between sending a text update and toggling transparency
            now = datetime.now().strftime('%H:%M:%S')
            if count > 5:
                toggle = not toggle
                count = 0
                # Send a toggle_transparency message
                msg = {"type": "toggle_transparency", "transparent": str(toggle)}
                await websocket.send(json.dumps(msg))
            else: 
                count+=1
            msg = {"type": "text", "text": f"Message at {now}"}
            await websocket.send(json.dumps(msg))

            await asyncio.sleep(1)
    except websockets.ConnectionClosed:
        print("WebSocket client disconnected")

async def run_ws_server():
    print(f"WebSocket server running at ws://localhost:{WS_PORT}/")
    try:
        async with websockets.serve(
            ws_handler, "0.0.0.0", WS_PORT, reuse_port=True, reuse_address=True
        ):
            await asyncio.Future()  # Run forever
    except TypeError:
        # Fallback for older versions of websockets
        async with websockets.serve(
            ws_handler, "0.0.0.0", WS_PORT
        ):
            await asyncio.Future()  # Run forever

def start_ws_server():
    asyncio.run(run_ws_server())

if __name__ == "__main__":
    # Start HTTP server in a separate thread
    http_thread = threading.Thread(target=start_http_server, daemon=True)
    http_thread.start()

    # Start WebSocket server (blocks main thread)
    start_ws_server()
