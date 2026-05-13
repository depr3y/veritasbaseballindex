"""
Veritas Baseball Index — NCAA Stats Scraper
--------------------------------------------
Scrapes game results from stats.ncaa.org for all D1 baseball teams.
Correctly identifies home/away/neutral site games from the official source.

Usage:
    python scraper.py                  # incremental update (new games only)
    python scraper.py --full-season    # full rebuild from scratch
    python scraper.py --team UCLA      # scrape one team (for testing)
"""

import requests, json, re, time, argparse
from bs4 import BeautifulSoup
from datetime import date, datetime
from collections import defaultdict

# ── Config ──────────────────────────────────────────────────────────────────
GAMES_FILE = "games.json"
CONF_FILE  = "team_conferences.json"
TEAMS_FILE = "ncaa_team_ids.json"   # cached team list so we don't refetch every run

BASE        = "https://stats.ncaa.org"
SPORT_CODE  = "MBA"
YEAR        = "2026"
DIVISION    = "1"

HEADERS = {
    "User-Agent": "VeritasBaseballIndex/1.0 (veritasbaseball.vercel.app)",
    "Accept": "text/html,application/xhtml+xml",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://stats.ncaa.org/",
}

# ── Load / Save helpers ──────────────────────────────────────────────────────
def load_json(path, default):
    try:
        with open(path) as f:
            return json.load(f)
    except:
        return default

def save_json(path, data, indent=None):
    with open(path, "w") as f:
        json.dump(data, f, indent=indent)

# ── Fetch D1 team list ────────────────────────────────────────────────────────
def fetch_team_list():
    """Fetch all D1 baseball team IDs and names from stats.ncaa.org."""
    url = f"{BASE}/game_upload/team_codes"
    params = {"utf8": "✓", "sport_code": SPORT_CODE,
              "academic_year": YEAR, "division": DIVISION}
    try:
        r = requests.get(url, headers=HEADERS, params=params, timeout=30)
        r.raise_for_status()
    except Exception as e:
        print(f"  Error fetching team list: {e}")
        return {}

    soup = BeautifulSoup(r.text, "html.parser")
    teams = {}

    # Try table rows
    for row in soup.select("table tr"):
        cells = row.select("td")
        if len(cells) >= 2:
            team_id = cells[0].get_text(strip=True)
            team_name = cells[1].get_text(strip=True)
            if team_id.isdigit() and team_name:
                teams[team_id] = team_name

    # Also try select/option format
    if not teams:
        for opt in soup.select("select option"):
            val = opt.get("value", "")
            name = opt.get_text(strip=True)
            if val.isdigit() and name and name not in ("Select a Team", ""):
                teams[val] = name

    return teams

def fetch_team_list_alt():
    """Alternative: fetch team list from the standings/rankings page."""
    url = f"{BASE}/rankings/change_sport_year_div"
    params = {"sport_code": SPORT_CODE, "academic_year": YEAR, "division": DIVISION}
    try:
        r = requests.get(url, headers=HEADERS, params=params, timeout=30)
        r.raise_for_status()
    except Exception as e:
        print(f"  Error (alt): {e}")
        return {}

    soup = BeautifulSoup(r.text, "html.parser")
    teams = {}
    for a in soup.select("a[href*='/teams/']"):
        href = a.get("href", "")
        m = re.search(r"/teams/(\d+)", href)
        if m:
            team_id = m.group(1)
            name = a.get_text(strip=True)
            if name:
                teams[team_id] = name
    return teams

