import { useState, useMemo } from "react"
import SCHEDULE_RAW from "../data/schedule.json"

const FLAG_EMOJI = {
  MEX:"🇲🇽",RSA:"🇿🇦",KOR:"🇰🇷",CZE:"🇨🇿",CAN:"🇨🇦",BIH:"🇧🇦",QAT:"🇶🇦",SUI:"🇨🇭",
  BRA:"🇧🇷",MAR:"🇲🇦",HAI:"🇭🇹",SCO:"🏴󠁧󠁢󠁳󠁣󠁴󠁿",USA:"🇺🇸",PAR:"🇵🇾",AUS:"🇦🇺",TUR:"🇹🇷",
  GER:"🇩🇪",CUW:"🇨🇼",CIV:"🇨🇮",ECU:"🇪🇨",NED:"🇳🇱",JPN:"🇯🇵",SWE:"🇸🇪",TUN:"🇹🇳",
  BEL:"🇧🇪",EGY:"🇪🇬",IRN:"🇮🇷",NZL:"🇳🇿",ESP:"🇪🇸",CPV:"🇨🇻",KSA:"🇸🇦",URU:"🇺🇾",
  FRA:"🇫🇷",SEN:"🇸🇳",IRQ:"🇮🇶",NOR:"🇳🇴",ARG:"🇦🇷",ALG:"🇩🇿",AUT:"🇦🇹",JOR:"🇯🇴",
  POR:"🇵🇹",COD:"🇨🇩",UZB:"🇺🇿",COL:"🇨🇴",ENG:"🏴󠁧󠁢󠁥󠁮󠁧󠁿",CRO:"🇭🇷",GHA:"🇬🇭",PAN:"🇵🇦",
}

const STAGE_COLORS = {
  "Group A":"bg-blue-500/20 text-blue-300",
  "Group B":"bg-purple-500/20 text-purple-300",
  "Group C":"bg-green-500/20 text-green-300",
  "Group D":"bg-orange-500/20 text-orange-300",
  "Group E":"bg-red-500/20 text-red-300",
  "Group F":"bg-pink-500/20 text-pink-300",
  "Group G":"bg-yellow-500/20 text-yellow-300",
  "Group H":"bg-teal-500/20 text-teal-300",
  "Group I":"bg-indigo-500/20 text-indigo-300",
  "Group J":"bg-cyan-500/20 text-cyan-300",
  "Group K":"bg-lime-500/20 text-lime-300",
  "Group L":"bg-rose-500/20 text-rose-300",
  "Round of 32":"bg-yellow-500/20 text-yellow-300",
  "Round of 16":"bg-orange-500/20 text-orange-300",
  "Quarter-Final":"bg-red-500/20 text-red-300",
  "Semi-Final":"bg-purple-500/20 text-purple-300",
  "Final":"bg-yellow-400/30 text-yellow-300",
}

// Convert ET to GMT (ET + 4 hours during summer EDT = UTC-4)
function etToGmt(date, timeEt) {
  const [h, m] = timeEt.split(":").map(Number)
  const gmtH = (h + 4) % 24
  const nextDay = h + 4 >= 24
  return {
    time: `${String(gmtH).padStart(2,"0")}:${String(m).padStart(2,"0")}`,
    nextDay,
  }
}

function formatDate(dateStr) {
  const d = new Date(dateStr + "T12:00:00")
  return d.toLocaleDateString("en-US", { weekday:"short", month:"short", day:"numeric" })
}

// Group matches by date
function groupByDate(matches) {
  const groups = {}
  for (const m of matches) {
    if (!groups[m.date]) groups[m.date] = []
    groups[m.date].push(m)
  }
  return groups
}

