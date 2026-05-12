"""
Veritas Baseball Index — RPI Scraper
Scrapes RPI from WarrenNolan.com and auto-matches to VBI team names.
"""
import requests, json, re
from datetime import datetime, timezone, timedelta

URL = "https://www.warrennolan.com/baseball/2026/compare-rankings"
OUTPUT = "rpi.json"
GAMES_FILE = "games.json"
HEADERS = {"User-Agent": "VeritasBaseballIndex/1.0 (college baseball rating project)"}

def normalize(name):
    """Normalize a team name for fuzzy matching."""
    name = name.lower().strip()
    # Remove common suffixes/prefixes that differ between sources
    for pat in [r'\bst\.?\b', r'\bstate\b', r'\buniversity\b', r'\bcollege\b',
                r'\(.*?\)', r'&', r'-', r"'", r'\.']:
        name = re.sub(pat, ' ', name)
    return re.sub(r'\s+', ' ', name).strip()

def best_match(raw_name, vbi_names):
    """Find the best matching VBI team name for a Warren Nolan name."""
    norm_raw = normalize(raw_name)
    # Exact normalized match
    for vbi in vbi_names:
        if normalize(vbi) == norm_raw:
            return vbi
    # One contains the other
    for vbi in vbi_names:
        nv = normalize(vbi)
        if norm_raw in nv or nv in norm_raw:
            return vbi
    # Word overlap score
    raw_words = set(norm_raw.split())
    best, best_score = None, 0
    for vbi in vbi_names:
        vbi_words = set(normalize(vbi).split())
        if not vbi_words: continue
        overlap = len(raw_words & vbi_words)
        score = overlap / max(len(raw_words), len(vbi_words))
        if score > best_score and score >= 0.6:
            best_score = score
            best = vbi
    return best

def load_vbi_names():
    try:
        games = json.load(open(GAMES_FILE))
        from collections import Counter
        tc = Counter()
        for g in games:
            tc[g['winner']] += 1
            tc[g['loser']] += 1
        return set(t for t, c in tc.items() if c >= 10)
    except:
        return set()

def scrape_rpi():
    try:
        r = requests.get(URL, headers=HEADERS, timeout=20)
        r.raise_for_status()
    except requests.RequestException as e:
        print(f"Error: {e}")
        return None

    html = r.text
    vbi_names = load_vbi_names()
    rankings = {}
    unmatched = []

    rows = re.findall(r'<tr>(.*?)</tr>', html, re.DOTALL)
    for row in rows:
        cells = re.findall(r'<td[^>]*>(.*?)</td>', row, re.DOTALL)
        if len(cells) < 4: continue
        team_match = re.search(r'>([^<]+)</a>', cells[0])
        if not team_match:
            team_match = re.search(r'>([^<]+)<', cells[0])
        if not team_match: continue
        raw_name = team_match.group(1).strip()
        if not raw_name or raw_name in ('Team', 'Record'): continue

        def clean(cell):
            text = re.sub(r'<[^>]+>', '', cell).strip()
            return int(text) if text.isdigit() else None

        rpi_rank = clean(cells[3]) if len(cells) > 3 else None
        if rpi_rank is None: continue

        vbi_name = best_match(raw_name, vbi_names) if vbi_names else raw_name
        if vbi_name:
            rankings[vbi_name] = {"rpi_rank": rpi_rank, "raw_name": raw_name}
        else:
            unmatched.append(raw_name)

    if unmatched:
        print(f"  Unmatched ({len(unmatched)}): {unmatched[:10]}")
    return rankings

if __name__ == "__main__":
    print("Scraping RPI from WarrenNolan.com...")
    rankings = scrape_rpi()
    if not rankings:
        print("Failed"); exit(1)

    EST = timezone(timedelta(hours=-4))
    today = datetime.now(EST).strftime('%Y-%m-%d')
    output = {"updated": today, "source": "warrennolan.com", "teams": rankings}
    with open(OUTPUT, "w") as f:
        json.dump(output, f, indent=2)

    print(f"Done! Matched {len(rankings)} teams.")
    print("\nTop 10 by RPI:")
    top10 = sorted(rankings.items(), key=lambda x: x[1]['rpi_rank'])[:10]
    for team, data in top10:
        print(f"  RPI #{data['rpi_rank']:3d}  {team}  (raw: {data['raw_name']})")
