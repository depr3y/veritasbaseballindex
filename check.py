import json
from collections import Counter

games = json.load(open('games.json'))
conf = json.load(open('team_conferences.json'))

D1 = {
    'acc','america-east','american','asun','atlantic-10','big-12','big-east',
    'big-south','big-ten','big-west','caa','cusa','di-independent','horizon',
    'ivy-league','maac','mac','mvc','mountain-west','nec','ovc','patriot',
    'sec','socon','southland','summit-league','sun-belt','swac','wac','wcc'
}

tc = Counter()
for g in games:
    tc[g['winner']] += 1
    tc[g['loser']] += 1

xav = [g for g in games if 'Xavier' in (g['winner'], g['loser'])]
xw = sum(1 for g in xav if g['winner'] == 'Xavier')
xl = sum(1 for g in xav if g['loser'] == 'Xavier')
print(f'Xavier total: {xw}-{xl} ({len(xav)} games)')

print('\nXavier games vs non-D1 opponents:')
found = False
for g in xav:
    opp = g['loser'] if g['winner'] == 'Xavier' else g['winner']
    opp_conf = conf.get(opp, 'UNKNOWN')
    if opp_conf not in D1:
        result = 'W' if g['winner'] == 'Xavier' else 'L'
        print(f"  {g['date']} {result} vs {opp} (conf={opp_conf})")
        found = True
if not found:
    print('  none — Xavier played only D1 opponents')

dates = sorted(set(g['date'] for g in games))
print(f'\nDate range: {dates[0]} to {dates[-1]}, {len(dates)} days')
print(f'Total games: {len(games)}')
print(f'Teams with 10+ games: {sum(1 for c in tc.values() if c >= 10)}')
