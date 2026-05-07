"""
True Earned Rank — Rating Engine
----------------------------------
Reads games.json produced by scraper.py,
runs the Colley Matrix, and writes rankings.json.

Usage:
    python3 rate.py
"""

import json
import numpy as np
from collections import defaultdict
from datetime import date

GAMES_FILE  = "games.json"
OUTPUT_FILE = "rankings.json"

HOME_WEIGHT    = 0.9
AWAY_WEIGHT    = 1.1
NEUTRAL_WEIGHT = 1.0


def build_ratings(games):
    teams = sorted(set(t for g in games for t in [g["winner"], g["loser"]]))
    n = len(teams)
    idx = {t: i for i, t in enumerate(teams)}

    wins     = defaultdict(float)
    losses   = defaultdict(float)
    matchups = defaultdict(float)

    for g in games:
        w, l = g["winner"], g["loser"]
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
    return {team: float(ratings_vec[idx[team]]) for team in teams}, wins, losses


def compute_record(wins, losses, team):
    """Return integer win/loss counts (unweighted) from raw games list."""
    return wins[team], losses[team]


if __name__ == "__main__":
    with open(GAMES_FILE) as f:
        games = json.load(f)

    print(f"Loaded {len(games)} games...")

    # Build unweighted win/loss counts for display
    raw_wins    = defaultdict(int)
    raw_losses  = defaultdict(int)
    for g in games:
        raw_wins[g["winner"]]  += 1
        raw_losses[g["loser"]] += 1

    ratings, _, _ = build_ratings(games)

    # Sort by rating descending
    ranked = sorted(ratings.items(), key=lambda x: x[1], reverse=True)

    output = {
        "generated": str(date.today()),
        "total_games": len(games),
        "rankings": [
            {
                "rank":   i + 1,
                "team":   team,
                "rating": round(rating, 4),
                "wins":   raw_wins[team],
                "losses": raw_losses[team],
            }
            for i, (team, rating) in enumerate(ranked)
        ]
    }

    with open(OUTPUT_FILE, "w") as f:
        json.dump(output, f, indent=2)

    print(f"Rankings written to {OUTPUT_FILE}")
    print(f"\nTop 10:")
    for entry in output["rankings"][:10]:
        print(f"  {entry['rank']:>3}. {entry['team']:<30} {entry['wins']}-{entry['losses']}  {entry['rating']:.4f}")
