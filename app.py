#!/usr/bin/env python3
"""Flask server for ReelChain — the film-to-film actor-bridge puzzle game.

The game (reelchain_game.html) is fully self-contained: the cast graph is
embedded and all puzzle logic runs client-side. This server just serves it.
The old "lookup tool" UI (index.html + /api/* endpoints) is gone — the game
IS the app now.

Run:  pip install flask && python app.py
Then: http://127.0.0.1:5055

To refresh the embedded graph/films after editing data.json, rerun build_game.py.
"""
import os
from flask import Flask, send_from_directory, abort

app = Flask(__name__)
HERE = os.path.dirname(os.path.abspath(__file__))
GAME_FILE = "reelchain_game.html"


@app.route("/")
def index():
    # Serve the self-contained game as the whole app.
    return send_from_directory(HERE, GAME_FILE)


@app.route("/game")
@app.route("/index.html")
@app.route("/reelchain_game.html")
def game():
    return send_from_directory(HERE, GAME_FILE)


@app.route("/healthz")
def healthz():
    path = os.path.join(HERE, GAME_FILE)
    return {"ok": os.path.exists(path), "game": GAME_FILE}, 200


if __name__ == "__main__":
    # Bind to 0.0.0.0 so other devices on your LAN (e.g. your phone) can reach it.
    # Access from your phone via http://<YOUR_PC_LAN_IP>:5055
    app.run(host="0.0.0.0", port=5055, debug=False)
