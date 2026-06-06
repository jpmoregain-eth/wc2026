"""
WC 2026 Squad Scraper + Score Calculator
Runs in GitHub Actions:
1. Scrapes all 48 squads from Wikipedia
2. Matches players to Supabase stats DB
3. Recomputes team strength scores
4. Writes prediction_data.json and squads.json
"""

import os
import json
import re
import time
import requests
from bs4 import BeautifulSoup
from supabase import create_client

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_SERVICE_KEY"]

NATION_CODES = {
    "Mexico":"MEX","South Africa":"RSA","Korea Republic":"KOR","South Korea":"KOR",
    "Czechia":"CZE","Czech Republic":"CZE","Canada":"CAN","Bosnia and Herzegovina":"BIH",
    "Bosnia & Herzegovina":"BIH","Qatar":"QAT","Switzerland":"SUI","Brazil":"BRA",
    "Morocco":"MAR","Haiti":"HAI","Scotland":"SCO","United States":"USA","USA":"USA",
    "Paraguay":"PAR","Australia":"AUS","Turkey":"TUR","Türkiye":"TUR","Germany":"GER",
    "Curaçao":"CUW","Côte d'Ivoire":"CIV","Ivory Coast":"CIV","Ecuador":"ECU",
    "Netherlands":"NED","Japan":"JPN","Sweden":"SWE","Tunisia":"TUN","Belgium":"BEL",
    "Egypt":"EGY","IR Iran":"IRN","Iran":"IRN","New Zealand":"NZL","Spain":"ESP",
    "Cabo Verde":"CPV","Cape Verde":"CPV","Saudi Arabia":"KSA","Uruguay":"URU",
    "France":"FRA","Senegal":"SEN","Iraq":"IRQ","Norway":"NOR","Argentina":"ARG",
    "Algeria":"ALG","Austria":"AUT","Jordan":"JOR","Portugal":"POR",
    "DR Congo":"COD","Congo DR":"COD","Uzbekistan":"UZB","Colombia":"COL",
    "England":"ENG","Croatia":"CRO","Ghana":"GHA","Panama":"PAN",
}

GROUPS = {
    "A":["Mexico","South Africa","South Korea","Czechia"],
    "B":["Canada","Bosnia & Herzegovina","Qatar","Switzerland"],
    "C":["Brazil","Morocco","Haiti","Scotland"],
    "D":["USA","Paraguay","Australia","Turkey"],
    "E":["Germany","Curaçao","Ivory Coast","Ecuador"],
    "F":["Netherlands","Japan","Sweden","Tunisia"],
    "G":["Belgium","Egypt","Iran","New Zealand"],
    "H":["Spain","Cape Verde","Saudi Arabia","Uruguay"],
    "I":["France","Senegal","Iraq","Norway"],
    "J":["Argentina","Algeria","Austria","Jordan"],
    "K":["Portugal","DR Congo","Uzbekistan","Colombia"],
    "L":["England","Croatia","Ghana","Panama"],
}

TEAM_TO_CODE = {v:k for k,v in {
    "Mexico":"MEX","South Africa":"RSA","South Korea":"KOR","Czechia":"CZE",
    "Canada":"CAN","Bosnia & Herzegovina":"BIH","Qatar":"QAT","Switzerland":"SUI",
    "Brazil":"BRA","Morocco":"MAR","Haiti":"HAI","Scotland":"SCO","USA":"USA",
    "Paraguay":"PAR","Australia":"AUS","Turkey":"TUR","Germany":"GER",
    "Curaçao":"CUW","Ivory Coast":"CIV","Ecuador":"ECU","Netherlands":"NED",
    "Japan":"JPN","Sweden":"SWE","Tunisia":"TUN","Belgium":"BEL","Egypt":"EGY",
    "Iran":"IRN","New Zealand":"NZL","Spain":"ESP","Cape Verde":"CPV",
    "Saudi Arabia":"KSA","Uruguay":"URU","France":"FRA","Senegal":"SEN",
    "Iraq":"IRQ","Norway":"NOR","Argentina":"ARG","Algeria":"ALG","Austria":"AUT",
    "Jordan":"JOR","Portugal":"POR","DR Congo":"COD","Uzbekistan":"UZB",
    "Colombia":"COL","England":"ENG","Croatia":"CRO","Ghana":"GHA","Panama":"PAN",
}.items()}