# ── Fetch schedule for one team ──────────────────────────────────────────────
def fetch_team_schedule(team_id, team_name):
    """
    Scrape a team's schedule from stats.ncaa.org.
    Returns list of game dicts with correct H/A/N location.
    """
    url = f"{BASE}/teams/{team_id}/schedule"
    try:
        r = requests.get(url, headers=HEADERS, timeout=20)
        if r.status_code == 404:
            return [], None
        r.raise_for_status()
    except Exception as e:
        print(f"    Error: {e}")
        return [], None

    soup = BeautifulSoup(r.text, "html.parser")
    games = []
    conf = None

    # Get conference from page
    for span in soup.select(".conference_name, .conf_name, span.conferenceName"):
        conf = span.get_text(strip=True)
        break
    # Fallback: check breadcrumb or header
    if not conf:
        for a in soup.select("a[href*='/conferences/']"):
            conf = a.get_text(strip=True)
            if conf and len(conf) > 2:
                break

    # Find schedule table
    table = None
    for t in soup.select("table"):
        headers = [th.get_text(strip=True).lower() for th in t.select("th")]
        if any(h in headers for h in ["opponent", "opp", "result"]):
            table = t
            break

    if not table:
        return [], conf

    # Parse column indices
    headers = [th.get_text(strip=True).lower() for th in table.select("thead th, tr:first-child th")]
    if not headers:
        headers = [td.get_text(strip=True).lower() for td in table.select("tr:first-child td")]

    def col(names):
        for name in names:
            for i, h in enumerate(headers):
                if name in h:
                    return i
        return -1

    date_col    = col(["date"])
    opp_col     = col(["opponent", "opp"])
    result_col  = col(["result", "score", "w/l"])
    site_col    = col(["site", "location", "home/away", "h/a"])

    if opp_col < 0 or result_col < 0:
        return [], conf

    for row in table.select("tbody tr, tr"):
        cells = row.select("td")
        if not cells or len(cells) <= max(opp_col, result_col):
            continue

        # Date
        game_date = ""
        if date_col >= 0 and date_col < len(cells):
            date_text = cells[date_col].get_text(strip=True)
            # Parse MM/DD/YYYY or similar
            for fmt in ["%m/%d/%Y", "%m/%d/%y", "%Y-%m-%d"]:
                try:
                    dt = datetime.strptime(date_text.split()[0], fmt)
                    game_date = dt.strftime("%Y-%m-%d")
                    break
                except:
                    pass
        if not game_date:
            continue

        # Skip future games
        if game_date > str(date.today()):
            continue

        # Opponent
        opp_cell = cells[opp_col]
        opp_text = opp_cell.get_text(strip=True)
        # Remove @ or vs from opponent name
        opp_name = re.sub(r"^[@#\s]*(at\s+|vs\.?\s*)?", "", opp_text, flags=re.IGNORECASE).strip()
        # Remove rank indicators like (5) or #5
        opp_name = re.sub(r"^[\(\)#\d]+\s*", "", opp_name).strip()
        opp_name = re.sub(r"\s*\(\d+\)\s*$", "", opp_name).strip()
        if not opp_name:
            continue

        # Result
        result_text = cells[result_col].get_text(strip=True).upper()
        if not result_text or result_text in ("", "-", "PPD", "CANC", "CANC.", "CANCEL"):
            continue
        if not (result_text.startswith("W") or result_text.startswith("L")):
            continue

        won = result_text.startswith("W")

        # Location / site
        location = "home"  # default
        if site_col >= 0 and site_col < len(cells):
            site_text = cells[site_col].get_text(strip=True).lower()
            if "neutral" in site_text or site_text in ("n", "neu"):
                location = "neutral"
            elif "away" in site_text or site_text in ("a", "@") or "@" in site_text:
                location = "away"
            elif "home" in site_text or site_text in ("h",):
                location = "home"
        else:
            # Infer from opponent text — if it has @ it's away
            if opp_text.strip().startswith("@"):
                location = "away"
            elif opp_text.strip().lower().startswith("at "):
                location = "away"

        winner = team_name if won else opp_name
        loser  = opp_name  if won else team_name

        # Generate stable game_id from teams + date
        parts = sorted([team_name, opp_name]) + [game_date]
        game_id = "_".join(parts).replace(" ", "-").replace("/", "-")

        games.append({
            "game_id":   game_id,
            "date":      game_date,
            "winner":    winner,
            "loser":     loser,
            "location":  location,
            "home_team": team_name if location == "home" else (opp_name if location == "away" else ""),
            "away_team": opp_name  if location == "home" else (team_name if location == "away" else ""),
        })

    return games, conf

