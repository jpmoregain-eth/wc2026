import { useState } from "react"

const FLAG_EMOJI = {
  "Mexico":"🇲🇽","South Africa":"🇿🇦","South Korea":"🇰🇷","Czechia":"🇨🇿",
  "Canada":"🇨🇦","Bosnia & Herzegovina":"🇧🇦","Qatar":"🇶🇦","Switzerland":"🇨🇭",
  "Brazil":"🇧🇷","Morocco":"🇲🇦","Haiti":"🇭🇹","Scotland":"🏴󠁧󠁢󠁳󠁣󠁴󠁿",
  "USA":"🇺🇸","Paraguay":"🇵🇾","Australia":"🇦🇺","Turkey":"🇹🇷",
  "Germany":"🇩🇪","Curaçao":"🇨🇼","Ivory Coast":"🇨🇮","Ecuador":"🇪🇨",
  "Netherlands":"🇳🇱","Japan":"🇯🇵","Sweden":"🇸🇪","Tunisia":"🇹🇳",
  "Belgium":"🇧🇪","Egypt":"🇪🇬","Iran":"🇮🇷","New Zealand":"🇳🇿",
  "Spain":"🇪🇸","Cape Verde":"🇨🇻","Saudi Arabia":"🇸🇦","Uruguay":"🇺🇾",
  "France":"🇫🇷","Senegal":"🇸🇳","Iraq":"🇮🇶","Norway":"🇳🇴",
  "Argentina":"🇦🇷","Algeria":"🇩🇿","Austria":"🇦🇹","Jordan":"🇯🇴",
  "Portugal":"🇵🇹","DR Congo":"🇨🇩","Uzbekistan":"🇺🇿","Colombia":"🇨🇴",
  "England":"🏴󠁧󠁢󠁥󠁮󠁧󠁿","Croatia":"🇭🇷","Ghana":"🇬🇭","Panama":"🇵🇦",
  "Nigeria":"🇳🇬","Senegal":"🇸🇳","Morocco":"🇲🇦",
}

const SCORES = {"England":{"score":89.3,"attack":5.64,"creativity":1.79},"France":{"score":88.5,"attack":5.48,"creativity":2.45},"Spain":{"score":86.4,"attack":5.36,"creativity":1.93},"Germany":{"score":95.0,"attack":6.12,"creativity":1.91},"Portugal":{"score":73.8,"attack":4.09,"creativity":2.39},"Netherlands":{"score":65.4,"attack":3.87,"creativity":1.12},"Belgium":{"score":61.5,"attack":2.99,"creativity":2.32},"Croatia":{"score":47.5,"attack":1.85,"creativity":1.3},"Switzerland":{"score":45.6,"attack":1.85,"creativity":1.07},"Austria":{"score":53.9,"attack":2.68,"creativity":1.37},"Scotland":{"score":45.3,"attack":1.94,"creativity":1.02},"Norway":{"score":70.3,"attack":4.03,"creativity":1.81},"Denmark":{"score":59.3,"attack":2.96,"creativity":1.79},"Sweden":{"score":55.4,"attack":2.87,"creativity":1.27},"Turkey":{"score":52.7,"attack":2.28,"creativity":1.54},"Bosnia & Herzegovina":{"score":32.0,"attack":0.71,"creativity":0.14},"Czechia":{"score":45.5,"attack":1.85,"creativity":0.9},"Brazil":{"score":80.9,"attack":5.0,"creativity":1.97},"Argentina":{"score":78.7,"attack":4.75,"creativity":2.04},"Colombia":{"score":46.3,"attack":2.02,"creativity":1.46},"Uruguay":{"score":46.9,"attack":2.17,"creativity":0.87},"Ecuador":{"score":24.1,"attack":0.12,"creativity":0.09},"Venezuela":{"score":28.6,"attack":0.48,"creativity":0.12},"Paraguay":{"score":35.7,"attack":0.93,"creativity":0.5},"Chile":{"score":28.5,"attack":0.42,"creativity":0.27},"USA":{"score":52.1,"attack":2.51,"creativity":1.42},"Mexico":{"score":39.4,"attack":1.63,"creativity":1.0},"Canada":{"score":33.5,"attack":0.79,"creativity":0.46},"Panama":{"score":22.6,"attack":0.0,"creativity":0.0},"Honduras":{"score":20.4,"attack":0.02,"creativity":0.03},"Jamaica":{"score":20.0,"attack":0.01,"creativity":0.02},"Curaçao":{"score":21.6,"attack":0.0,"creativity":0.0},"Haiti":{"score":27.5,"attack":0.65,"creativity":0.25},"Costa Rica":{"score":20.8,"attack":0.0,"creativity":0.0},"Japan":{"score":51.3,"attack":2.3,"creativity":1.68},"South Korea":{"score":28.0,"attack":0.24,"creativity":0.42},"Australia":{"score":22.2,"attack":0.09,"creativity":0.05},"Saudi Arabia":{"score":23.0,"attack":0.03,"creativity":0.13},"Iran":{"score":19.8,"attack":0,"creativity":0},"Qatar":{"score":19.8,"attack":0,"creativity":0},"Jordan":{"score":20.3,"attack":0.0,"creativity":0.0},"Uzbekistan":{"score":19.8,"attack":0.0,"creativity":0.0},"Iraq":{"score":20.9,"attack":0.0,"creativity":0.0},"Morocco":{"score":51.1,"attack":2.37,"creativity":1.18},"Senegal":{"score":63.1,"attack":3.82,"creativity":1.09},"Nigeria":{"score":60.3,"attack":3.36,"creativity":1.65},"Cameroon":{"score":40.5,"attack":1.59,"creativity":0.77},"Egypt":{"score":35.0,"attack":1.18,"creativity":0.7},"Ivory Coast":{"score":54.0,"attack":2.56,"creativity":1.64},"Cape Verde":{"score":22.6,"attack":0.0,"creativity":0.0},"DR Congo":{"score":26.7,"attack":0.56,"creativity":0.24},"South Africa":{"score":23.7,"attack":0.24,"creativity":0.08},"Ghana":{"score":50.4,"attack":2.57,"creativity":1.17},"New Zealand":{"score":23.8,"attack":0.34,"creativity":0.03},"Algeria":{"score":19.8,"attack":0,"creativity":0},"Tunisia":{"score":19.8,"attack":0,"creativity":0}}

