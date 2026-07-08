#!/usr/bin/env python3
"""
Bipartite shortest-path solver for the "connect two films via actors" game.
Graph: films and actors alternate. BFS finds the shortest valid chain.
Also provides validation of a player-submitted chain.
"""
import json
import sys


def load_graph(path="data.json"):
    with open(path, encoding="utf-8") as fh:
        d = json.load(fh)
    return d["films"], d["actors"]


def solve(film_a, film_b, films, actors, max_depth=8):
    """Return list of (film, actor, film, ...) alternating, or None if not connected."""
    if film_a not in films or film_b not in films:
        missing = [f for f in (film_a, film_b) if f not in films]
        return {"error": "unknown_film", "missing": missing}

    if film_a == film_b:
        return {"error": "same_film"}

    # BFS over bipartite graph. State = current film. Track path of (film).
    # We store path as list of films and the actor linking each consecutive pair.
    from collections import deque
    # queue holds (current_film, path_films, path_actors)
    start = (film_a, [film_a], [])
    q = deque([start])
    visited_film = {film_a}
    visited_actor = set()

    while q:
        cur, path_f, path_a = q.popleft()
        if len(path_f) - 1 > max_depth:
            continue
        for actor in films.get(cur, []):
            if actor in visited_actor and actor not in actors:
                pass
            # expand actor -> neighbor films
            for nxt in actors.get(actor, []):
                if nxt in visited_film:
                    continue
                new_path_f = path_f + [nxt]
                new_path_a = path_a + [actor]
                if nxt == film_b:
                    return {
                        "connected": True,
                        "steps": len(new_path_a),
                        "chain": build_chain(new_path_f, new_path_a),
                    }
                visited_film.add(nxt)
                q.append((nxt, new_path_f, new_path_a))
    return {"connected": False}


def build_chain(path_f, path_a):
    # path_f: [F1, F2, ..., Fn]; path_a: [A1, ..., A(n-1)]
    chain = []
    for i, f in enumerate(path_f):
        chain.append({"type": "film", "name": f})
        if i < len(path_a):
            chain.append({"type": "actor", "name": path_a[i]})
    return chain


def validate_chain(chain_films, chain_actors, films):
    """Validate a player-submitted chain: F1, A1, F2, A2, ..., Fn.
    chain_films = [F1, F2, ...]; chain_actors = [A1, A2, ...]
    Rules: each actor Ai must be in both Fi and F(i+1)'s cast.
    """
    if not chain_films or len(chain_films) < 2:
        return {"valid": False, "reason": "need at least two films"}
    if len(chain_actors) != len(chain_films) - 1:
        return {"valid": False, "reason": "each pair of films must be linked by exactly one actor"}
    for f in chain_films:
        if f not in films:
            return {"valid": False, "reason": "unknown film: %s" % f}
    for i, a in enumerate(chain_actors):
        fa = chain_films[i]
        fb = chain_films[i + 1]
        if a not in films.get(fa, []):
            return {"valid": False, "reason": "%s is not in the cast of %s" % (a, fa)}
        if a not in films.get(fb, []):
            return {"valid": False, "reason": "%s is not in the cast of %s" % (a, fb)}
    return {"valid": True, "steps": len(chain_actors)}


if __name__ == "__main__":
    films, actors = load_graph()
    # Test cases
    tests = [
        ("The Godfather", "Pulp Fiction"),
        ("Star Wars", "The Dark Knight"),
        ("Forrest Gump", "Mad Max: Fury Road"),
        ("The Matrix", "Jurassic Park"),
    ]
    for a, b in tests:
        r = solve(a, b, films, actors)
        print("=== %s -> %s ===" % (a, b))
        if "error" in r:
            print("  error:", r)
        elif not r.get("connected"):
            print("  NOT CONNECTED")
        else:
            print("  steps:", r["steps"])
            print("  chain:", " -> ".join(x["name"] for x in r["chain"]))
