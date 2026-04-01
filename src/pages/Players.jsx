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
