#!/bin/bash
# Run this from inside ~/Downloads/wc2026
# chmod +x setup_wc2026.sh && ./setup_wc2026.sh

set -e
mkdir -p src/components src/pages src/data src/lib

echo "Writing tailwind config..."
cat > tailwind.config.js << 'EOF'
/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: { extend: { colors: { fifa: { blue: "#1a3c6e", gold: "#c9a84c" } } } },
  plugins: [],
}
EOF

echo "Writing CSS..."
cat > src/index.css << 'EOF'
@tailwind base;
@tailwind components;
@tailwind utilities;
body { background-color: #0f172a; color: #f1f5f9; }
EOF

echo "Writing Supabase client..."
cat > src/lib/supabase.js << 'EOF'
import { createClient } from '@supabase/supabase-js'
export const supabase = createClient(
  "https://ttjrzmegmpavhthrvrzb.supabase.co",
  "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InR0anJ6bWVnbXBhdmh0aHJ2cnpiIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzQwOTc3OTUsImV4cCI6MjA4OTY3Mzc5NX0.RlBDMFGDKr7Q2u5t9VTQ3Hgf-KtOCGCFoGcK3YRUO9Y"
)
EOF

echo "Writing group data..."
cat > src/data/groups.js << 'EOF'
export const GROUPS = {
  A:{teams:["Mexico","South Africa","South Korea","Czechia"]},
  B:{teams:["Canada","Bosnia & Herzegovina","Qatar","Switzerland"]},
  C:{teams:["Brazil","Morocco","Haiti","Scotland"]},
  D:{teams:["USA","Paraguay","Australia","Turkey"]},
  E:{teams:["Germany","Curaçao","Ivory Coast","Ecuador"]},
  F:{teams:["Netherlands","Japan","Sweden","Tunisia"]},
  G:{teams:["Belgium","Egypt","Iran","New Zealand"]},
  H:{teams:["Spain","Cape Verde","Saudi Arabia","Uruguay"]},
  I:{teams:["France","Senegal","Iraq","Norway"]},
  J:{teams:["Argentina","Algeria","Austria","Jordan"]},
  K:{teams:["Portugal","DR Congo","Uzbekistan","Colombia"]},
  L:{teams:["England","Croatia","Ghana","Panama"]},
}
export const FLAG_EMOJI = {
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
}
EOF

echo "Writing App.jsx..."
cat > src/App.jsx << 'EOF'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar'
import Home from './pages/Home'
import Groups from './pages/Groups'
import Bracket from './pages/Bracket'
import Players from './pages/Players'
export default function App() {
  return (
    <BrowserRouter>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/groups" element={<Groups />} />
        <Route path="/bracket" element={<Bracket />} />
        <Route path="/players" element={<Players />} />
      </Routes>
    </BrowserRouter>
  )
}
EOF

echo "Writing Navbar..."
cat > src/components/Navbar.jsx << 'EOF'
import { Link, useLocation } from 'react-router-dom'
const links = [
  {to:"/",label:"Home"},{to:"/groups",label:"Groups"},
  {to:"/bracket",label:"Bracket"},{to:"/players",label:"Players"},
]
export default function Navbar() {
  const { pathname } = useLocation()
  return (
    <nav className="bg-[#1a3c6e] border-b border-yellow-600/30 sticky top-0 z-50">
      <div className="max-w-6xl mx-auto px-4 flex items-center justify-between h-14">
        <Link to="/" className="font-bold text-yellow-400 text-lg tracking-wide">⚽ WC 2026</Link>
        <div className="flex gap-1">
          {links.map(l => (
            <Link key={l.to} to={l.to}
              className={`px-3 py-1.5 rounded text-sm font-medium transition-colors
                ${pathname===l.to ? "bg-yellow-400 text-blue-900" : "text-slate-300 hover:text-white hover:bg-white/10"}`}>
              {l.label}
            </Link>
          ))}
        </div>
      </div>
    </nav>
  )
}
EOF

echo "Writing Home page..."
cat > src/pages/Home.jsx << 'EOF'
import { useEffect, useState } from "react"
import { Link } from "react-router-dom"
import { GROUPS, FLAG_EMOJI } from "../data/groups"

function useCountdown(target) {
  const [t, setT] = useState({})
  useEffect(() => {
    const calc = () => {
      const diff = new Date(target) - new Date()
      if (diff <= 0) return setT({days:0,hours:0,minutes:0,seconds:0})
      setT({days:Math.floor(diff/86400000),hours:Math.floor((diff%86400000)/3600000),
            minutes:Math.floor((diff%3600000)/60000),seconds:Math.floor((diff%60000)/1000)})
    }
    calc(); const id = setInterval(calc, 1000); return () => clearInterval(id)
  }, [target])
  return t
}

function Box({value,label}) {
  return (
    <div className="flex flex-col items-center bg-white/5 border border-yellow-500/20 rounded-xl px-6 py-4 min-w-[80px]">
      <span className="text-4xl font-bold text-yellow-400 tabular-nums">{String(value??0).padStart(2,"0")}</span>
      <span className="text-xs text-slate-400 mt-1 uppercase tracking-widest">{label}</span>
    </div>
  )
}

export default function Home() {
  const t = useCountdown("2026-06-11T20:00:00Z")
  return (
    <div className="max-w-6xl mx-auto px-4 py-10">
      <div className="text-center mb-14">
        <p className="text-yellow-400 text-sm uppercase tracking-widest mb-3">FIFA World Cup</p>
        <h1 className="text-5xl md:text-7xl font-extrabold text-white mb-2">USA · Canada · Mexico</h1>
        <p className="text-slate-400 text-lg mb-8">June 11 – July 19, 2026 · 48 Teams · 104 Matches</p>
        <div className="flex justify-center gap-3 flex-wrap">
          <Box value={t.days} label="Days" />
          <Box value={t.hours} label="Hours" />
          <Box value={t.minutes} label="Mins" />
          <Box value={t.seconds} label="Secs" />
        </div>
        <p className="text-slate-500 text-sm mt-3">Until opening kick-off · Mexico City</p>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-14">
        {[
          {to:"/groups",icon:"🏆",title:"Group Stage",desc:"12 groups · 48 teams · standings"},
          {to:"/bracket",icon:"📊",title:"Bracket",desc:"Round of 32 through to the Final"},
          {to:"/players",icon:"⚽",title:"Player Stats",desc:"xG, assists, tackles & more"},
        ].map(c => (
          <Link key={c.to} to={c.to}
            className="bg-white/5 hover:bg-white/10 border border-white/10 hover:border-yellow-500/40 rounded-xl p-6 transition-all group">
            <div className="text-3xl mb-3">{c.icon}</div>
            <div className="font-semibold text-white group-hover:text-yellow-400 transition-colors">{c.title}</div>
            <div className="text-sm text-slate-400 mt-1">{c.desc}</div>
          </Link>
        ))}
      </div>
      <h2 className="text-xl font-bold text-white mb-4">Group Stage Draw</h2>
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-3">
        {Object.entries(GROUPS).map(([letter,{teams}]) => (
          <Link key={letter} to="/groups"
            className="bg-white/5 hover:bg-white/10 border border-white/10 rounded-lg p-3 transition-all">
            <div className="text-yellow-400 font-bold text-sm mb-2">Group {letter}</div>
            {teams.map(t => (
              <div key={t} className="text-slate-300 text-xs py-0.5 flex items-center gap-1.5">
                <span>{FLAG_EMOJI[t]}</span><span>{t}</span>
              </div>
            ))}
          </Link>
        ))}
      </div>
    </div>
  )
}
EOF

echo "Writing Groups page..."
cat > src/pages/Groups.jsx << 'EOF'
import { GROUPS, FLAG_EMOJI } from "../data/groups"
function GroupTable({letter,teams}) {
  return (
    <div className="bg-white/5 border border-white/10 rounded-xl overflow-hidden">
      <div className="bg-[#1a3c6e] px-4 py-2.5 flex items-center gap-2">
        <span className="bg-yellow-400 text-blue-900 font-extrabold text-sm w-7 h-7 rounded flex items-center justify-center">{letter}</span>
        <span className="text-white font-semibold text-sm">Group {letter}</span>
      </div>
      <table className="w-full text-xs">
        <thead>
          <tr className="text-slate-500 border-b border-white/5">
            <th className="text-left px-3 py-2">Team</th>
            <th className="px-2 py-2">P</th><th className="px-2 py-2">W</th>
            <th className="px-2 py-2">D</th><th className="px-2 py-2">L</th>
            <th className="px-2 py-2">GD</th><th className="px-2 py-2">Pts</th>
          </tr>
        </thead>
        <tbody>
          {teams.map((t,i) => (
            <tr key={t} className={`border-b border-white/5 last:border-0 hover:bg-white/5 ${i<2?"border-l-2 border-l-green-500":""}`}>
              <td className="px-3 py-2.5 flex items-center gap-2">
                <span className="text-base">{FLAG_EMOJI[t]}</span>
                <span className="text-slate-200 font-medium">{t}</span>
              </td>
              {[0,0,0,0,0,0].map((v,j) => (
                <td key={j} className={`text-center px-2 py-2.5 ${j===5?"text-white font-bold":"text-slate-400"}`}>{v}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
      <div className="px-3 py-1.5 text-slate-600 text-xs border-t border-white/5">
        <span className="inline-block w-2 h-2 bg-green-500 rounded-sm mr-1"/>Top 2 advance
      </div>
    </div>
  )
}
export default function Groups() {
  return (
    <div className="max-w-6xl mx-auto px-4 py-10">
      <h1 className="text-3xl font-extrabold text-white mb-2">Group Stage</h1>
      <p className="text-slate-400 mb-8">12 groups · Standings update once matches begin June 11</p>
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-5">
        {Object.entries(GROUPS).map(([letter,{teams}]) => (
          <GroupTable key={letter} letter={letter} teams={teams} />
        ))}
      </div>
    </div>
  )
}
EOF

echo "Writing Bracket page..."
cat > src/pages/Bracket.jsx << 'EOF'
const TBD = "TBD"
function Match({home=TBD,away=TBD}) {
  return (
    <div className="bg-white/5 border border-white/10 rounded-lg overflow-hidden w-40">
      <div className="px-3 py-1.5 text-slate-300 text-xs border-b border-white/5">{home}</div>
      <div className="px-3 py-1.5 text-slate-300 text-xs">{away}</div>
    </div>
  )
}
function Round({title,count}) {
  return (
    <div className="flex flex-col gap-2 items-center">
      <h3 className="text-yellow-400 font-bold text-xs text-center mb-2 whitespace-nowrap">{title}</h3>
      <div className="flex flex-col gap-3">
        {Array(count).fill(0).map((_,i) => <Match key={i}/>)}
      </div>
    </div>
  )
}
export default function Bracket() {
  return (
    <div className="max-w-full px-4 py-10">
      <h1 className="text-3xl font-extrabold text-white mb-2 max-w-6xl mx-auto">Tournament Bracket</h1>
      <p className="text-slate-400 mb-8 max-w-6xl mx-auto">Knockout stage begins after group stage · Fills in as teams advance</p>
      <div className="overflow-x-auto pb-8">
        <div className="flex gap-6 items-center w-fit mx-auto">
          <Round title="Round of 32" count={8}/>
          <Round title="Round of 16" count={4}/>
          <Round title="Quarters" count={2}/>
          <Round title="Semis" count={1}/>
          <div className="flex flex-col items-center gap-2">
            <h3 className="text-yellow-400 font-bold text-xs mb-2">🏆 Final</h3>
            <Match/>
          </div>
          <Round title="Semis" count={1}/>
          <Round title="Quarters" count={2}/>
          <Round title="Round of 16" count={4}/>
          <Round title="Round of 32" count={8}/>
        </div>
      </div>
      <p className="text-center text-slate-500 text-sm mt-4">Final: July 19 · MetLife Stadium, East Rutherford NJ</p>
    </div>
  )
}
EOF

echo "Writing Players page..."
cat > src/pages/Players.jsx << 'EOF'
import { useEffect, useState } from "react"
import { supabase } from "../lib/supabase"
const NATION_NAMES = {
  ENG:"England",FRA:"France",ESP:"Spain",GER:"Germany",POR:"Portugal",
  NED:"Netherlands",BEL:"Belgium",CRO:"Croatia",SUI:"Switzerland",AUT:"Austria",
  SCO:"Scotland",NOR:"Norway",SWE:"Sweden",TUR:"Turkey",BIH:"Bosnia",
  CZE:"Czechia",BRA:"Brazil",ARG:"Argentina",COL:"Colombia",URU:"Uruguay",
  ECU:"Ecuador",PAR:"Paraguay",USA:"USA",MEX:"Mexico",CAN:"Canada",
  PAN:"Panama",CUW:"Curaçao",HAI:"Haiti",JPN:"Japan",KOR:"S.Korea",
  AUS:"Australia",KSA:"Saudi Arabia",IRN:"Iran",QAT:"Qatar",JOR:"Jordan",
  UZB:"Uzbekistan",IRQ:"Iraq",MAR:"Morocco",SEN:"Senegal",NGA:"Nigeria",
  CMR:"Cameroon",EGY:"Egypt",CIV:"Ivory Coast",CPV:"Cape Verde",COD:"DR Congo",
  RSA:"South Africa",GHA:"Ghana",NZL:"New Zealand",ALG:"Algeria",TUN:"Tunisia",
}
export default function Players() {
  const [players, setPlayers] = useState([])
  const [loading, setLoading] = useState(true)
  const [search, setSearch] = useState("")
  const [nation, setNation] = useState("All")
  const [sortBy, setSortBy] = useState("xg")
  const [page, setPage] = useState(0)
  const PER = 50

  useEffect(() => {
    setLoading(true)
    let q = supabase.from("wc2026_players")
      .select("player,nation,squad,position,minutes,goals,assists,xg,xa,progressive_passes")
      .order(sortBy,{ascending:false}).range(page*PER,(page+1)*PER-1)
    if (nation!=="All") q = q.eq("nation",nation)
    if (search) q = q.ilike("player",`%${search}%`)
    q.then(({data,error}) => { if(!error) setPlayers(data||[]); setLoading(false) })
  }, [nation,sortBy,search,page])

  return (
    <div className="max-w-6xl mx-auto px-4 py-10">
      <h1 className="text-3xl font-extrabold text-white mb-2">Player Stats</h1>
      <p className="text-slate-400 mb-6">2025–26 club season · WC 2026 nations only</p>
      <div className="flex flex-wrap gap-3 mb-6">
        <input value={search} onChange={e=>{setSearch(e.target.value);setPage(0)}}
          placeholder="Search player..." className="bg-white/5 border border-white/10 rounded-lg px-3 py-2 text-sm text-white placeholder-slate-500 focus:outline-none w-44"/>
        <select value={nation} onChange={e=>{setNation(e.target.value);setPage(0)}}
          className="bg-white/5 border border-white/10 rounded-lg px-3 py-2 text-sm text-white">
          <option value="All" className="bg-slate-800">All Nations</option>
          {Object.entries(NATION_NAMES).map(([k,v])=><option key={k} value={k} className="bg-slate-800">{v}</option>)}
        </select>
        <select value={sortBy} onChange={e=>{setSortBy(e.target.value);setPage(0)}}
          className="bg-white/5 border border-white/10 rounded-lg px-3 py-2 text-sm text-white">
          {["xg","goals","assists","xa","progressive_passes","minutes"].map(s=>(
            <option key={s} value={s} className="bg-slate-800">Sort: {s}</option>
          ))}
        </select>
      </div>
      {loading ? <div className="text-center py-20 text-slate-400">Loading...</div> : (
        <>
          <div className="overflow-x-auto rounded-xl border border-white/10">
            <table className="w-full text-sm">
              <thead>
                <tr className="bg-white/5 text-slate-400 text-xs uppercase">
                  <th className="text-left px-4 py-3">#</th>
                  <th className="text-left px-4 py-3">Player</th>
                  <th className="text-left px-4 py-3">Nation</th>
                  <th className="text-left px-4 py-3">Club</th>
                  <th className="px-4 py-3">Pos</th>
                  <th className="px-4 py-3">Min</th>
                  <th className="px-4 py-3">Gls</th>
                  <th className="px-4 py-3">Ast</th>
                  <th className="px-4 py-3">xG</th>
                  <th className="px-4 py-3">xA</th>
                </tr>
              </thead>
              <tbody>
                {players.map((p,i)=>(
                  <tr key={i} className="border-t border-white/5 hover:bg-white/5">
                    <td className="px-4 py-3 text-slate-500">{page*PER+i+1}</td>
                    <td className="px-4 py-3 font-medium text-white">{p.player}</td>
                    <td className="px-4 py-3"><span className="text-xs bg-blue-900/50 text-yellow-400 px-2 py-0.5 rounded font-mono">{p.nation}</span></td>
                    <td className="px-4 py-3 text-slate-400 text-xs">{p.squad}</td>
                    <td className="px-4 py-3 text-center text-slate-400 text-xs">{p.position}</td>
                    <td className="px-4 py-3 text-center text-slate-300">{p.minutes?Math.round(p.minutes):"-"}</td>
                    <td className="px-4 py-3 text-center text-white font-semibold">{p.goals??"-"}</td>
                    <td className="px-4 py-3 text-center text-slate-300">{p.assists??"-"}</td>
                    <td className="px-4 py-3 text-center text-yellow-400 font-semibold">{p.xg?.toFixed(1)??"-"}</td>
                    <td className="px-4 py-3 text-center text-slate-300">{p.xa?.toFixed(1)??"-"}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <div className="flex justify-between mt-4">
            <button onClick={()=>setPage(p=>Math.max(0,p-1))} disabled={page===0}
              className="px-4 py-2 bg-white/5 border border-white/10 rounded-lg text-sm text-slate-300 hover:bg-white/10 disabled:opacity-30">← Prev</button>
            <span className="text-slate-400 text-sm self-center">Page {page+1}</span>
            <button onClick={()=>setPage(p=>p+1)} disabled={players.length<PER}
              className="px-4 py-2 bg-white/5 border border-white/10 rounded-lg text-sm text-slate-300 hover:bg-white/10 disabled:opacity-30">Next →</button>
          </div>
        </>
      )}
    </div>
  )
}
EOF

echo ""
echo "✅ All files written! Now run:"
echo "   npm run dev"
