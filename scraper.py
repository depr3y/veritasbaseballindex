"""
Veritas Baseball Index — NCAA D1 Baseball Scraper
---------------------------------------------------
Scrapes game results, conference data, and box score stats
from ncaa-api.henrygd.me.

Saves:
  games.json            — win/loss/location/date for ratings
  team_conferences.json — team -> conference mapping
  game_stats.json       — full box score stats per game

Usage:
    python scraper.py                    # scrape today
    python scraper.py --date 2026-05-06  # scrape specific date
    python scraper.py --full-season      # scrape entire 2026 season
"""

import requests
import json
import time
import argparse
from datetime import date, timedelta
import os

BASE_URL   = "https://ncaa-api.henrygd.me"
GAMES_FILE = "games.json"
CONF_FILE  = "team_conferences.json"
STATS_FILE = "game_stats.json"

HEADERS = {
    "User-Agent": "VeritasBaseballIndex/1.0 (college baseball rating project)"
}


def load_json(filepath, default):
    if os.path.exists(filepath):
        with open(filepath) as f:
            return json.load(f)
    return default


def save_json(filepath, data):
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)


def fetch_box_score(game_id):
    """Fetch hits/runs/errors for a single completed game."""
    url = f"{BASE_URL}/game/{game_id}/boxscore"
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        if r.status_code != 200:
            return None
        return r.json()
    except Exception:
        return None


def parse_box_score(box_data, game_id, home_team, away_team, winner, loser, game_date):
    """Extract runs, hits, errors from box score response."""
    if not box_data:
        return None

    try:
        teams = box_data.get("teams", [])
        result = {
            "game_id":   game_id,
            "date":      game_date,
            "home_team": home_team,
            "away_team": away_team,
            "winner":    winner,
            "loser":     loser,
        }

        for team in teams:
            name = team.get("team", {}).get("names", {}).get("short", "")
            side = "home" if name == home_team else "away"
            totals = team.get("totals", {})
            result[f"{side}_runs"]   = totals.get("R", "")
            result[f"{side}_hits"]   = totals.get("H", "")
            result[f"{side}_errors"] = totals.get("E", "")
            result[f"{side}_team"]   = name

        return result
    except Exception:
        return None


def scrape_date(target_date, known_confs, existing_game_ids):
    date_str = target_date.strftime("%Y/%m/%d")
    url = f"{BASE_URL}/scoreboard/baseball/d1/{date_str}"

    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        if r.status_code == 404:
            return [], known_confs, []
        r.raise_for_status()
        data = r.json()
    except requests.RequestException as e:
        print(f"  Error fetching {target_date}: {e}")
        return [], known_confs, []
    except json.JSONDecodeError:
        return [], known_confs, []

    games      = []
    new_stats  = []

    for game in data.get("games", []):
        g = game.get("game", {})

        home      = g.get("home", {})
        away      = g.get("away", {})
        game_id   = g.get("gameID", "")

        home_team  = home.get("names", {}).get("short", "")
        away_team  = away.get("names", {}).get("short", "")
        home_score = home.get("score", "")
        away_score = away.get("score", "")

        # Capture conference for each team
        for team, side in [(home_team, home), (away_team, away)]:
            if team and team not in known_confs:
                confs = side.get("conferences", [])
                real_confs = [c["conferenceName"] for c in confs
                              if c.get("conferenceName") not in ("Top 25", "")]
                if real_confs:
                    known_confs[team] = real_confs[0]

        if home_score == "" or away_score == "":
            continue

        try:
            home_score = int(home_score)
            away_score = int(away_score)
        except (ValueError, TypeError):
            continue

        if not home_team or not away_team:
            continue
        if home_score == away_score:
            continue

        if home_score > away_score:
            winner, loser, location = home_team, away_team, "home"
        else:
            winner, loser, location = away_team, home_team, "away"

        games.append({
            "game_id":  game_id,
            "winner":   winner,
            "loser":    loser,
            "location": location,
            "date":     str(target_date),
            "home_team": home_team,
            "away_team": away_team,
            "home_score": home_score,
            "away_score": away_score,
        })

        # Fetch box score if we haven't already
        if game_id and game_id not in existing_game_ids:
            time.sleep(0.3)
            box_data = fetch_box_score(game_id)
            stats = parse_box_score(
                box_data, game_id, home_team, away_team,
                winner, loser, str(target_date)
            )
            if stats:
                new_stats.append(stats)

    return games, known_confs, new_stats


def all_dates_this_season():
    season_start = date(2026, 2, 14)
    today = date.today()
    dates = []
    current = season_start
    while current <= today:
        dates.append(current)
        current += timedelta(days=1)
    return dates


def deduplicate_games(games):
    seen = set()
    unique = []
    for g in games:
        key = (g["winner"], g["loser"], g["date"])
        if key not in seen:
            seen.add(key)
            unique.append(g)
    return unique


def deduplicate_stats(stats):
    seen = set()
    unique = []
    for s in stats:
        if s["game_id"] not in seen:
            seen.add(s["game_id"])
            unique.append(s)
    return unique


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", help="Specific date (YYYY-MM-DD)")
    parser.add_argument("--full-season", action="store_true")
    args = parser.parse_args()

    existing_games = load_json(GAMES_FILE, [])
    known_confs    = load_json(CONF_FILE, {})
    existing_stats = load_json(STATS_FILE, [])

    # Track which game IDs we already have stats for
    existing_game_ids = {s["game_id"] for s in existing_stats}

    new_games = []
    new_stats = []

    if args.full_season:
        dates = all_dates_this_season()
        print(f"Scraping full season: {len(dates)} dates...")
        for i, d in enumerate(dates):
            print(f"  [{i+1}/{len(dates)}] {d}...", end=" ", flush=True)
            days_games, known_confs, days_stats = scrape_date(d, known_confs, existing_game_ids)
            print(f"{len(days_games)} games, {len(days_stats)} box scores")
            new_games.extend(days_games)
            new_stats.extend(days_stats)
            existing_game_ids.update(s["game_id"] for s in days_stats)
            time.sleep(0.5)

    elif args.date:
        target = date.fromisoformat(args.date)
        print(f"Scraping {target}...")
        new_games, known_confs, new_stats = scrape_date(target, known_confs, existing_game_ids)
        print(f"  Found {len(new_games)} games, {len(new_stats)} box scores")

    else:
        today = date.today()
        print(f"Scraping today ({today})...")
        new_games, known_confs, new_stats = scrape_date(today, known_confs, existing_game_ids)
        print(f"  Found {len(new_games)} games, {len(new_stats)} box scores")

    all_games = deduplicate_games(existing_games + new_games)
    all_stats = deduplicate_stats(existing_stats + new_stats)

    save_json(GAMES_FILE, all_games)
    save_json(CONF_FILE, known_confs)
    save_json(STATS_FILE, all_stats)

    print(f"\nSaved {len(all_games)} games, {len(all_stats)} box scores, {len(known_confs)} team conferences")
