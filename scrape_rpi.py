"""
Veritas Baseball Index — RPI Scraper
--------------------------------------
Scrapes RPI (and ELO) rankings from WarrenNolan.com/compare-rankings.
Saves to rpi.json for use in the VBI rankings comparison.

Usage:
    python scrape_rpi.py
"""

import requests
import json
import re
from datetime import datetime, timezone, timedelta

URL = "https://www.warrennolan.com/baseball/2026/compare-rankings"
OUTPUT = "rpi.json"

HEADERS = {
    "User-Agent": "VeritasBaseballIndex/1.0 (college baseball rating project)"
}

NAME_MAP = {
    "UCLA": "UCLA", "Texas": "Texas", "Mississippi State": "Mississippi St.",
    "North Carolina": "North Carolina", "Georgia Tech": "Georgia Tech",
    "Auburn": "Auburn", "Alabama": "Alabama", "Florida State": "Florida State",
    "Southern Miss": "Southern Miss", "USC": "Southern California",
    "Texas A&M": "Texas A&M", "Florida": "Florida", "Ole Miss": "Ole Miss",
    "Georgia": "Georgia", "Nebraska": "Nebraska", "Wake Forest": "Wake Forest",
    "West Virginia": "West Virginia", "Oregon State": "Oregon St.",
    "Oregon": "Oregon", "Cincinnati": "Cincinnati", "Oklahoma": "Oklahoma",
    "Kansas": "Kansas", "Virginia": "Virginia", "Oklahoma State": "Oklahoma St.",
    "Missouri State": "Missouri St.", "Coastal Carolina": "Coastal Carolina",
    "Arkansas": "Arkansas", "UC Santa Barbara": "UC Santa Barbara",
    "Boston College": "Boston College", "Kentucky": "Kentucky",
    "Jacksonville State": "Jacksonville St.", "UCF": "UCF",
    "Tennessee": "Tennessee", "Miami": "Miami", "Michigan": "Michigan",
    "Liberty": "Liberty", "Mercer": "Mercer", "Clemson": "Clemson",
    "Virginia Tech": "Virginia Tech", "TCU": "TCU", "High Point": "High Point",
    "Texas State": "Texas State", "NC State": "NC State",
    "Miami (OH)": "Miami (OH)", "Arizona State": "Arizona St.",
    "Gonzaga": "Gonzaga", "UTSA": "UTSA", "Louisiana": "Louisiana",
    "Pittsburgh": "Pittsburgh", "SE Missouri State": "Southeast Missouri",
    "Purdue": "Purdue", "Western Carolina": "Western Carolina",
    "Kent State": "Kent St.", "Troy": "Troy", "East Carolina": "East Carolina",
    "California": "California", "LSU": "LSU", "South Alabama": "South Alabama",
    "Arkansas State": "Arkansas St.", "Kansas State": "Kansas St.",
    "UAB": "UAB", "Vanderbilt": "Vanderbilt", "Duke": "Duke",
    "Notre Dame": "Notre Dame", "Stanford": "Stanford", "Rice": "Rice",
    "Louisville": "Louisville", "Maryland": "Maryland", "Penn State": "Penn St.",
    "Minnesota": "Minnesota", "Michigan State": "Michigan St.",
    "Ohio State": "Ohio St.", "Illinois": "Illinois", "Iowa": "Iowa",
    "Xavier": "Xavier", "UConn": "UConn", "Seton Hall": "Seton Hall",
    "Georgetown": "Georgetown", "St. John's": "St. John's (NY)",
    "Villanova": "Villanova", "Dallas Baptist": "Dallas Baptist",
    "Sam Houston": "Sam Houston", "Kennesaw State": "Kennesaw St.",
    "Indiana": "Indiana", "Wichita State": "Wichita St.",
    "Tarleton State": "Tarleton St.",
}

def normalize(name):
    name = name.strip()
    return NAME_MAP.get(name, name)

def scrape_rpi():
    try:
        r = requests.get(URL, headers=HEADERS, timeout=20)
        r.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching rankings: {e}")
        return None

    html = r.text
    rankings = {}
    rows = re.findall(r'<tr>(.*?)</tr>', html, re.DOTALL)

    for row in rows:
        cells = re.findall(r'<td[^>]*>(.*?)</td>', row, re.DOTALL)
        if len(cells) < 4:
            continue
        team_cell = cells[0]
        team_match = re.search(r'>([^<]+)</a>', team_cell)
        if not team_match:
            team_match = re.search(r'>([^<]+)<', team_cell)
        if not team_match:
            continue
        raw_name = team_match.group(1).strip()
        if not raw_name or raw_name in ('Team', 'Record'):
            continue

        def clean(cell):
            text = re.sub(r'<[^>]+>', '', cell).strip()
            return int(text) if text.isdigit() else None

        elo_rank = clean(cells[2]) if len(cells) > 2 else None
        rpi_rank = clean(cells[3]) if len(cells) > 3 else None
        if rpi_rank is None:
            continue

        vbi_name = normalize(raw_name)
        rankings[vbi_name] = {
            "rpi_rank": rpi_rank,
            "elo_rank": elo_rank,
            "raw_name": raw_name
        }

    return rankings

if __name__ == "__main__":
    print("Scraping RPI + ELO from WarrenNolan.com...")
    rankings = scrape_rpi()
    if not rankings:
        print("Failed to scrape data")
        exit(1)

    EST = timezone(timedelta(hours=-4))
    today = datetime.now(EST).strftime('%Y-%m-%d')
    output = {"updated": today, "source": "warrennolan.com", "teams": rankings}

    with open(OUTPUT, "w") as f:
        json.dump(output, f, indent=2)

    print(f"Done! Saved {len(rankings)} teams to {OUTPUT}")
    print(f"\nTop 10 by RPI:")
    top10 = sorted(rankings.items(), key=lambda x: x[1]['rpi_rank'])[:10]
    for team, data in top10:
        print(f"  RPI #{data['rpi_rank']}  ELO #{data['elo_rank']}  {team}")
