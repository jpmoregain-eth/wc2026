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
