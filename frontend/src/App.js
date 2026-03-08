import React from 'react';
import { BrowserRouter, Routes, Route, useLocation } from 'react-router-dom';
import { AnimatePresence } from 'framer-motion';
import '@/App.css';
import Home from '@/pages/Home';
import Features from '@/pages/Features';
import About from '@/pages/About';
import LiveDashcam from '@/pages/LiveDashcam';
import Navbar from '@/components/Navbar';

const AnimatedRoutes = () => {
  const location = useLocation();

  return (
    <AnimatePresence mode="wait">
      <Routes location={location} key={location.pathname}>
        <Route path="/" element={<Home />} />
        <Route path="/live-dashcam" element={<LiveDashcam />} />
        <Route path="/features" element={<Features />} />
        <Route path="/about" element={<About />} />
      </Routes>
    </AnimatePresence>
  );
};

function App() {
  return (
    <div className="App min-h-screen text-slate-100 font-sans selection:bg-purple-500/30 selection:text-white">
      <BrowserRouter>
        <Navbar />
        <AnimatedRoutes />
      </BrowserRouter>
    </div>
  );
}

export default App;
