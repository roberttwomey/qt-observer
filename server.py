import asyncio
import websockets
import http.server
import socketserver
import threading
from datetime import datetime
import json
import random


HTTP_PORT = 8080
WS_PORT = 8081

quantum_notes = [
    "quantum eraser",
    "we could be walking along a diagram (feynman diagram), performing an electron",
    "re-performing a diagram, as a ritual (kind of like Augusto Boal)",
    "choreographing a feynman diagram. in a diagram there are different things that can happen (or not happen). so there is a way of performing this that we could maintain that chance process",
    "Quantum, it's probabilistic — so in individual instances you don't know where it might go, but in aggregate over time you see those distributions",
    "the moments where the improvisational choice happens, corresponds to the observation, moment of choice/observation/measurement",
    "once the light hits the screen an observation has been made",
    "light, photons, polarization patterns",
    "transverse wave",
    "all states of light (polarization) are some combination of horizontal and vertical",
    "beam intensity dropped (cos() ^ 2 of the difference between the angles)",
    "light comes in all oscillating at one angle, only part gets through, but all the light that comes through is now oscillating vertically",
    "each individual photon either gets through or doesn't (quantum) as opposed to 80%",
    "bell's theorem (hidden variables and non-local influence)",
    "Quantum is local, deterministic, no hidden variables",
    "possibilities",
    "it's random",
    "both possibilities happen (many worlds)",
    "there are non-local",
    "slow down time, dramatize, moment of choice //",
    "temporal microscope",
    "using a strobe or something else to demarcate time or give a sense of slowing down or speeding up",
    "temporal zoom",
    "Copenhagen"
]
# 
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
            now = datetime.now().strftime('%H:%M:%S')
            # Every 10 seconds, send an audio message
            if count == 4:
                audio_msg = {"type": "audio", "file": "media/ding.mp3"}
                await websocket.send(json.dumps(audio_msg))
            if count == 5:
                toggle = not toggle
                count = 0
                msg = {"type": "toggle_transparency", "transparent": str(toggle)}
                await websocket.send(json.dumps(msg))
                
                msg = {"type": "text", "text": f"{random.choice(quantum_notes)}"}
                await websocket.send(json.dumps(msg))
            

            count += 1
            # msg = {"type": "text", "text": f"Message at {now}"}
            # await websocket.send(json.dumps(msg))
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