def normalize(name):
    name = name.lower().strip()
    replacements = {
        'á':'a','à':'a','ã':'a','â':'a','ä':'a','é':'e','è':'e','ê':'e','ë':'e',
        'í':'i','ì':'i','î':'i','ï':'i','ó':'o','ò':'o','õ':'o','ô':'o','ö':'o',
        'ú':'u','ù':'u','û':'u','ü':'u','ý':'y','ÿ':'y','ñ':'n','ç':'c','ß':'ss',
        'ø':'o','å':'a','æ':'ae','œ':'oe','š':'s','č':'c','ž':'z','ř':'r','ě':'e',
        'ğ':'g','ı':'i','ł':'l','ń':'n','ś':'s','ț':'t','ș':'s','ă':'a','â':'a',
    }
    for k,v in replacements.items():
        name = name.replace(k, v)
    name = re.sub(r"[^a-z ]","",name)
    return name.strip()

def scrape_wikipedia_squads():
    print("Scraping Wikipedia squads...")
    url = "https://en.wikipedia.org/wiki/2026_FIFA_World_Cup_squads"
    resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
    soup = BeautifulSoup(resp.text, "html.parser")

    squads = {}
    current_team = None

    # Find all h3 headings (team names) and tables
    for elem in soup.find_all(["h2","h3","table"]):
        if elem.name in ["h2","h3"]:
            text = elem.get_text(strip=True).replace("[edit]","").strip()
            # Match to a known team
            for team, code in NATION_CODES.items():
                if team.lower() in text.lower():
                    current_team = text
                    if code not in squads:
                        squads[code] = []
                    break

        elif elem.name == "table" and current_team:
            code = None
            for team, c in NATION_CODES.items():
                if team.lower() in current_team.lower():
                    code = c
                    break
            if not code:
                continue

            rows = elem.find_all("tr")
            for row in rows:
                cells = row.find_all(["td","th"])
                if len(cells) < 3:
                    continue
                texts = [c.get_text(strip=True) for c in cells]
                # Look for position indicator
                pos_indicators = {"GK","DF","MF","FW"}
                pos = None
                name = None
                for i, t in enumerate(texts):
                    if t in pos_indicators:
                        pos = t
                        # Name is usually next cell
                        if i+1 < len(texts):
                            name = texts[i+1]
                        break

                if name and pos:
                    # Clean name - remove extra info in brackets
                    name = re.sub(r'\(.*?\)', '', name).strip()
                    name = re.sub(r'\[.*?\]', '', name).strip()
                    if name and len(name) > 2:
                        squads[code].append({
                            "name": name,
                            "name_norm": normalize(name),
                            "position": pos,
                        })

    # Deduplicate within each team
    for code in squads:
        seen = set()
        unique = []
        for p in squads[code]:
            if p["name_norm"] not in seen:
                seen.add(p["name_norm"])
                unique.append(p)
        squads[code] = unique

    total = sum(len(v) for v in squads.values())
    print(f"Scraped {len(squads)} teams, {total} players total")
    return squads

def fetch_supabase_players(supabase):
    print("Fetching Supabase player stats...")
    all_players = []
    offset = 0
    while True:
        res = supabase.table("wc2026_players") \
            .select("id,player,nation,minutes,goals,assists,xg,xa,shots,shots_on_target,position") \
            .range(offset, offset+999).execute()
        if not res.data: break
        all_players.extend(res.data)
        offset += 1000
        if len(res.data) < 1000: break
    print(f"Fetched {len(all_players)} players from Supabase")
    return all_players

def match_squad_to_stats(squads, db_players):
    """Match confirmed squad players to their stats in our DB."""
    # Build lookup by normalized name + nation
    db_lookup = {}
    for p in db_players:
        if p.get("player") and p.get("nation"):
            key = (normalize(p["player"]), p["nation"])
            db_lookup[key] = p

    matched_stats = {}  # nation_code -> list of player stats

    for code, players in squads.items():
        matched_stats[code] = []
        matched = 0
        for p in players:
            key = (p["name_norm"], code)
            if key in db_lookup:
                stats = db_lookup[key].copy()
                stats["position_squad"] = p["position"]
                matched_stats[code].append(stats)
                matched += 1
            else:
                # Try without nation (some players coded differently)
                found = None
                for (norm_name, nation), stats in db_lookup.items():
                    if norm_name == p["name_norm"]:
                        found = stats.copy()
                        found["position_squad"] = p["position"]
                        break
                if found:
                    matched_stats[code].append(found)
                    matched += 1
                else:
                    # Add with zero stats (player exists in squad but not in our DB)
                    matched_stats[code].append({
                        "player": p["name"],
                        "nation": code,
                        "position_squad": p["position"],
                        "minutes": 0, "goals": 0, "assists": 0,
                        "xg": None, "xa": None,
                        "shots": None, "shots_on_target": None,
                    })

        print(f"  {code}: {matched}/{len(players)} matched")

    return matched_stats

