"""
Veritas Baseball Index — NCAA D1 Baseball Scraper
---------------------------------------------------
Scrapes game results and conference data from ncaa-api.henrygd.me.
Box scores are optional and only fetched with --box-scores flag.

Usage:
    python scraper.py                              # scrape today (fast)
    python scraper.py --date 2026-05-06            # scrape specific date
    python scraper.py --full-season                # scrape entire season (fast)
    python scraper.py --full-season --box-scores   # scrape + box scores (slow)
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
    url = f"{BASE_URL}/game/{game_id}/boxscore"
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        if r.status_code != 200:
            return None
        return r.json()
    except Exception:
        return None


def parse_box_score(box_data, game_id, home_team, away_team, winner, loser, game_date):
    if not box_data:
        return None
    try:
        teams = box_data.get("teams", [])
        result = {
            "game_id": game_id, "date": game_date,
            "home_team": home_team, "away_team": away_team,
            "winner": winner, "loser": loser,
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


def scrape_date(target_date, known_confs, existing_game_ids, fetch_boxes=False):
    date_str = target_date.strftime("%Y/%m/%d")
    url = f"{BASE_URL}/scoreboard/baseball/d1/{date_str}"

    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        if r.status_code == 404:
            return [], known_confs, []
        r.raise_for_status()
        data = r.json()
    except requests.RequestException as e:
        print(f"  Error: {e}")
        return [], known_confs, []
    except json.JSONDecodeError:
        return [], known_confs, []

    games     = []
    new_stats = []

    for game in data.get("games", []):
        g       = game.get("game", {})
        home    = g.get("home", {})
        away    = g.get("away", {})
        game_id = g.get("gameID", "")

        home_team  = home.get("names", {}).get("short", "")
        away_team  = away.get("names", {}).get("short", "")
        home_score = home.get("score", "")
        away_score = away.get("score", "")

        # Capture conferences
        for team, side in [(home_team, home), (away_team, away)]:
            if team and team not in known_confs:
                confs = side.get("conferences", [])
                real_confs = [c["conferenceSeo"] for c in confs
              if c.get("conferenceSeo") not in ("top-25", "")]
                if real_confs:
                    known_confs[team] = real_confs[0]

        if home_score == "" or away_score == "":
            continue
        try:
            home_score = int(home_score)
            away_score = int(away_score)
        except (ValueError, TypeError):
            continue

        if not home_team or not away_team or home_score == away_score:
            continue

        if home_score > away_score:
            winner, loser, location = home_team, away_team, "home"
        else:
            winner, loser, location = away_team, home_team, "away"

        games.append({
            "game_id": game_id, "winner": winner, "loser": loser,
            "location": location, "date": str(target_date),
            "home_team": home_team, "away_team": away_team,
            "home_score": home_score, "away_score": away_score,
        })

        # Only fetch box scores if flag is set
        if fetch_boxes and game_id and game_id not in existing_game_ids:
            time.sleep(0.3)
            box_data = fetch_box_score(game_id)
            stats = parse_box_score(box_data, game_id, home_team, away_team,
                                    winner, loser, str(target_date))
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
    parser.add_argument("--box-scores", action="store_true",
                        help="Also fetch box scores (slower)")
    args = parser.parse_args()

    existing_games = load_json(GAMES_FILE, [])
    known_confs    = load_json(CONF_FILE, {})
    existing_stats = load_json(STATS_FILE, [])
    existing_game_ids = {s["game_id"] for s in existing_stats}

    new_games = []
    new_stats = []

    if args.full_season:
        dates = all_dates_this_season()
        print(f"Scraping full season: {len(dates)} dates {'(+ box scores)' if args.box_scores else '(fast mode)'}...")
        for i, d in enumerate(dates):
            print(f"  [{i+1}/{len(dates)}] {d}...", end=" ", flush=True)
            days_games, known_confs, days_stats = scrape_date(
                d, known_confs, existing_game_ids, fetch_boxes=args.box_scores)
            print(f"{len(days_games)} games")
            new_games.extend(days_games)
            new_stats.extend(days_stats)
            existing_game_ids.update(s["game_id"] for s in days_stats)
            time.sleep(0.5)

    elif args.date:
        target = date.fromisoformat(args.date)
        print(f"Scraping {target}...")
        new_games, known_confs, new_stats = scrape_date(
            target, known_confs, existing_game_ids, fetch_boxes=args.box_scores)
        print(f"  Found {len(new_games)} games")

    else:
        today = date.today()
        print(f"Scraping today ({today})...")
        new_games, known_confs, new_stats = scrape_date(
            today, known_confs, existing_game_ids, fetch_boxes=args.box_scores)
        print(f"  Found {len(new_games)} games")

    all_games = deduplicate_games(existing_games + new_games)
    all_stats = deduplicate_stats(existing_stats + new_stats)

    save_json(GAMES_FILE, all_games)
    save_json(CONF_FILE, known_confs)
    save_json(STATS_FILE, all_stats)

    print(f"\nDone! {len(all_games)} games, {len(known_confs)} team conferences, {len(all_stats)} box scores")
