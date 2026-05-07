import json
import requests
from datetime import date

SUPABASE_URL = "https://fcipxtdcyxerytxfrzhf.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZjaXB4dGRjeXhlcnl0eGZyemhmIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3ODE4NzM3MSwiZXhwIjoyMDkzNzYzMzcxfQ.x9Hs11sVHdX_6WkIrD872EKPJ8eTk72M1BET12HnJj4"

def upload_rankings():
    with open("rankings.json") as f:
        data = json.load(f)

    rankings = data["rankings"]
    today = str(date.today())

    # Add today's date to each row
    for r in rankings:
        r["updated_at"] = today

    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "resolution=merge-duplicates"
    }

    # Clear old rankings first
    requests.delete(
        f"{SUPABASE_URL}/rest/v1/rankings",
        headers=headers,
        params={"rank": "gte.1"}
    )

    # Upload in batches of 100
    for i in range(0, len(rankings), 100):
        batch = rankings[i:i+100]
        r = requests.post(
            f"{SUPABASE_URL}/rest/v1/rankings",
            headers=headers,
            json=batch
        )
        print(f"Batch {i//100 + 1}: {r.status_code}")

    print(f"Done! Uploaded {len(rankings)} teams.")

if __name__ == "__main__":
    upload_rankings()