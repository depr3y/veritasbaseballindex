"""
True Earned Rank — NCAA D1 Baseball Scraper
--------------------------------------------
Uses the free public NCAA API (ncaa-api.henrygd.me) instead of scraping
stats.ncaa.org directly — no 403 errors, no browser spoofing needed.

Usage:
    python scraper.py                    # scrape today's games
    python scraper.py --date 2026-05-06  # scrape a specific date
    python scraper.py --full-season      # scrape all games since Feb 14
"""

import requests
import json
import time
import argparse
from datetime import date, timedelta
import os

BASE_URL   = "https://ncaa-api.henrygd.me"
GAMES_FILE = "games.json"

HEADERS = {
    "User-Agent": "TrueEarnedRank/1.0 (college baseball rating project)"
}


def load_existing_games():
    if os.path.exists(GAMES_FILE):
        with open(GAMES_FILE) as f:
            return json.load(f)
    return []


def save_games(games):
    with open(GAMES_FILE, "w") as f:
        json.dump(games, f, indent=2)
    print(f"Saved {len(games)} total games to {GAMES_FILE}")


def scrape_date(target_date):
    date_str = target_date.strftime("%Y/%m/%d")
    url = f"{BASE_URL}/scoreboard/baseball/d1/{date_str}"

    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        if r.status_code == 404:
            return []
        r.raise_for_status()
        data = r.json()
    except requests.RequestException as e:
        print(f"  Error fetching {target_date}: {e}")
        return []
    except json.JSONDecodeError:
        print(f"  Bad response for {target_date}")
        return []

    games = []

    for game in data.get("games", []):
        g = game.get("game", {})

        home_team  = g.get("home", {}).get("names", {}).get("short", "")
        away_team  = g.get("away", {}).get("names", {}).get("short", "")
        home_score = g.get("home", {}).get("score", "")
        away_score = g.get("away", {}).get("score", "")

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
            "winner":   winner,
            "loser":    loser,
            "location": location,
            "date":     str(target_date)
        })

    return games


def all_dates_this_season():
    season_start = date(2026, 2, 14)
    today = date.today()
    dates = []
    current = season_start
    while current <= today:
        dates.append(current)
        current += timedelta(days=1)
    return dates


def deduplicate(games):
    seen = set()
    unique = []
    for g in games:
        key = (g["winner"], g["loser"], g["date"])
        if key not in seen:
            seen.add(key)
            unique.append(g)
    return unique


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", help="Specific date (YYYY-MM-DD)")
    parser.add_argument("--full-season", action="store_true")
    args = parser.parse_args()

    existing = load_existing_games()
    new_games = []

    if args.full_season:
        dates = all_dates_this_season()
        print(f"Scraping full season: {len(dates)} dates...")
        for i, d in enumerate(dates):
            print(f"  [{i+1}/{len(dates)}] {d}...", end=" ", flush=True)
            days_games = scrape_date(d)
            print(f"{len(days_games)} games")
            new_games.extend(days_games)
            time.sleep(0.5)

    elif args.date:
        target = date.fromisoformat(args.date)
        print(f"Scraping {target}...")
        new_games = scrape_date(target)
        print(f"  Found {len(new_games)} games")

    else:
        today = date.today()
        print(f"Scraping today ({today})...")
        new_games = scrape_date(today)
        print(f"  Found {len(new_games)} games")

    all_games = deduplicate(existing + new_games)
    save_games(all_games)
