import requests, re

URL = "http://www.boydsworld.com/baseball/rpi/currentrpi.html"
HEADERS = {"User-Agent": "VeritasBaseballIndex/1.0", "Accept-Encoding": "identity"}

session = requests.Session()
r = session.get(URL, headers=HEADERS, timeout=30, stream=True)
content = b""
for chunk in r.iter_content(chunk_size=4096):
    content += chunk
text = content.decode('utf-8', errors='replace')

print(f"Page size: {len(text)} bytes")

teams = []
for line in text.split('\n'):
    m = re.match(r'^\s+(\d+)\s+([\d.]+)\s+\d+\s+\d+\s+[\d.]+\s+[\d.]+\s+\d+\s+\d+\s+(.+)$', line)
    if m:
        raw = re.sub(r'<.*', '', m.group(3)).strip()
        if raw:
            teams.append((int(m.group(1)), raw))

print(f"Total teams found: {len(teams)}")
for rank, name in teams:
    print(f'    "{name}": "",')
