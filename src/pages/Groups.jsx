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