function MatchCard({ match }) {
  const gmt = etToGmt(match.date, match.time_et)
  const isKnownTeam = !match.home.startsWith("W") && !match.home.startsWith("1") && !match.home.startsWith("2") && !match.home.startsWith("3")
  const stageColor = STAGE_COLORS[match.stage_name] || "bg-white/10 text-slate-300"

  return (
    <div className="bg-white/5 border border-white/10 rounded-xl p-4 hover:bg-white/8 transition-all">
      <div className="flex items-center justify-between mb-3">
        <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${stageColor}`}>
          {match.stage_name}
        </span>
        <span className="text-slate-500 text-xs">#{match.match}</span>
      </div>

      {/* Teams */}
      <div className="flex items-center justify-between gap-3 mb-3">
        <div className="flex-1 flex flex-col items-center gap-1">
          <span className="text-3xl">{FLAG_EMOJI[match.home] || "🏳️"}</span>
          <span className="text-sm font-semibold text-white text-center leading-tight">
            {isKnownTeam ? match.home_name : match.home}
          </span>
        </div>
        <div className="flex flex-col items-center">
          <span className="text-slate-400 text-lg font-bold">vs</span>
        </div>
        <div className="flex-1 flex flex-col items-center gap-1">
          <span className="text-3xl">{FLAG_EMOJI[match.away] || "🏳️"}</span>
          <span className="text-sm font-semibold text-white text-center leading-tight">
            {isKnownTeam ? match.away_name : match.away}
          </span>
        </div>
      </div>

      {/* Time & Venue */}
      <div className="border-t border-white/5 pt-3 flex items-center justify-between text-xs">
        <div className="text-slate-400">
          <span className="text-white font-semibold">{gmt.time} GMT</span>
          {gmt.nextDay && <span className="text-slate-500 ml-1">(+1 day)</span>}
          <span className="text-slate-600 ml-2">{match.time_et} ET</span>
        </div>
        <div className="text-slate-500 text-right">
          <div>{match.venue}</div>
          <div className="text-slate-600">{match.city}</div>
        </div>
      </div>
    </div>
  )
}

const FILTER_OPTIONS = [
  { label: "All", value: "all" },
  { label: "Groups", value: "group" },
  { label: "Knockouts", value: "knockout" },
  { label: "Group A", value: "A" }, { label: "Group B", value: "B" },
  { label: "Group C", value: "C" }, { label: "Group D", value: "D" },
  { label: "Group E", value: "E" }, { label: "Group F", value: "F" },
  { label: "Group G", value: "G" }, { label: "Group H", value: "H" },
  { label: "Group I", value: "I" }, { label: "Group J", value: "J" },
  { label: "Group K", value: "K" }, { label: "Group L", value: "L" },
]

const KNOCKOUT_STAGES = ["R32","R16","QF","SF","BF","F"]

export default function Schedule() {
  const [filter, setFilter] = useState("all")
  const [search, setSearch] = useState("")

  const filtered = useMemo(() => {
    return SCHEDULE_RAW.filter(m => {
      if (filter === "group") return !KNOCKOUT_STAGES.includes(m.stage)
      if (filter === "knockout") return KNOCKOUT_STAGES.includes(m.stage)
      if (filter !== "all") return m.stage === filter
      if (search) {
        const s = search.toLowerCase()
        return m.home_name.toLowerCase().includes(s) ||
               m.away_name.toLowerCase().includes(s) ||
               m.city.toLowerCase().includes(s)
      }
      return true
    })
  }, [filter, search])

  const byDate = groupByDate(filtered)
  const today = new Date().toISOString().split("T")[0]

  return (
    <div className="max-w-6xl mx-auto px-4 py-10">
      <div className="mb-8">
        <h1 className="text-3xl font-extrabold text-white mb-2">Match Schedule</h1>
        <p className="text-slate-400">All 104 matches · Times shown in GMT & ET</p>
      </div>

      {/* Filters */}
      <div className="flex flex-wrap gap-2 mb-4">
        <input
          value={search}
          onChange={e => { setSearch(e.target.value); setFilter("all") }}
          placeholder="Search team or city..."
          className="bg-white/5 border border-white/10 rounded-lg px-3 py-1.5 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-yellow-500/50 w-44"
        />
      </div>
      <div className="flex flex-wrap gap-2 mb-8">
        {FILTER_OPTIONS.map(f => (
          <button key={f.value} onClick={() => { setFilter(f.value); setSearch("") }}
            className={`px-3 py-1 rounded-lg text-xs font-medium transition-colors
              ${filter === f.value ? "bg-yellow-400 text-blue-900" : "bg-white/5 text-slate-300 hover:bg-white/10"}`}>
            {f.label}
          </button>
        ))}
      </div>

      {/* Match count */}
      <p className="text-slate-500 text-sm mb-6">{filtered.length} matches</p>

      {/* Matches by date */}
      <div className="space-y-10">
        {Object.entries(byDate).map(([date, matches]) => (
          <div key={date}>
            <div className="flex items-center gap-3 mb-4">
              <h2 className="text-white font-bold text-lg">{formatDate(date)}</h2>
              {date === today && (
                <span className="bg-green-500/20 text-green-400 text-xs px-2 py-0.5 rounded-full font-medium">Today</span>
              )}
              <span className="text-slate-600 text-sm">{matches.length} match{matches.length > 1 ? "es" : ""}</span>
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-3">
              {matches.map(m => <MatchCard key={m.match} match={m} />)}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
