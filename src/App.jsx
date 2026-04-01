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