const GROUPS = {"A":[{"team":"Czechia","pts":7,"gf":2,"ga":0,"score":45.5},{"team":"Mexico","pts":7,"gf":2,"ga":0,"score":39.4},{"team":"South Korea","pts":1,"gf":0,"ga":2,"score":28.0},{"team":"South Africa","pts":1,"gf":0,"ga":2,"score":23.7}],"B":[{"team":"Switzerland","pts":9,"gf":3,"ga":0,"score":45.6},{"team":"Canada","pts":4,"gf":1,"ga":1,"score":33.5},{"team":"Bosnia & Herzegovina","pts":4,"gf":1,"ga":1,"score":32.0},{"team":"Qatar","pts":0,"gf":0,"ga":3,"score":19.8}],"C":[{"team":"Brazil","pts":9,"gf":3,"ga":0,"score":80.9},{"team":"Morocco","pts":4,"gf":2,"ga":2,"score":51.1},{"team":"Scotland","pts":4,"gf":1,"ga":1,"score":45.3},{"team":"Haiti","pts":0,"gf":0,"ga":3,"score":27.5}],"D":[{"team":"Turkey","pts":7,"gf":3,"ga":1,"score":52.7},{"team":"USA","pts":7,"gf":3,"ga":1,"score":52.1},{"team":"Paraguay","pts":3,"gf":1,"ga":2,"score":35.7},{"team":"Australia","pts":0,"gf":0,"ga":3,"score":22.2}],"E":[{"team":"Germany","pts":9,"gf":6,"ga":0,"score":95.0},{"team":"Ivory Coast","pts":6,"gf":2,"ga":2,"score":54.0},{"team":"Ecuador","pts":1,"gf":0,"ga":3,"score":24.1},{"team":"Curaçao","pts":1,"gf":0,"ga":3,"score":21.6}],"F":[{"team":"Netherlands","pts":9,"gf":3,"ga":0,"score":65.4},{"team":"Sweden","pts":4,"gf":2,"ga":2,"score":55.4},{"team":"Japan","pts":4,"gf":2,"ga":2,"score":51.3},{"team":"Tunisia","pts":0,"gf":0,"ga":3,"score":19.8}],"G":[{"team":"Belgium","pts":9,"gf":3,"ga":0,"score":61.5},{"team":"Egypt","pts":6,"gf":2,"ga":1,"score":35.0},{"team":"New Zealand","pts":1,"gf":0,"ga":2,"score":23.8},{"team":"Iran","pts":1,"gf":0,"ga":2,"score":19.8}],"H":[{"team":"Spain","pts":9,"gf":3,"ga":0,"score":86.4},{"team":"Uruguay","pts":6,"gf":2,"ga":1,"score":46.9},{"team":"Saudi Arabia","pts":1,"gf":0,"ga":2,"score":23.0},{"team":"Cape Verde","pts":1,"gf":0,"ga":2,"score":22.6}],"I":[{"team":"France","pts":9,"gf":3,"ga":0,"score":88.5},{"team":"Norway","pts":4,"gf":2,"ga":2,"score":70.3},{"team":"Senegal","pts":4,"gf":2,"ga":2,"score":63.1},{"team":"Iraq","pts":0,"gf":0,"ga":3,"score":20.9}],"J":[{"team":"Argentina","pts":9,"gf":3,"ga":0,"score":78.7},{"team":"Austria","pts":6,"gf":2,"ga":1,"score":53.9},{"team":"Jordan","pts":1,"gf":0,"ga":2,"score":20.3},{"team":"Algeria","pts":1,"gf":0,"ga":2,"score":19.8}],"K":[{"team":"Portugal","pts":9,"gf":3,"ga":0,"score":73.8},{"team":"Colombia","pts":6,"gf":2,"ga":1,"score":46.3},{"team":"DR Congo","pts":1,"gf":0,"ga":2,"score":26.7},{"team":"Uzbekistan","pts":1,"gf":0,"ga":2,"score":19.8}],"L":[{"team":"England","pts":9,"gf":3,"ga":0,"score":89.3},{"team":"Ghana","pts":4,"gf":2,"ga":2,"score":50.4},{"team":"Croatia","pts":4,"gf":1,"ga":1,"score":47.5},{"team":"Panama","pts":0,"gf":0,"ga":3,"score":22.6}]}

