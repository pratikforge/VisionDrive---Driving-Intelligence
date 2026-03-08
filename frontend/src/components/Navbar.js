import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const Navbar = () => {
  const navigate = useNavigate();

  const handleLaunchEngine = async () => {
    try {
      const response = await axios.post(`${API}/launch-engine`);
      alert(response.data.message);
    } catch (error) {
      console.error('Failed to launch engine:', error);
      alert('Failed to launch VisionDrive engine. Please ensure the engine is properly configured.');
    }
  };

  return (
    <nav className="fixed top-6 left-1/2 -translate-x-1/2 w-[95%] max-w-7xl z-50 bg-black/40 backdrop-blur-xl border border-white/10 rounded-full shadow-[0_8px_32px_rgba(0,0,0,0.5)]">
      <div className="px-6 py-3">
        <div className="flex items-center justify-between">
          {/* Logo */}
          <Link to="/" className="flex items-center space-x-3" data-testid="logo-link">
            <img src="/logo.jpg" alt="VisionDrive Logo" className="w-12 h-12 object-contain rounded-lg shadow-lg" />
            <span className="text-white font-semibold text-xl tracking-wide">VisionDrive</span>
          </Link>

          {/* Navigation Links */}
          <div className="flex items-center space-x-8">
            <Link
              to="/live-dashcam"
              className="text-white/90 hover:text-white transition-colors duration-200 font-medium flex items-center space-x-1"
              data-testid="nav-dashcam"
            >
              <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                <circle cx="12" cy="12" r="4" />
                <path d="M12 2a10 10 0 100 20 10 10 0 000-20zm0 2a8 8 0 110 16 8 8 0 010-16z" opacity="0.3" />
              </svg>
              <span>Live Dashcam</span>
            </Link>
            <Link
              to="/features"
              className="text-white/90 hover:text-white transition-colors duration-200 font-medium"
              data-testid="nav-features"
            >
              Features
            </Link>
            <Link
              to="/about"
              className="text-white/90 hover:text-white transition-colors duration-200 font-medium"
              data-testid="nav-about"
            >
              About
            </Link>

            {/* Start Button */}
            <button
              onClick={handleLaunchEngine}
              className="btn-gradient-purple text-white px-6 py-2.5 rounded-full font-semibold shadow-lg"
              data-testid="nav-start-button"
            >
              Start
            </button>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
