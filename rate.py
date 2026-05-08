"""
Veritas Baseball Index — Rating Engine
----------------------------------------
Reads games.json and team_conferences.json,
runs the Colley Matrix, writes rankings.json.

Usage:
    python rate.py
"""

import json
import numpy as np
from collections import defaultdict, Counter
from datetime import date
import os

GAMES_FILE  = "games.json"
CONF_FILE   = "team_conferences.json"
OUTPUT_FILE = "rankings.json"

HOME_WEIGHT    = 0.9
AWAY_WEIGHT    = 1.1
NEUTRAL_WEIGHT = 1.0
MIN_GAMES      = 10


def load_conferences():
    if os.path.exists(CONF_FILE):
        with open(CONF_FILE) as f:
            return json.load(f)
    return {}


def build_ratings(games):
    teams = sorted(set(t for g in games for t in [g["winner"], g["loser"]]))
    n = len(teams)
    idx = {t: i for i, t in enumerate(teams)}

    wins     = defaultdict(float)
    losses   = defaultdict(float)
    matchups = defaultdict(float)

    for g in games:
        w, l  = g["winner"], g["loser"]
        loc   = g.get("location", "neutral")
        weight = {"home": HOME_WEIGHT, "away": AWAY_WEIGHT, "neutral": NEUTRAL_WEIGHT}.get(loc, 1.0)

        wins[w]   += weight
        losses[l] += weight
        matchups[(idx[w], idx[l])] += weight
        matchups[(idx[l], idx[w])] += weight

    C = np.zeros((n, n))
    b = np.zeros(n)

    for i, team in enumerate(teams):
        total = wins[team] + losses[team]
        C[i][i] = 2 + total
        b[i]    = 1 + (wins[team] - losses[team]) / 2

    for (i, j), count in matchups.items():
        if i != j:
            C[i][j] -= count

    ratings_vec = np.linalg.solve(C, b)
    return {team: float(ratings_vec[idx[team]]) for team in teams}


if __name__ == "__main__":
    with open(GAMES_FILE) as f:
        games = json.load(f)

    print(f"Loaded {len(games)} games...")

    conferences = load_conferences()
    print(f"Loaded conferences for {len(conferences)} teams")

    # Raw win/loss counts
    raw_wins   = defaultdict(int)
    raw_losses = defaultdict(int)
    for g in games:
        raw_wins[g["winner"]]  += 1
        raw_losses[g["loser"]] += 1

    # Filter teams with fewer than MIN_GAMES
    game_counts = Counter()
    for g in games:
        game_counts[g["winner"]] += 1
        game_counts[g["loser"]]  += 1

    games = [g for g in games
             if game_counts[g["winner"]] >= MIN_GAMES
             and game_counts[g["loser"]] >= MIN_GAMES]

    remaining = len(set(t for g in games for t in [g["winner"], g["loser"]]))
    print(f"After filtering (<{MIN_GAMES} games): {remaining} teams")

    ratings = build_ratings(games)
    ranked  = sorted(ratings.items(), key=lambda x: x[1], reverse=True)

    output = {
        "generated":   str(date.today()),
        "total_games": len(games),
        "rankings": [
            {
                "rank":   i + 1,
                "team":   team,
                "rating": round(rating, 4),
                "wins":   raw_wins[team],
                "losses": raw_losses[team],
                "conf":   conferences.get(team, "Other"),
            }
            for i, (team, rating) in enumerate(ranked)
        ]
    }

    with open(OUTPUT_FILE, "w") as f:
        json.dump(output, f, indent=2)

    print(f"Rankings written to {OUTPUT_FILE}")
    print(f"\nTop 10:")
    for entry in output["rankings"][:10]:
        print(f"  {entry['rank']:>3}. {entry['team']:<30} {entry['wins']}-{entry['losses']}  {entry['conf']:<15}  {entry['rating']:.4f}")
