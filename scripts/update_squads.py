"""
WC 2026 Squad Scraper + Score Calculator v4
Uses wc2026_national_stats for predictions (real WC squad data)
"""

import os, json, re, requests
from bs4 import BeautifulSoup
from supabase import create_client

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_SERVICE_KEY"]

NATION_CODES = {
    "Czech Republic":"CZE","Mexico":"MEX","South Africa":"RSA","South Korea":"KOR",
    "Bosnia and Herzegovina":"BIH","Canada":"CAN","Qatar":"QAT","Switzerland":"SUI",
    "Brazil":"BRA","Haiti":"HAI","Morocco":"MAR","Scotland":"SCO",
    "Australia":"AUS","Paraguay":"PAR","Türkiye":"TUR","Turkey":"TUR",
    "United States":"USA","Curaçao":"CUW","Ecuador":"ECU","Germany":"GER",
    "Côte d'Ivoire":"CIV","Ivory Coast":"CIV","Japan":"JPN","Netherlands":"NED",
    "Sweden":"SWE","Tunisia":"TUN","Belgium":"BEL","Egypt":"EGY",
    "IR Iran":"IRN","Iran":"IRN","New Zealand":"NZL","Cabo Verde":"CPV",
    "Cape Verde":"CPV","Saudi Arabia":"KSA","Spain":"ESP","Uruguay":"URU",
    "France":"FRA","Iraq":"IRQ","Norway":"NOR","Senegal":"SEN","Algeria":"ALG",
    "Argentina":"ARG","Austria":"AUT","Jordan":"JOR","Colombia":"COL",
    "Congo DR":"COD","DR Congo":"COD","Portugal":"POR","Uzbekistan":"UZB",
    "Croatia":"CRO","England":"ENG","Ghana":"GHA","Panama":"PAN",
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

CODE_TO_TEAM = {
    "MEX":"Mexico","RSA":"South Africa","KOR":"South Korea","CZE":"Czechia",
    "CAN":"Canada","BIH":"Bosnia & Herzegovina","QAT":"Qatar","SUI":"Switzerland",
    "BRA":"Brazil","HAI":"Haiti","MAR":"Morocco","SCO":"Scotland",
    "AUS":"Australia","PAR":"Paraguay","TUR":"Turkey","USA":"USA",
    "CUW":"Curaçao","ECU":"Ecuador","GER":"Germany","CIV":"Ivory Coast",
    "JPN":"Japan","NED":"Netherlands","SWE":"Sweden","TUN":"Tunisia",
    "BEL":"Belgium","EGY":"Egypt","IRN":"Iran","NZL":"New Zealand",
    "CPV":"Cape Verde","KSA":"Saudi Arabia","ESP":"Spain","URU":"Uruguay",
    "FRA":"France","IRQ":"Iraq","NOR":"Norway","SEN":"Senegal","ALG":"Algeria",
    "ARG":"Argentina","AUT":"Austria","JOR":"Jordan","COL":"Colombia",
    "COD":"DR Congo","POR":"Portugal","UZB":"Uzbekistan","CRO":"Croatia",
    "ENG":"England","GHA":"Ghana","PAN":"Panama",
}

POS_MAP = {"1":"GK","2":"DF","3":"MF","4":"FW"}

def normalize(name):
    name = name.lower().strip()
    for k,v in {'á':'a','à':'a','ã':'a','â':'a','ä':'a','é':'e','è':'e','ê':'e',
                'ë':'e','í':'i','ì':'i','î':'i','ï':'i','ó':'o','ò':'o','õ':'o',
                'ô':'o','ö':'o','ú':'u','ù':'u','û':'u','ü':'u','ý':'y','ÿ':'y',
                'ñ':'n','ç':'c','ß':'ss','ø':'o','å':'a','æ':'ae','œ':'oe',
                'š':'s','č':'c','ž':'z','ř':'r','ě':'e','ğ':'g','ı':'i',
                'ł':'l','ń':'n','ś':'s','ț':'t','ș':'s','ă':'a'}.items():
        name = name.replace(k,v)
    return re.sub(r"[^a-z ]","",name).strip()

def scrape_wikipedia_squads():
    print("Scraping Wikipedia squads...")
    url = "https://en.wikipedia.org/wiki/2026_FIFA_World_Cup_squads"
    resp = requests.get(url, headers={"User-Agent":"Mozilla/5.0"}, timeout=30)
    soup = BeautifulSoup(resp.text, "html.parser")

    squads = {}
    current_code = None

    for elem in soup.find_all(["h2","h3","table"]):
        if elem.name in ["h2","h3"]:
            text = elem.get_text(strip=True).replace("[edit]","").strip()
            for team, code in NATION_CODES.items():
                if team.lower() == text.lower():
                    current_code = code
                    if code not in squads:
                        squads[code] = []
                    break

        elif elem.name == "table" and current_code:
            for row in elem.find_all("tr"):
                cells = row.find_all(["td","th"])
                if len(cells) < 3: continue
                texts = [c.get_text(strip=True) for c in cells]
                pos_raw = texts[1] if len(texts) > 1 else ""
                pos = next((p for num,p in POS_MAP.items() if pos_raw.startswith(num) and p in pos_raw), None)
                if pos:
                    name = re.sub(r'\[.*?\]','',re.sub(r'\(.*?\)','',texts[2])).strip()
                    if name and len(name) > 2 and name != "Player":
                        squads[current_code].append({"name":name,"name_norm":normalize(name),"position":pos})

    for code in squads:
        seen = set()
        squads[code] = [p for p in squads[code] if p["name_norm"] not in seen and not seen.add(p["name_norm"])]

    total = sum(len(v) for v in squads.values())
    print(f"Scraped {len(squads)} teams, {total} players")
    return squads

def fetch_national_stats(supabase):
    """Fetch confirmed squad players from national stats table."""
    print("Fetching national stats...")
    all_players = []
    offset = 0
    while True:
        res = supabase.table("wc2026_national_stats") \
            .select("player,nation,goals,assists,caps,age") \
            .eq("in_squad", True) \
            .range(offset, offset+999).execute()
        if not res.data: break
        all_players.extend(res.data)
        offset += 1000
        if len(res.data) < 1000: break
    print(f"Fetched {len(all_players)} squad players")
    return all_players

def compute_scores_from_national(national_players):
    """
    Compute team strength from national stats.
    Primary metric: goals per cap (international finishing rate)
    Secondary: assists per cap (creativity)
    Weighted by caps (more experienced players count more)
    """
    from collections import defaultdict
    by_nation = defaultdict(list)
    for p in national_players:
        if p.get("nation"):
            by_nation[p["nation"]].append(p)

    scores = {}
    for code, team_name in CODE_TO_TEAM.items():
        players = by_nation.get(code, [])

        # Filter to players with at least some data
        active = [p for p in players if (p.get("caps") or 0) > 0]
        if not active:
            active = players

        if not active:
            scores[team_name] = {"raw":0,"score":25,"attack":0,"creativity":0,"experience":0,"players":0}
            continue

        total_caps = sum(p.get("caps") or 0 for p in active) or 1

        # Goals per cap weighted by caps (top scorers matter most)
        by_goals = sorted(active, key=lambda p:(p.get("goals") or 0), reverse=True)
        top_att = by_goals[:8]  # top 8 goal contributors

        by_ast = sorted(active, key=lambda p:(p.get("assists") or 0), reverse=True)
        top_mid = by_ast[:6]

        def goals_per_cap(p):
            caps = max(p.get("caps") or 1, 1)
            return (p.get("goals") or 0) / caps

        def ast_per_cap(p):
            caps = max(p.get("caps") or 1, 1)
            return (p.get("assists") or 0) / caps

        # Attack = sum of goals/cap for top attackers, weighted by caps
        attack = sum(goals_per_cap(p) * min(p.get("caps") or 1, 50) for p in top_att)
        creativity = sum(ast_per_cap(p) * min(p.get("caps") or 1, 50) for p in top_mid)
        experience = min(total_caps / len(active), 100) if active else 0

        # Raw score: attack 55% + creativity 30% + experience 15%
        raw = (attack * 0.55) + (creativity * 0.30) + (experience * 0.15)

        scores[team_name] = {
            "raw":        round(raw, 4),
            "attack":     round(attack, 2),
            "creativity": round(creativity, 2),
            "experience": round(experience, 1),
            "players":    len(active),
        }

    # Normalize to 0-100
    raws = [v["raw"] for v in scores.values() if v.get("raw",0) > 0]
    if raws:
        mn, mx = min(raws), max(raws)
        for t in scores:
            r = scores[t].get("raw",0)
            scores[t]["score"] = round(20 + ((r-mn)/(mx-mn))*75, 1) if mx>mn else 50
    else:
        for t in scores: scores[t]["score"] = 25

    return scores

def mark_squad_players(supabase, squads, national_players):
    """Re-mark in_squad on wc2026_national_stats."""
    print("Marking squad players...")

    db_lookup = {}
    name_lookup = {}
    for p in national_players:
        if not p.get("player"): continue
        norm = normalize(p["player"])
        # Need id - re-fetch with id
    # Skip re-marking in GitHub Action since it was already done manually
    print("  (Skipping re-mark - already done)")

def simulate_group(teams, scores):
    standings = {t:{"pts":0,"gf":0,"ga":0} for t in teams}
    for i in range(len(teams)):
        for j in range(i+1,len(teams)):
            h,a = teams[i],teams[j]
            hs = scores.get(h,{}).get("score",40)
            as_ = scores.get(a,{}).get("score",40)
            if abs(hs-as_) < 8:
                standings[h]["pts"]+=1; standings[a]["pts"]+=1
            elif hs > as_:
                standings[h]["pts"]+=3; standings[h]["gf"]+=1; standings[a]["ga"]+=1
            else:
                standings[a]["pts"]+=3; standings[a]["gf"]+=1; standings[h]["ga"]+=1
    return sorted(teams, key=lambda t:(standings[t]["pts"],standings[t]["gf"]-standings[t]["ga"],scores.get(t,{}).get("score",0)),reverse=True), standings

def simulate_knockout(t1,t2,scores):
    return t1 if scores.get(t1,{}).get("score",40) >= scores.get(t2,{}).get("score",40) else t2

def build_predictions(scores):
    group_results = {}
    for letter, teams in GROUPS.items():
        st, standings = simulate_group(teams, scores)
        group_results[letter] = [{"team":t,"pts":standings[t]["pts"],"gf":standings[t]["gf"],"ga":standings[t]["ga"],"score":round(scores.get(t,{}).get("score",0),1)} for t in st]

    third = sorted([group_results[l][2] for l in group_results], key=lambda x:(x["pts"],x["gf"]-x["ga"],x["score"]),reverse=True)
    bt = [t["team"] for t in third[:8]]
    adv = {f"{l}1":group_results[l][0]["team"] for l in group_results}
    adv.update({f"{l}2":group_results[l][1]["team"] for l in group_results})

    r32p = [(adv["A1"],adv["B2"]),(adv["C1"],adv["D2"]),(adv["E1"],adv["F2"]),(adv["G1"],adv["H2"]),
            (adv["I1"],adv["J2"]),(adv["K1"],adv["L2"]),(adv["B1"],adv["A2"]),(adv["D1"],adv["C2"]),
            (adv["F1"],adv["E2"]),(adv["H1"],adv["G2"]),(adv["J1"],adv["I2"]),(adv["L1"],adv["K2"]),
            (bt[0],bt[1]),(bt[2],bt[3]),(bt[4],bt[5]),(bt[6],bt[7])]

    def sr(pairs): return [simulate_knockout(a,b,scores) for a,b in pairs]
    r32w=sr(r32p); r16p=list(zip(r32w[::2],r32w[1::2])); r16w=sr(r16p)
    qfp=list(zip(r16w[::2],r16w[1::2])); qfw=sr(qfp)
    sfp=list(zip(qfw[::2],qfw[1::2])); sfw=sr(sfp)
    sfl=[qfw[i*2+(0 if sfw[i]==qfw[i*2+1] else 1)] for i in range(2)]
    champ=simulate_knockout(sfw[0],sfw[1],scores)
    third_w=simulate_knockout(sfl[0],sfl[1],scores)

    import datetime
    return {
        "generated_at": datetime.datetime.utcnow().isoformat()+"Z",
        "model": "national_stats_v2",
        "model_description": "Based on international goals/caps, assists/caps weighted by experience. Confirmed 26-man WC squads.",
        "scores":{k:{"score":v["score"],"attack":v.get("attack",0),"creativity":v.get("creativity",0),"experience":v.get("experience",0),"players":v.get("players",0)} for k,v in scores.items()},
        "groups":group_results,
        "bracket":{
            "r32":[{"home":a,"away":b,"winner":w} for (a,b),w in zip(r32p,r32w)],
            "r16":[{"home":a,"away":b,"winner":w} for (a,b),w in zip(r16p,r16w)],
            "qf":[{"home":a,"away":b,"winner":w} for (a,b),w in zip(qfp,qfw)],
            "sf":[{"home":a,"away":b,"winner":w} for (a,b),w in zip(sfp,sfw)],
            "final":{"home":sfw[0],"away":sfw[1],"winner":champ},
            "third":{"home":sfl[0],"away":sfl[1],"winner":third_w},
        }
    }

def main():
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

    squads = scrape_wikipedia_squads()
    national_players = fetch_national_stats(supabase)
    scores = compute_scores_from_national(national_players)
    predictions = build_predictions(scores)

    champ = predictions["bracket"]["final"]["winner"]
    print(f"\n=== PREDICTED CHAMPION: {champ} ===")
    top5 = sorted(scores.items(), key=lambda x:x[1].get("score",0), reverse=True)[:10]
    for i,(t,s) in enumerate(top5,1):
        print(f"  {i}. {t}: {s['score']} (atk:{s.get('attack',0):.2f} crt:{s.get('creativity',0):.2f} exp:{s.get('experience',0):.0f})")

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
