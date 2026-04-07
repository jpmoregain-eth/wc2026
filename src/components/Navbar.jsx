import { Link, useLocation } from 'react-router-dom'
const links = [
  {to:"/",label:"Home"},{to:"/groups",label:"Groups"},
  {to:"/bracket",label:"Bracket"},{to:"/players",label:"Players"},
  { to: "/about", label: "About" },
  { to: "/predictions", label: "Predictions" },
  { to: "/schedule", label: "Schedule" },
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