const BRACKET = {"r32":[{"home":"Czechia","away":"Canada","winner":"Czechia"},{"home":"Brazil","away":"USA","winner":"Brazil"},{"home":"Germany","away":"Sweden","winner":"Germany"},{"home":"Belgium","away":"Uruguay","winner":"Belgium"},{"home":"France","away":"Austria","winner":"France"},{"home":"Portugal","away":"Ghana","winner":"Portugal"},{"home":"Switzerland","away":"Mexico","winner":"Switzerland"},{"home":"Turkey","away":"Morocco","winner":"Turkey"},{"home":"Netherlands","away":"Ivory Coast","winner":"Netherlands"},{"home":"Spain","away":"Egypt","winner":"Spain"},{"home":"Argentina","away":"Norway","winner":"Argentina"},{"home":"England","away":"Colombia","winner":"England"},{"home":"Senegal","away":"Japan","winner":"Senegal"},{"home":"Croatia","away":"Scotland","winner":"Croatia"},{"home":"Bosnia & Herzegovina","away":"Paraguay","winner":"Paraguay"},{"home":"South Korea","away":"DR Congo","winner":"South Korea"}],"r16":[{"home":"Czechia","away":"Brazil","winner":"Brazil"},{"home":"Germany","away":"Belgium","winner":"Germany"},{"home":"France","away":"Portugal","winner":"France"},{"home":"Switzerland","away":"Turkey","winner":"Turkey"},{"home":"Netherlands","away":"Spain","winner":"Spain"},{"home":"Argentina","away":"England","winner":"England"},{"home":"Senegal","away":"Croatia","winner":"Senegal"},{"home":"Paraguay","away":"South Korea","winner":"Paraguay"}],"qf":[{"home":"Brazil","away":"Germany","winner":"Germany"},{"home":"France","away":"Turkey","winner":"France"},{"home":"Spain","away":"England","winner":"England"},{"home":"Senegal","away":"Paraguay","winner":"Senegal"}],"sf":[{"home":"Germany","away":"France","winner":"Germany"},{"home":"England","away":"Senegal","winner":"England"}],"final":{"home":"Germany","away":"England","winner":"Germany"},"third":{"home":"France","away":"Senegal","winner":"France"}}

function ScoreBar({ score }) {
  return (
    <div className="flex items-center gap-2 flex-1">
      <div className="h-1.5 bg-white/10 rounded-full flex-1">
        <div className="h-1.5 bg-yellow-400 rounded-full transition-all" style={{ width: `${score}%` }} />
      </div>
      <span className="text-yellow-400 text-xs font-bold w-8 text-right">{score}</span>
    </div>
  )
}

