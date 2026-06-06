"""
WC 2026 Squad Scraper + Score Calculator v2
Uses bulk SQL update for in_squad marking (much faster)
"""

import os
import json
import re
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

TEAM_TO_CODE = {
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
}

CODE_TO_TEAM = {v:k for k,v in TEAM_TO_CODE.items()}

def normalize(name):
    name = name.lower().strip()
    replacements = {
        'á':'a','à':'a','ã':'a','â':'a','ä':'a','é':'e','è':'e','ê':'e','ë':'e',
        'í':'i','ì':'i','î':'i','ï':'i','ó':'o','ò':'o','õ':'o','ô':'o','ö':'o',
        'ú':'u','ù':'u','û':'u','ü':'u','ý':'y','ÿ':'y','ñ':'n','ç':'c','ß':'ss',
        'ø':'o','å':'a','æ':'ae','œ':'oe','š':'s','č':'c','ž':'z','ř':'r','ě':'e',
        'ğ':'g','ı':'i','ł':'l','ń':'n','ś':'s','ț':'t','ș':'s','ă':'a',
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
    current_code = None

    for elem in soup.find_all(["h2","h3","table"]):
        if elem.name in ["h2","h3"]:
            text = elem.get_text(strip=True).replace("[edit]","").strip()
            for team, code in NATION_CODES.items():
                if team.lower() in text.lower():
                    current_code = code
                    if code not in squads:
                        squads[code] = []
                    break

        elif elem.name == "table" and current_code:
            rows = elem.find_all("tr")
            for row in rows:
                cells = row.find_all(["td","th"])
                if len(cells) < 3:
                    continue
                texts = [c.get_text(strip=True) for c in cells]
                pos_indicators = {"GK","DF","MF","FW"}
                pos = None
                name = None
                for i, t in enumerate(texts):
                    if t in pos_indicators:
                        pos = t
                        if i+1 < len(texts):
                            name = texts[i+1]
                        break
                if name and pos:
                    name = re.sub(r'\(.*?\)', '', name).strip()
                    name = re.sub(r'\[.*?\]', '', name).strip()
                    if name and len(name) > 2:
                        squads[current_code].append({
                            "name": name,
                            "name_norm": normalize(name),
                            "position": pos,
                        })

    # Deduplicate
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
    print("Fetching Supabase players...")
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
    print(f"Fetched {len(all_players)} players")
    return all_players

def mark_squad_players(supabase, squads, db_players):
    """Mark confirmed squad players using bulk update by id list."""
    print("\nMarking squad players...")

    # Build normalized name lookup from DB
    db_lookup = {}
    for p in db_players:
        if p.get("player") and p.get("nation"):
            key = (normalize(p["player"]), p["nation"])
            db_lookup[key] = p["id"]

    # Also build name-only lookup as fallback
    name_lookup = {}
    for p in db_players:
        if p.get("player"):
            norm = normalize(p["player"])
            if norm not in name_lookup:
                name_lookup[norm] = p["id"]

    # Find IDs to mark
    ids_to_mark = set()
    for code, players in squads.items():
        matched = 0
        for p in players:
            # Try exact match first
            key = (p["name_norm"], code)
            if key in db_lookup:
                ids_to_mark.add(db_lookup[key])
                matched += 1
            # Fallback: name only
            elif p["name_norm"] in name_lookup:
                ids_to_mark.add(name_lookup[p["name_norm"]])
                matched += 1
        print(f"  {code}: {matched}/{len(players)} matched")

    print(f"\nTotal to mark: {len(ids_to_mark)}")

    # Reset all to false first
    supabase.table("wc2026_players").update({"in_squad": False}).neq("id", 0).execute()
    print("  Reset all to false")

    # Mark in batches using filter on id list
    ids_list = list(ids_to_mark)
    batch_size = 500
    total_marked = 0
    for i in range(0, len(ids_list), batch_size):
        batch = ids_list[i:i+batch_size]
        supabase.table("wc2026_players") \
            .update({"in_squad": True}) \
            .in_("id", batch) \
            .execute()
        total_marked += len(batch)
        print(f"  Marked {total_marked}/{len(ids_list)}...")

    print(f"Done — {total_marked} players marked as in_squad=true")
    return ids_to_mark

def match_squad_to_stats(squads, db_players):
    db_lookup = {}
    for p in db_players:
        if p.get("player") and p.get("nation"):
            key = (normalize(p["player"]), p["nation"])
            db_lookup[key] = p

    name_lookup = {}
    for p in db_players:
        if p.get("player"):
            norm = normalize(p["player"])
            if norm not in name_lookup:
                name_lookup[norm] = p

    matched_stats = {}
    for code, players in squads.items():
        matched_stats[code] = []
        for p in players:
            key = (p["name_norm"], code)
            if key in db_lookup:
                stats = db_lookup[key].copy()
                stats["position_squad"] = p["position"]
                matched_stats[code].append(stats)
            elif p["name_norm"] in name_lookup:
                stats = name_lookup[p["name_norm"]].copy()
                stats["position_squad"] = p["position"]
                matched_stats[code].append(stats)
            else:
                matched_stats[code].append({
                    "player": p["name"], "nation": code,
                    "position_squad": p["position"],
                    "minutes": 0, "goals": 0, "assists": 0,
                    "xg": None, "xa": None,
                    "shots": None, "shots_on_target": None,
                })
    return matched_stats

def compute_scores(matched_stats):
    scores = {}
    for code, players in matched_stats.items():
        team_name = CODE_TO_TEAM.get(code, code)
        active = [p for p in players if (p.get("minutes") or 0) >= 200]
        if not active:
            active = [p for p in players if (p.get("minutes") or 0) > 0]
        if not active:
            active = players

        def per90(stat, player):
            mins = max(player.get("minutes") or 1, 1)
            return ((player.get(stat) or 0) / mins) * 90

        by_xg = sorted(active, key=lambda p: (p.get("xg") or 0), reverse=True)
        top_att = by_xg[:6]
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

    raws = [v["raw"] for v in scores.values() if v.get("raw", 0) > 0]
    if raws:
        min_r, max_r = min(raws), max(raws)
        for team in scores:
            raw = scores[team].get("raw", 0)
            scores[team]["score"] = round(20 + ((raw - min_r) / (max_r - min_r)) * 75, 1) if max_r > min_r else 50
    return scores

def simulate_group(teams, scores):
    standings = {t: {"pts":0,"gf":0,"ga":0} for t in teams}
    for i in range(len(teams)):
        for j in range(i+1, len(teams)):
            h, a = teams[i], teams[j]
            hs = scores.get(h,{}).get("score",40)
            as_ = scores.get(a,{}).get("score",40)
            if abs(hs-as_) < 8:
                standings[h]["pts"] += 1; standings[a]["pts"] += 1
            elif hs > as_:
                standings[h]["pts"] += 3; standings[h]["gf"] += 1; standings[a]["ga"] += 1
            else:
                standings[a]["pts"] += 3; standings[a]["gf"] += 1; standings[h]["ga"] += 1
    return sorted(teams, key=lambda t:(standings[t]["pts"],standings[t]["gf"]-standings[t]["ga"],scores.get(t,{}).get("score",0)),reverse=True), standings

def simulate_knockout(t1, t2, scores):
    return t1 if scores.get(t1,{}).get("score",40) >= scores.get(t2,{}).get("score",40) else t2

def build_predictions(scores):
    group_results = {}
    for letter, teams in GROUPS.items():
        sorted_teams, standings = simulate_group(teams, scores)
        group_results[letter] = [{"team":t,"pts":standings[t]["pts"],"gf":standings[t]["gf"],"ga":standings[t]["ga"],"score":round(scores.get(t,{}).get("score",0),1)} for t in sorted_teams]

    third_place = sorted([group_results[l][2] for l in group_results], key=lambda x:(x["pts"],x["gf"]-x["ga"],x["score"]),reverse=True)
    best_third = [t["team"] for t in third_place[:8]]
    adv = {f"{l}1":group_results[l][0]["team"] for l in group_results}
    adv.update({f"{l}2":group_results[l][1]["team"] for l in group_results})

    r32p = [(adv["A1"],adv["B2"]),(adv["C1"],adv["D2"]),(adv["E1"],adv["F2"]),(adv["G1"],adv["H2"]),
            (adv["I1"],adv["J2"]),(adv["K1"],adv["L2"]),(adv["B1"],adv["A2"]),(adv["D1"],adv["C2"]),
            (adv["F1"],adv["E2"]),(adv["H1"],adv["G2"]),(adv["J1"],adv["I2"]),(adv["L1"],adv["K2"]),
            (best_third[0],best_third[1]),(best_third[2],best_third[3]),(best_third[4],best_third[5]),(best_third[6],best_third[7])]

    def sim_round(pairs): return [simulate_knockout(a,b,scores) for a,b in pairs]
    r32w=sim_round(r32p); r16p=list(zip(r32w[::2],r32w[1::2])); r16w=sim_round(r16p)
    qfp=list(zip(r16w[::2],r16w[1::2])); qfw=sim_round(qfp)
    sfp=list(zip(qfw[::2],qfw[1::2])); sfw=sim_round(sfp)
    sfl=[qfw[i*2+(0 if sfw[i]==qfw[i*2+1] else 1)] for i in range(2)]
    champion=simulate_knockout(sfw[0],sfw[1],scores); third=simulate_knockout(sfl[0],sfl[1],scores)

    return {
        "generated_at": __import__("datetime").datetime.utcnow().isoformat()+"Z",
        "scores": {k:{"score":v["score"],"attack":v.get("attack",0),"creativity":v.get("creativity",0),"players_matched":v.get("players_matched",0)} for k,v in scores.items()},
        "groups": group_results,
        "bracket": {
            "r32":[{"home":a,"away":b,"winner":w} for (a,b),w in zip(r32p,r32w)],
            "r16":[{"home":a,"away":b,"winner":w} for (a,b),w in zip(r16p,r16w)],
            "qf":[{"home":a,"away":b,"winner":w} for (a,b),w in zip(qfp,qfw)],
            "sf":[{"home":a,"away":b,"winner":w} for (a,b),w in zip(sfp,sfw)],
            "final":{"home":sfw[0],"away":sfw[1],"winner":champion},
            "third":{"home":sfl[0],"away":sfl[1],"winner":third},
        }
    }

def main():
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

    squads = scrape_wikipedia_squads()
    db_players = fetch_supabase_players(supabase)
    mark_squad_players(supabase, squads, db_players)
    matched = match_squad_to_stats(squads, db_players)
    scores = compute_scores(matched)
    predictions = build_predictions(scores)

    champion = predictions["bracket"]["final"]["winner"]
    print(f"\n=== PREDICTED CHAMPION: {champion} ===")
    top5 = sorted(scores.items(), key=lambda x:x[1].get("score",0), reverse=True)[:5]
    for i,(t,s) in enumerate(top5,1):
        print(f"  {i}. {t}: {s['score']} ({s.get('players_matched',0)} matched)")

    os.makedirs("src/data", exist_ok=True)
    with open("src/data/prediction_data.json","w") as f:
        json.dump(predictions, f, indent=2)
    print("Wrote prediction_data.json")

    squads_out = {code:[{"name":p["name"],"position":p["position"]} for p in players] for code,players in squads.items()}
    with open("src/data/squads.json","w") as f:
        json.dump(squads_out, f, indent=2)
    print("Wrote squads.json")

if __name__ == "__main__":
    main()
