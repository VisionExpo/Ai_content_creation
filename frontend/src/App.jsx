import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar'
import Footer from './components/Footer'
import Home from './pages/Home'
import AdGeneration from './pages/AdGeneration'
import SocialContent from './pages/SocialContent'
import VideoGeneration from './pages/VideoGeneration'

function App() {
  return (
    <Router>
      <div className="flex flex-col min-h-screen">
        <Navbar />
        <main className="flex-grow container mx-auto px-4 py-8">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/ad-generation" element={<AdGeneration />} />
            <Route path="/social-content" element={<SocialContent />} />
            <Route path="/video-generation" element={<VideoGeneration />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </Router>
  )
}

export default App