def compute_scores(matched_stats):
    scores = {}

    for code, players in matched_stats.items():
        # Find team name
        team_name = None
        for name, c in TEAM_TO_CODE.items():
            if c == code:
                team_name = name
                break
        if not team_name:
            team_name = code

        active = [p for p in players if (p.get("minutes") or 0) >= 200]
        if not active:
            active = [p for p in players if (p.get("minutes") or 0) > 0]
        if not active:
            active = players

        if not active:
            scores[team_name] = {"score": 25, "attack": 0, "creativity": 0, "players_matched": 0}
            continue

        def per90(stat, player):
            mins = max(player.get("minutes") or 1, 1)
            val = player.get(stat) or 0
            return (val / mins) * 90

        # Top attackers by xG
        by_xg = sorted(active, key=lambda p: (p.get("xg") or 0), reverse=True)
        top_att = by_xg[:6]  # top 6 by xG
        top_mid = sorted(active, key=lambda p: (p.get("xa") or 0), reverse=True)[:5]

        attack     = sum(per90("xg", p) for p in top_att)
        creativity = sum(per90("xa", p) for p in top_mid)
        finishing  = sum(per90("goals", p) for p in top_att)

        raw = (attack * 0.5) + (creativity * 0.3) + (finishing * 0.2)

        scores[team_name] = {
            "raw": round(raw, 4),
            "attack": round(attack, 2),
            "creativity": round(creativity, 2),
            "finishing": round(finishing, 2),
            "players_matched": len([p for p in players if (p.get("minutes") or 0) > 0]),
            "squad_size": len(players),
        }

    # Normalize to 0-100
    raws = [v["raw"] for v in scores.values() if v.get("raw", 0) > 0]
    if raws:
        min_r, max_r = min(raws), max(raws)
        for team in scores:
            raw = scores[team].get("raw", 0)
            if max_r > min_r:
                scores[team]["score"] = round(20 + ((raw - min_r) / (max_r - min_r)) * 75, 1)
            else:
                scores[team]["score"] = 50

    return scores

def simulate_group(teams, scores):
    standings = {t: {"pts":0,"gf":0,"ga":0} for t in teams}
    matchups = [(teams[i],teams[j]) for i in range(len(teams)) for j in range(i+1,len(teams))]

    for home, away in matchups:
        hs = scores.get(home, {}).get("score", 40)
        as_ = scores.get(away, {}).get("score", 40)
        diff = abs(hs - as_)

        if diff < 8:
            standings[home]["pts"] += 1
            standings[away]["pts"] += 1
        elif hs > as_:
            standings[home]["pts"] += 3
            standings[home]["gf"] += 1
            standings[away]["ga"] += 1
        else:
            standings[away]["pts"] += 3
            standings[away]["gf"] += 1
            standings[home]["ga"] += 1

    return sorted(teams, key=lambda t: (
        standings[t]["pts"],
        standings[t]["gf"] - standings[t]["ga"],
        scores.get(t,{}).get("score",0)
    ), reverse=True), standings

def simulate_knockout(t1, t2, scores):
    s1 = scores.get(t1,{}).get("score",40)
    s2 = scores.get(t2,{}).get("score",40)
    return t1 if s1 >= s2 else t2

