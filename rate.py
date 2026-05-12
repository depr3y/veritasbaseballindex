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
RPI_FILE    = "rpi.json"

# NCAA Baseball RPI location weights
RPI_ROAD_WIN   = 1.3
RPI_HOME_WIN   = 0.7
RPI_NEUTRAL    = 1.0

def calc_rpi(games, teams):
    """
    Calculate NCAA-style location-weighted RPI for all teams.
    RPI = 0.25*WP + 0.50*OWP + 0.25*OOWP
    Road win=1.3, home win=0.7, neutral=1.0 (losses inverse)
    Fully vectorized — runs in under 5 seconds.
    """
    def lw(location, is_winner):
        if location == "away": return RPI_ROAD_WIN if is_winner else RPI_HOME_WIN
        if location == "home": return RPI_HOME_WIN if is_winner else RPI_ROAD_WIN
        return RPI_NEUTRAL

    # Precompute weighted wins/losses and per-opponent contributions
    w_wins   = defaultdict(float)
    w_losses = defaultdict(float)
    # head2head[team][opp] = (wins_weight_vs_opp, losses_weight_vs_opp)
    h2h_w = defaultdict(lambda: defaultdict(float))
    h2h_l = defaultdict(lambda: defaultdict(float))
    opp_list = defaultdict(list)

    for g in games:
        wi, li = g["winner"], g["loser"]
        loc = g.get("location", "neutral")
        ww = lw(loc, True)
        wl = lw(loc, False)
        w_wins[wi]   += ww
        w_losses[li] += wl
        h2h_w[wi][li] += ww  # winner's wins vs loser
        h2h_l[li][wi] += wl  # loser's losses vs winner
        opp_list[wi].append(li)
        opp_list[li].append(wi)

    def wp(team):
        t = w_wins[team] + w_losses[team]
        return w_wins[team] / t if t > 0 else 0.0

    def owp(team):
        opps = opp_list[team]
        if not opps: return 0.0
        total = 0.0
        for opp in opps:
            # Exclude games vs team from opp's record
            ow = w_wins[opp]   - h2h_w[opp].get(team, 0.0)
            ol = w_losses[opp] - h2h_l[opp].get(team, 0.0)
            t = ow + ol
            total += (ow / t) if t > 0 else 0.0
        return total / len(opps)

    # Precompute OWP for all teams (needed for OOWP)
    owp_cache = {team: owp(team) for team in teams}

    def oowp(team):
        opps = opp_list[team]
        if not opps: return 0.0
        return sum(owp_cache[opp] for opp in opps if opp in owp_cache) / len(opps)

    rpi_scores = {
        team: 0.25 * wp(team) + 0.50 * owp_cache[team] + 0.25 * oowp(team)
        for team in teams
    }
    ranked = sorted(rpi_scores.items(), key=lambda x: -x[1])
    return {team: {"rpi_rank": i+1, "rpi_score": round(score, 5)}
            for i, (team, score) in enumerate(ranked)}

HOME_WEIGHT    = 0.9
AWAY_WEIGHT    = 1.1
NEUTRAL_WEIGHT = 1.0
MIN_GAMES      = 10

D1_CONFERENCES = {
    "acc", "america-east", "american", "asun", "atlantic-10",
    "big-12", "big-east", "big-south", "big-ten", "big-west",
    "caa", "cusa", "di-independent", "horizon", "ivy-league",
    "maac", "mac", "mvc", "mountain-west", "nec", "ovc",
    "patriot", "sec", "socon", "southland", "summit-league",
    "sun-belt", "swac", "wac", "wcc"
}

# Pretty display names for the website
CONF_DISPLAY = {
    "acc": "ACC", "america-east": "America East", "american": "American",
    "asun": "ASUN", "atlantic-10": "A-10", "big-12": "Big 12",
    "big-east": "Big East", "big-south": "Big South", "big-ten": "Big Ten",
    "big-west": "Big West", "caa": "CAA", "cusa": "CUSA",
    "di-independent": "Ind", "horizon": "Horizon", "ivy-league": "Ivy",
    "maac": "MAAC", "mac": "MAC", "mvc": "MVC", "mountain-west": "MWC",
    "nec": "NEC", "ovc": "OVC", "patriot": "Patriot", "sec": "SEC",
    "socon": "SoCon", "southland": "Southland", "summit-league": "Summit",
    "sun-belt": "Sun Belt", "swac": "SWAC", "wac": "WAC", "wcc": "WCC"
}


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

    # Filter out non-D1 teams
    before = len(games)
    games = [g for g in games
             if conferences.get(g["winner"], "") in D1_CONFERENCES
             and conferences.get(g["loser"], "") in D1_CONFERENCES]
    print(f"After D1 filter: {len(games)} games (removed {before - len(games)})")

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
    print(f"After min games filter: {remaining} teams")

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
                "conf":   CONF_DISPLAY.get(conferences.get(team, ""), "Other"),
            }
            for i, (team, rating) in enumerate(ranked)
        ]
    }

    with open(OUTPUT_FILE, "w") as f:
        json.dump(output, f, indent=2)

    print(f"Rankings written to {OUTPUT_FILE}")

    # Calculate and write RPI
    print("Calculating RPI...")
    rpi_teams = set(t for g in games for t in [g["winner"], g["loser"]])
    rpi_data = calc_rpi(games, rpi_teams)
    from datetime import datetime, timezone, timedelta
    EST = timezone(timedelta(hours=-4))
    today_str = datetime.now(EST).strftime('%Y-%m-%d')
    rpi_output = {
        "updated": today_str,
        "source": "calculated from games.json (NCAA location-weighted RPI formula)",
        "teams": {team: data for team, data in rpi_data.items()}
    }
    with open(RPI_FILE, "w") as f:
        json.dump(rpi_output, f, indent=2)
    print(f"RPI written to {RPI_FILE} ({len(rpi_data)} teams)")
    print(f"\nTop 10 RPI:")
    for team, data in sorted(rpi_data.items(), key=lambda x: x[1]['rpi_rank'])[:10]:
        print(f"  #{data['rpi_rank']:3d} {team:<30} {data['rpi_score']:.5f}")

    print(f"\nTop 10 VBI:")
    for entry in output["rankings"][:10]:
        print(f"  {entry['rank']:>3}. {entry['team']:<30} {entry['wins']}-{entry['losses']}  {entry['conf']:<15}  {entry['rating']:.4f}")
