import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar'
import Home from './pages/Home'
import Groups from './pages/Groups'
import Bracket from './pages/Bracket'
import Players from './pages/Players'
import Privacy from './pages/Privacy'
import About from './pages/About'
import Predictions from './pages/Predictions'
import Schedule from './pages/Schedule'
export default function App() {
  return (
    <BrowserRouter>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/groups" element={<Groups />} />
        <Route path="/bracket" element={<Bracket />} />
        <Route path="/players" element={<Players />} />
	<Route path="/privacy" element={<Privacy />} />
	<Route path="/about" element={<About />} />
	<Route path="/predictions" element={<Predictions />} />
	<Route path="/schedule" element={<Schedule />} />
      </Routes>
	<footer className="text-center py-6 text-slate-600 text-xs border-t border-white/5 mt-10">
  <a href="/privacy" className="hover:text-slate-400">Privacy Policy</a>
  {" · "}
  <a href="/about" className="hover:text-slate:400">About</a>
  {" · "}
  Not affiliated with FIFA
	</footer>	
    </BrowserRouter>
  )
}