# ── D1 filter ────────────────────────────────────────────────────────────────
# Known D1 team name patterns — filter out non-D1 opponents
# We only keep games where BOTH teams are in our D1 list
def filter_d1_games(all_games, d1_names):
    """Keep only games where both winner and loser are D1 teams."""
    filtered = []
    for g in all_games:
        if g["winner"] in d1_names and g["loser"] in d1_names:
            filtered.append(g)
    return filtered

# ── Deduplication ────────────────────────────────────────────────────────────
def dedup_games(games):
    """Deduplicate by game_id, keeping one record per game."""
    seen = {}
    for g in games:
        gid = g.get("game_id", "")
        if gid and gid not in seen:
            seen[gid] = g
        elif not gid:
            # Fallback key
            key = f"{sorted([g['winner'],g['loser']])}_{g['date']}"
            if key not in seen:
                seen[key] = g
    return list(seen.values())

# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--full-season", action="store_true",
                        help="Full rebuild — ignore existing games.json")
    parser.add_argument("--team", help="Scrape a single team by name (for testing)")
    args = parser.parse_args()

    # Load existing data
    existing_games = [] if args.full_season else load_json(GAMES_FILE, [])
    known_confs    = load_json(CONF_FILE, {})
    existing_ids   = {g.get("game_id","") for g in existing_games}

    # Load or fetch team list
    team_ids = load_json(TEAMS_FILE, {})
    if not team_ids or args.full_season:
        print("Fetching D1 team list from stats.ncaa.org...")
        team_ids = fetch_team_list()
        if not team_ids:
            print("  Primary method failed, trying alternative...")
            team_ids = fetch_team_list_alt()
        if not team_ids:
            print("  ERROR: Could not fetch team list")
            exit(1)
        save_json(TEAMS_FILE, team_ids)
        print(f"  Found {len(team_ids)} teams")

    d1_names = set(team_ids.values())

    # Filter to one team if --team flag
    if args.team:
        team_ids = {k: v for k, v in team_ids.items() if args.team.lower() in v.lower()}
        if not team_ids:
            print(f"Team '{args.team}' not found")
            exit(1)
        print(f"Testing with: {list(team_ids.values())}")

    all_new_games = []
    teams_list = list(team_ids.items())
    total = len(teams_list)

    print(f"\nScraping {total} teams...")
    for i, (team_id, team_name) in enumerate(teams_list):
        print(f"  [{i+1:3d}/{total}] {team_name:<30}", end=" ", flush=True)

        games, conf = fetch_team_schedule(team_id, team_name)

        # Save conference
        if conf and team_name not in known_confs:
            known_confs[team_name] = conf

        # Filter new games
        new = [g for g in games if g.get("game_id","") not in existing_ids]
        all_new_games.extend(new)
        existing_ids.update(g.get("game_id","") for g in new)

        print(f"{len(games)} games ({len(new)} new)", flush=True)
        time.sleep(0.4)  # polite rate limit

    print(f"\nTotal new games found: {len(all_new_games)}")

    # Combine and deduplicate
    combined = existing_games + all_new_games
    combined = filter_d1_games(combined, d1_names)
    combined = dedup_games(combined)
    combined.sort(key=lambda g: g["date"])

    # Save
    save_json(GAMES_FILE, combined)
    save_json(CONF_FILE, known_confs)

    # Stats
    from collections import Counter
    locs = Counter(g["location"] for g in combined)
    print(f"\nSaved {len(combined)} games to {GAMES_FILE}")
    print(f"Location breakdown: {dict(locs)}")
    print(f"Conferences: {len(known_confs)} teams mapped")

    dates = sorted(set(g["date"] for g in combined))
    if dates:
        print(f"Date range: {dates[0]} to {dates[-1]}")