def build_predictions(scores):
    # Group stage
    group_results = {}
    for letter, teams in GROUPS.items():
        sorted_teams, standings = simulate_group(teams, scores)
        group_results[letter] = [
            {"team": t, "pts": standings[t]["pts"],
             "gf": standings[t]["gf"], "ga": standings[t]["ga"],
             "score": round(scores.get(t,{}).get("score",0),1)}
            for t in sorted_teams
        ]

    # Best third place
    third_place = [group_results[l][2] for l in group_results]
    third_place.sort(key=lambda x: (x["pts"], x["gf"]-x["ga"], x["score"]), reverse=True)
    best_third = [t["team"] for t in third_place[:8]]

    advancers = {f"{l}1": group_results[l][0]["team"] for l in group_results}
    advancers.update({f"{l}2": group_results[l][1]["team"] for l in group_results})

    r32_pairs = [
        (advancers["A1"],advancers["B2"]),(advancers["C1"],advancers["D2"]),
        (advancers["E1"],advancers["F2"]),(advancers["G1"],advancers["H2"]),
        (advancers["I1"],advancers["J2"]),(advancers["K1"],advancers["L2"]),
        (advancers["B1"],advancers["A2"]),(advancers["D1"],advancers["C2"]),
        (advancers["F1"],advancers["E2"]),(advancers["H1"],advancers["G2"]),
        (advancers["J1"],advancers["I2"]),(advancers["L1"],advancers["K2"]),
        (best_third[0],best_third[1]),(best_third[2],best_third[3]),
        (best_third[4],best_third[5]),(best_third[6],best_third[7]),
    ]

    def sim_round(pairs):
        return [simulate_knockout(a,b,scores) for a,b in pairs]

    r32w = sim_round(r32_pairs)
    r16_pairs = list(zip(r32w[::2], r32w[1::2]))
    r16w = sim_round(r16_pairs)
    qf_pairs = list(zip(r16w[::2], r16w[1::2]))
    qfw = sim_round(qf_pairs)
    sf_pairs = list(zip(qfw[::2], qfw[1::2]))
    sfw = sim_round(sf_pairs)
    sfl = [qfw[i*2+(0 if sfw[i]==qfw[i*2+1] else 1)] for i in range(2)]
    champion = simulate_knockout(sfw[0], sfw[1], scores)
    third = simulate_knockout(sfl[0], sfl[1], scores)

    return {
        "generated_at": __import__("datetime").datetime.utcnow().isoformat() + "Z",
        "scores": {k: {
            "score": v["score"],
            "attack": v.get("attack",0),
            "creativity": v.get("creativity",0),
            "players_matched": v.get("players_matched",0),
        } for k,v in scores.items()},
        "groups": group_results,
        "bracket": {
            "r32":   [{"home":a,"away":b,"winner":w} for (a,b),w in zip(r32_pairs,r32w)],
            "r16":   [{"home":a,"away":b,"winner":w} for (a,b),w in zip(r16_pairs,r16w)],
            "qf":    [{"home":a,"away":b,"winner":w} for (a,b),w in zip(qf_pairs,qfw)],
            "sf":    [{"home":a,"away":b,"winner":w} for (a,b),w in zip(sf_pairs,sfw)],
            "final": {"home":sfw[0],"away":sfw[1],"winner":champion},
            "third": {"home":sfl[0],"away":sfl[1],"winner":third},
        }
    }

def main():
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

    # 1. Scrape squads
    squads = scrape_wikipedia_squads()

    # 2. Fetch DB stats
    db_players = fetch_supabase_players(supabase)

    # 3. Match
    matched = match_squad_to_stats(squads, db_players)

    # 4. Compute scores
    scores = compute_scores(matched)

    # 5. Build predictions
    predictions = build_predictions(scores)

    champion = predictions["bracket"]["final"]["winner"]
    print(f"\n=== PREDICTED CHAMPION: {champion} ===")

    top5 = sorted(scores.items(), key=lambda x: x[1].get("score",0), reverse=True)[:5]
    for i,(t,s) in enumerate(top5,1):
        print(f"  {i}. {t}: {s['score']} ({s.get('players_matched',0)} players matched)")

    # 6. Mark confirmed squad players in Supabase
    print("\nMarking confirmed squad players in Supabase...")

    # First reset all to false
    supabase.table("wc2026_players").update({"in_squad": False}).neq("id", 0).execute()
    print("  Reset all in_squad to false")

    # Build set of confirmed player norm names + nation codes
    confirmed = set()
    for code, players in squads.items():
        for p in players:
            confirmed.add((p["name_norm"], code))

    # Fetch all players from DB
    all_db = []
    offset = 0
    while True:
        res = supabase.table("wc2026_players").select("id,player,nation").range(offset, offset+999).execute()
        if not res.data: break
        all_db.extend(res.data)
        offset += 1000
        if len(res.data) < 1000: break

    # Mark matches
    to_mark = []
    for p in all_db:
        if not p.get("player") or not p.get("nation"):
            continue
        norm = normalize(p["player"])
        if (norm, p["nation"]) in confirmed:
            to_mark.append(p["id"])

    # Also try name-only match for players whose nation code differs
    marked_ids = set(to_mark)
    confirmed_names = {n for (n, _) in confirmed}
    for p in all_db:
        if p["id"] in marked_ids:
            continue
        if p.get("player") and normalize(p["player"]) in confirmed_names:
            to_mark.append(p["id"])
            marked_ids.add(p["id"])

    print(f"  Marking {len(to_mark)} players as in_squad=true")

    # Update in batches
    for i in range(0, len(to_mark), 200):
        batch_ids = to_mark[i:i+200]
        for pid in batch_ids:
            supabase.table("wc2026_players").update({"in_squad": True}).eq("id", pid).execute()

    print(f"  Done marking squad players")

    # 7. Write output files
    os.makedirs("src/data", exist_ok=True)

    with open("src/data/prediction_data.json","w") as f:
        json.dump(predictions, f, indent=2)
    print("\nWrote src/data/prediction_data.json")

    # Write squads (for future use in lineup display)
    squads_out = {}
    for code, players in squads.items():
        squads_out[code] = [{"name": p["name"], "position": p["position"]} for p in players]

    with open("src/data/squads.json","w") as f:
        json.dump(squads_out, f, indent=2)
    print("Wrote src/data/squads.json")

if __name__ == "__main__":
    main()
