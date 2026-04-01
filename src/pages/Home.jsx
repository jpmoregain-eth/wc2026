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
