import { useState } from 'react'
import { Link } from 'react-router-dom'

const Navbar = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false)

  return (
    <nav className="bg-primary-700 text-white shadow-md">
      <div className="container mx-auto px-4">
        <div className="flex justify-between items-center py-4">
          <Link to="/" className="text-2xl font-bold">AI Content Creation</Link>
          
          {/* Mobile menu button */}
          <button 
            className="md:hidden"
            onClick={() => setIsMenuOpen(!isMenuOpen)}
          >
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className="h-6 w-6">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d={isMenuOpen ? "M6 18L18 6M6 6l12 12" : "M4 6h16M4 12h16M4 18h16"} />
            </svg>
          </button>
          
          {/* Desktop menu */}
          <div className="hidden md:flex space-x-6">
            <Link to="/" className="hover:text-primary-200 transition-colors">Home</Link>
            <Link to="/ad-generation" className="hover:text-primary-200 transition-colors">Ad Generation</Link>
            <Link to="/social-content" className="hover:text-primary-200 transition-colors">Social Content</Link>
            <Link to="/video-generation" className="hover:text-primary-200 transition-colors">Video Generation</Link>
          </div>
        </div>
        
        {/* Mobile menu */}
        {isMenuOpen && (
          <div className="md:hidden py-4 space-y-3">
            <Link to="/" className="block hover:text-primary-200 transition-colors">Home</Link>
            <Link to="/ad-generation" className="block hover:text-primary-200 transition-colors">Ad Generation</Link>
            <Link to="/social-content" className="block hover:text-primary-200 transition-colors">Social Content</Link>
            <Link to="/video-generation" className="block hover:text-primary-200 transition-colors">Video Generation</Link>
          </div>
        )}
      </div>
    </nav>
  )
}

export default Navbar