function MatchCard({ home, away, winner, dim }) {
  return (
    <div className={`bg-white/5 border rounded-lg overflow-hidden w-40 ${dim ? "opacity-40" : "border-white/10"}`}>
      <div className={`px-3 py-1.5 text-xs flex items-center gap-1.5 border-b border-white/5
        ${winner === home ? "text-white font-bold" : "text-slate-400"}`}>
        <span>{FLAG_EMOJI[home] || "🏳️"}</span>
        <span className="truncate">{home}</span>
        {winner === home && <span className="ml-auto text-yellow-400 text-xs">✓</span>}
      </div>
      <div className={`px-3 py-1.5 text-xs flex items-center gap-1.5
        ${winner === away ? "text-white font-bold" : "text-slate-400"}`}>
        <span>{FLAG_EMOJI[away] || "🏳️"}</span>
        <span className="truncate">{away}</span>
        {winner === away && <span className="ml-auto text-yellow-400 text-xs">✓</span>}
      </div>
    </div>
  )
}

function GroupCard({ letter, teams }) {
  return (
    <div className="bg-white/5 border border-white/10 rounded-xl overflow-hidden">
      <div className="bg-[#1a3c6e] px-4 py-2.5 flex items-center gap-2">
        <span className="bg-yellow-400 text-blue-900 font-extrabold text-sm w-7 h-7 rounded flex items-center justify-center">{letter}</span>
        <span className="text-white font-semibold text-sm">Group {letter}</span>
        <span className="ml-auto text-slate-400 text-xs">Predicted</span>
      </div>
      <table className="w-full text-xs">
        <thead>
          <tr className="text-slate-500 border-b border-white/5">
            <th className="text-left px-3 py-2">Team</th>
            <th className="px-2 py-2">Pts</th>
            <th className="px-2 py-2">GF</th>
            <th className="px-2 py-2">GA</th>
            <th className="px-3 py-2 text-right">Strength</th>
          </tr>
        </thead>
        <tbody>
          {teams.map((t, i) => (
            <tr key={t.team} className={`border-b border-white/5 last:border-0 
              ${i < 2 ? "border-l-2 border-l-green-500" : ""}`}>
              <td className="px-3 py-2.5 flex items-center gap-2">
                <span className="text-base">{FLAG_EMOJI[t.team] || "🏳️"}</span>
                <span className={`font-medium ${i < 2 ? "text-white" : "text-slate-400"}`}>{t.team}</span>
              </td>
              <td className="text-center px-2 py-2.5 text-white font-bold">{t.pts}</td>
              <td className="text-center px-2 py-2.5 text-slate-400">{t.gf}</td>
              <td className="text-center px-2 py-2.5 text-slate-400">{t.ga}</td>
              <td className="px-3 py-2.5">
                <ScoreBar score={t.score} />
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      <div className="px-3 py-1.5 text-slate-600 text-xs border-t border-white/5">
        <span className="inline-block w-2 h-2 bg-green-500 rounded-sm mr-1"/>
        Top 2 advance to Round of 32
      </div>
    </div>
  )
}

function BracketRound({ title, matches, highlightWinners = false }) {
  return (
    <div className="flex flex-col items-center gap-2">
      <h3 className="text-yellow-400 font-bold text-xs text-center mb-2 whitespace-nowrap">{title}</h3>
      <div className="flex flex-col gap-3">
        {matches.map((m, i) => (
          <MatchCard key={i} home={m.home} away={m.away} winner={m.winner} />
        ))}
      </div>
    </div>
  )
}

export default function Predictions() {
  const [tab, setTab] = useState("groups")

  return (
    <div className="max-w-6xl mx-auto px-4 py-10">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-extrabold text-white mb-2">Tournament Predictions</h1>
        <p className="text-slate-400">Based on 2025–26 club season xG, xA & goals · For entertainment only</p>
      </div>

      {/* Predicted winner banner */}
      <div className="bg-gradient-to-r from-yellow-500/10 to-yellow-600/5 border border-yellow-500/30 rounded-2xl p-6 mb-8 flex flex-wrap items-center gap-6">
        <div>
          <p className="text-yellow-400 text-xs uppercase tracking-widest mb-1">Predicted Champion</p>
          <div className="flex items-center gap-3">
            <span className="text-5xl">{FLAG_EMOJI[BRACKET.final.winner]}</span>
            <span className="text-4xl font-extrabold text-white">{BRACKET.final.winner}</span>
          </div>
        </div>
        <div className="h-12 w-px bg-white/10 hidden sm:block" />
        <div className="flex gap-8">
          <div>
            <p className="text-slate-500 text-xs mb-1">Final</p>
            <p className="text-slate-300 text-sm">
              {FLAG_EMOJI[BRACKET.final.home]} {BRACKET.final.home} vs {FLAG_EMOJI[BRACKET.final.away]} {BRACKET.final.away}
            </p>
          </div>
          <div>
            <p className="text-slate-500 text-xs mb-1">3rd Place</p>
            <p className="text-slate-300 text-sm">
              {FLAG_EMOJI[BRACKET.third.winner]} {BRACKET.third.winner}
            </p>
          </div>
          <div>
            <p className="text-slate-500 text-xs mb-1">Strength Score</p>
            <p className="text-yellow-400 font-bold">{SCORES[BRACKET.final.winner]?.score} / 100</p>
          </div>
        </div>
      </div>

      {/* Top 5 teams */}
      <div className="mb-8">
        <h2 className="text-sm font-semibold text-slate-400 uppercase tracking-widest mb-3">Top 5 by Strength Score</h2>
        <div className="flex flex-wrap gap-3">
          {Object.entries(SCORES)
            .sort((a,b) => b[1].score - a[1].score)
            .slice(0,5)
            .map(([team, s], i) => (
              <div key={team} className="bg-white/5 border border-white/10 rounded-xl px-4 py-3 flex items-center gap-3 min-w-[160px]">
                <span className="text-slate-500 font-bold text-lg">#{i+1}</span>
                <span className="text-2xl">{FLAG_EMOJI[team] || "🏳️"}</span>
                <div>
                  <div className="text-white font-semibold text-sm">{team}</div>
                  <div className="text-yellow-400 text-xs font-bold">{s.score} pts</div>
                </div>
              </div>
            ))}
        </div>
      </div>

      {/* Tab switcher */}
      <div className="flex gap-2 mb-6">
        {["groups","bracket"].map(t => (
          <button key={t} onClick={() => setTab(t)}
            className={`px-5 py-2 rounded-lg text-sm font-semibold capitalize transition-colors
              ${tab === t ? "bg-yellow-400 text-blue-900" : "bg-white/5 text-slate-300 hover:bg-white/10"}`}>
            {t === "groups" ? "Group Stage" : "Bracket"}
          </button>
        ))}
      </div>

      {/* Groups tab */}
      {tab === "groups" && (
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-5">
          {Object.entries(GROUPS).map(([letter, teams]) => (
            <GroupCard key={letter} letter={letter} teams={teams} />
          ))}
        </div>
      )}

      {/* Bracket tab */}
      {tab === "bracket" && (
        <div className="overflow-x-auto pb-8">
          <div className="flex gap-5 items-start w-fit mx-auto">
            <BracketRound title="Round of 32" matches={BRACKET.r32.slice(0,8)} />
            <BracketRound title="Round of 16" matches={BRACKET.r16.slice(0,4)} />
            <BracketRound title="Quarters" matches={BRACKET.qf.slice(0,2)} />
            <div className="flex flex-col gap-3 items-center">
              <h3 className="text-yellow-400 font-bold text-xs mb-2">Semis</h3>
              <MatchCard {...BRACKET.sf[0]} />
            </div>
            <div className="flex flex-col gap-3 items-center pt-6">
              <h3 className="text-yellow-400 font-bold text-xs mb-2">🏆 Final</h3>
              <MatchCard {...BRACKET.final} />
              <h3 className="text-slate-500 font-bold text-xs mt-4 mb-2">3rd Place</h3>
              <MatchCard {...BRACKET.third} />
            </div>
            <div className="flex flex-col gap-3 items-center">
              <h3 className="text-yellow-400 font-bold text-xs mb-2">Semis</h3>
              <MatchCard {...BRACKET.sf[1]} />
            </div>
            <BracketRound title="Quarters" matches={BRACKET.qf.slice(2)} />
            <BracketRound title="Round of 16" matches={BRACKET.r16.slice(4)} />
            <BracketRound title="Round of 32" matches={BRACKET.r32.slice(8)} />
          </div>
        </div>
      )}

      {/* Disclaimer */}
      <div className="mt-10 p-4 bg-white/3 border border-white/5 rounded-xl text-center">
        <p className="text-slate-600 text-xs">
          ⚠️ Predictions are based on individual club-level stats (xG, xA, goals) from the 2025–26 season across 8 leagues.
          They do not account for team tactics, home advantage, injuries, or form.
          For entertainment purposes only.
        </p>
      </div>
    </div>
  )
}
