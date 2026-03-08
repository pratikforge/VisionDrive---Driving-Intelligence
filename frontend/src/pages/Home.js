import React from 'react';
import axios from 'axios';
import { motion } from 'framer-motion';
import { useCounter } from '@/hooks/useScrollReveal';
import FloatingParticles from '@/components/FloatingParticles';
import BackgroundPattern from '@/components/BackgroundPattern';

const BACKEND_URL = "http://127.0.0.1:8000";
const API = `${BACKEND_URL}/api`;

/* ─── Framer Motion variants ─── */
const fadeUp = {
  hidden: { opacity: 0, y: 30 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.8, ease: [0.16, 1, 0.3, 1] } }
};

const fadeLeft = {
  hidden: { opacity: 0, x: -40 },
  visible: { opacity: 1, x: 0, transition: { duration: 0.8, ease: [0.16, 1, 0.3, 1] } }
};

const fadeRight = {
  hidden: { opacity: 0, x: 40 },
  visible: { opacity: 1, x: 0, transition: { duration: 0.8, ease: [0.16, 1, 0.3, 1] } }
};

const scaleUp = {
  hidden: { opacity: 0, scale: 0.9 },
  visible: { opacity: 1, scale: 1, transition: { duration: 0.8, ease: [0.16, 1, 0.3, 1] } }
};

/* ─── Animated stat counter ─── */
const StatCounter = ({ value, label }) => {
  const numericPart = parseInt(value, 10) || 0;
  const suffix = value.replace(/[\d]/g, '');
  const prefix = value.startsWith('<') ? '<' : '';
  const count = useCounter(numericPart, 1800, true);

  return (
    <motion.div variants={fadeUp} className="text-center">
      <div className="text-4xl md:text-5xl font-bold text-white tracking-tight mb-2">
        {numericPart > 0 ? `${prefix}${count}${suffix}` : value}
      </div>
      <div className="text-white/50 text-sm uppercase tracking-widest">{label}</div>
    </motion.div>
  );
};

const Home = () => {
  const handleOpenApp = async () => {
    try {
      const response = await axios.post(`${API}/launch-engine`);
      alert(response.data.message);
    } catch (error) {
      console.error('Failed to launch engine:', error);
      alert('Failed to launch VisionDrive engine. Please ensure the engine is properly configured.');
    }
  };

  return (
    <div className="gradient-bg" data-testid="home-page">
      <FloatingParticles />
      <BackgroundPattern />

      {/* ─── Hero Section ─── */}
      <section className="min-h-screen flex items-center justify-center px-6 pt-32 pb-16 relative z-10 overflow-hidden">
        <div className="max-w-7xl mx-auto w-full relative">
          <div className="grid md:grid-cols-2 gap-12 items-center">

            <motion.div initial="hidden" animate="visible" variants={fadeLeft} className="space-y-8 relative z-20">
              <div className="space-y-6">
                <motion.div
                  initial={{ opacity: 0, scale: 0.8 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ delay: 0.2 }}
                  className="inline-flex items-center bg-white/5 border border-white/10 backdrop-blur-md rounded-full px-5 py-2 mb-2 shadow-[0_0_20px_rgba(255,255,255,0.05)]"
                >
                  <span className="w-2.5 h-2.5 bg-green-400 rounded-full mr-3 live-dot shadow-[0_0_10px_#4ade80]"></span>
                  <span className="text-white/90 text-sm font-semibold tracking-wide">SYSTEM ONLINE</span>
                </motion.div>
                <h1 className="text-6xl md:text-[5.5rem] font-bold leading-[1.1] tracking-tight" data-testid="hero-heading">
                  <span className="text-white">Experience</span>
                  <br />
                  <span className="text-transparent bg-clip-text bg-gradient-to-r from-orange-400 via-purple-500 to-blue-500 animate-gradient-x">VisionDrive</span>
                </h1>
                <p className="text-2xl text-white/80 font-medium tracking-wide" data-testid="hero-subheading">
                  We don't drive the car — we understand the incident.
                </p>
                <p className="text-lg text-white/50 max-w-lg leading-relaxed">
                  Next-generation AR navigation with sub-50ms object detection,
                  risk fusion, and immutable black-box recording.
                </p>
              </div>

              <div className="flex items-center space-x-6">
                <button
                  onClick={handleOpenApp}
                  className="group relative px-8 py-4 bg-white text-black rounded-full font-bold text-lg overflow-hidden transition-transform hover:scale-105"
                  data-testid="open-app-button"
                >
                  <div className="absolute inset-0 w-full h-full bg-gradient-to-r from-orange-400 via-purple-500 to-blue-500 opacity-0 group-hover:opacity-10 transition-opacity"></div>
                  <span className="relative flex items-center space-x-2">
                    <span>Initialize Core</span>
                    <svg className="w-5 h-5 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
                    </svg>
                  </span>
                </button>
                <a href="#architecture" className="text-white/70 hover:text-white font-medium transition-colors flex items-center space-x-2">
                  <span>View Architecture</span>
                  <span>↓</span>
                </a>
              </div>
            </motion.div>

            <motion.div initial="hidden" animate="visible" variants={fadeRight} className="relative z-10">
              <div className="relative">
                {/* Decorative glow behind image */}
                <div className="absolute inset-0 bg-gradient-to-tr from-purple-500/30 to-blue-500/30 blur-[100px] rounded-full scale-110"></div>

                <div className="glass-card p-2 rounded-[2rem] relative z-10 border border-white/10 shadow-[0_0_50px_rgba(0,0,0,0.5)] float">
                  <div className="overflow-hidden rounded-[1.5rem] relative">
                    <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent z-10"></div>
                    <img
                      src="/ar-hero.jpg"
                      alt="VisionDrive AR Navigation HUD"
                      className="w-full h-auto object-cover transform scale-105 hover:scale-100 transition-transform duration-700"
                    />

                    {/* HUD Elements Overlay */}
                    <div className="absolute top-6 left-6 z-20 flex items-center space-x-2">
                      <span className="px-3 py-1 bg-red-500/20 border border-red-500/50 text-red-400 rounded-md text-xs font-mono backdrop-blur-md">REC [00:42:15]</span>
                    </div>
                    <div className="absolute top-6 right-6 z-20 bg-black/40 backdrop-blur-md border border-white/10 rounded-lg px-4 py-2 flex items-center space-x-3">
                      <div className="w-2 h-2 rounded-full bg-green-400 live-dot"></div>
                      <span className="text-white text-sm font-mono tracking-widest">FPS: 45</span>
                    </div>
                    <div className="absolute bottom-6 left-6 right-6 z-20 flex justify-between items-end">
                      <div className="bg-black/40 backdrop-blur-md border border-white/10 rounded-xl p-4 max-w-[200px]">
                        <div className="text-orange-400 text-xs font-mono mb-1">WARNING</div>
                        <div className="text-white text-sm font-semibold">Pedestrian 12m</div>
                      </div>
                      <div className="text-white/50 font-mono text-xs">
                        SYS.V1.4.2_STABLE
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </motion.div>

          </div>
        </div>
      </section>

      {/* ─── Stats Bar ─── */}
      <section className="py-12 border-y border-white/5 bg-white/[0.02] relative z-10 backdrop-blur-sm" id="architecture">
        <div className="max-w-7xl mx-auto px-6">
          <motion.div
            initial="hidden" whileInView="visible" viewport={{ once: true, margin: "-100px" }}
            variants={{
              visible: { transition: { staggerChildren: 0.1 } }
            }}
            className="grid grid-cols-2 md:grid-cols-4 gap-8 divide-x divide-white/5"
          >
            <StatCounter value="25+" label="Object Classes" />
            <StatCounter value="<50ms" label="Inference Time" />
            <StatCounter value="YOLOv8" label="Core Engine" />
            <StatCounter value="24/7" label="Immutable Logging" />
          </motion.div>
        </div>
      </section>

      {/* ─── Feature Highlights ─── */}
      <section className="py-32 px-6 relative z-10">
        <div className="max-w-7xl mx-auto">
          <motion.div initial="hidden" whileInView="visible" viewport={{ once: true }} variants={fadeUp} className="text-center mb-20">
            <div className="text-purple-400 font-mono text-sm tracking-widest mb-4 uppercase">System Architecture</div>
            <h2 className="text-5xl md:text-6xl font-bold text-white mb-6">Designed For <span className="text-transparent bg-clip-text bg-gradient-to-r from-orange-400 to-red-500">Certainty</span></h2>
            <p className="text-xl text-white/50 max-w-2xl mx-auto">
              Three synchronized subsystems operating perfectly in parallel.
            </p>
          </motion.div>

          <motion.div
            initial="hidden" whileInView="visible" viewport={{ once: true }}
            variants={{ visible: { transition: { staggerChildren: 0.2 } } }}
            className="grid md:grid-cols-3 gap-8"
          >
            {[
              {
                icon: <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" /></svg>,
                title: 'AR Holographic HUD',
                desc: 'Real-time lane detection and navigation arrows projected perfectly onto the spatial feed. Turn guidance and distance counters at sub-millimeter precision.',
                glow: 'group-hover:shadow-[0_0_40px_rgba(249,115,22,0.3)]',
                iconColor: 'text-orange-400',
              },
              {
                icon: <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M12 9v2m0 4h.01M12 3a9 9 0 100 18 9 9 0 000-18z" /></svg>,
                title: 'Risk Fusion Engine',
                desc: 'Multi-variable risk scoring combining tensor distance, velocity, and class hierarchy. Instant deterministic alerts for volatile path factors.',
                glow: 'group-hover:shadow-[0_0_40px_rgba(168,85,247,0.3)]',
                iconColor: 'text-purple-400',
              },
              {
                icon: <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M4 7v10c0 2 1 3 3 3h10c2 0 3-1 3-3V7c0-2-1-3-3-3H7C5 4 4 5 4 7zM12 11v3M12 8h.01" /></svg>,
                title: 'Immutable Black Box',
                desc: 'Rolling buffer architecture saving crucial incident frames. Hardware-level physical lock on airbag deployment ensures cryptographic integrity.',
                glow: 'group-hover:shadow-[0_0_40px_rgba(59,130,246,0.3)]',
                iconColor: 'text-blue-400',
              },
            ].map((f, i) => (
              <motion.div key={i} variants={scaleUp} className={`glass-card p-8 rounded-3xl transition-all duration-500 group ${f.glow} border border-white/5`}>
                <div className={`w-14 h-14 rounded-2xl bg-white/5 border border-white/10 flex items-center justify-center mb-6 shadow-inner ${f.iconColor}`}>
                  {f.icon}
                </div>
                <h3 className="text-2xl font-bold text-white mb-4 tracking-tight">{f.title}</h3>
                <p className="text-white/60 leading-relaxed font-medium">{f.desc}</p>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* ─── Emergency Feature Banner ─── */}
      <section className="py-24 px-6 relative z-10">
        <div className="max-w-5xl mx-auto">
          <motion.div initial="hidden" whileInView="visible" viewport={{ once: true }} variants={scaleUp}>
            <div className="glass-card p-12 rounded-[2.5rem] relative overflow-hidden border border-red-500/20 shadow-[0_0_60px_rgba(239,68,68,0.15)] bg-gradient-to-r from-red-950/40 to-black">
              {/* Rotating radar glow effect */}
              <div className="absolute top-1/2 right-1/4 w-[800px] h-[800px] bg-red-500/10 rounded-full blur-[100px] -translate-y-1/2 animate-pulse"></div>

              <div className="relative z-10 grid md:grid-cols-2 gap-16 items-center">
                <div>
                  <div className="inline-flex items-center bg-red-500/10 border border-red-500/30 rounded-full px-4 py-1.5 mb-6">
                    <span className="w-2 h-2 rounded-full bg-red-500 animate-ping mr-3"></span>
                    <span className="text-red-400 text-sm font-bold tracking-widest uppercase">Critical Override</span>
                  </div>
                  <h3 className="text-4xl lg:text-5xl font-bold text-white mb-6 leading-tight">Airbag Trigger<br />Protocol</h3>
                  <p className="text-white/60 text-lg leading-relaxed mb-8">
                    Millisecond detection of airbag deployment triggers total system lockdown.
                    Black-box shards are encrypted, written to permanent storage, and emergency services are dialed via bridge.
                  </p>
                </div>
                <div className="space-y-6">
                  {[
                    { step: '01', text: 'Deployment detected via telemetry hook' },
                    { step: '02', text: 'Rolling buffer locked into read-only mode' },
                    { step: '03', text: 'Bridge established to emergency 112 protocol' },
                    { step: '04', text: 'GPS & Telemetry log offloaded to authorities' },
                  ].map((s, i) => (
                    <motion.div
                      key={i}
                      variants={fadeLeft}
                      className="flex items-center space-x-5 bg-black/40 border border-white/5 p-4 rounded-2xl"
                    >
                      <span className="bg-red-500/20 text-red-400 font-mono font-bold text-sm px-3 py-1 rounded-lg">{s.step}</span>
                      <p className="text-white/80 font-medium">{s.text}</p>
                    </motion.div>
                  ))}
                </div>
              </div>
            </div>
          </motion.div>
        </div>
      </section>

      {/* ─── Tech Stack ─── */}
      <section className="py-24 px-6 relative z-10">
        <div className="max-w-7xl mx-auto text-center">
          <motion.div initial="hidden" whileInView="visible" viewport={{ once: true }} variants={fadeUp}>
            <div className="text-blue-400 font-mono text-sm tracking-widest mb-4 uppercase">Infrastructure</div>
            <h2 className="text-4xl md:text-5xl font-bold text-white mb-16">Engineered Foundation</h2>
          </motion.div>

          <motion.div
            initial="hidden" whileInView="visible" viewport={{ once: true }}
            variants={{ visible: { transition: { staggerChildren: 0.1 } } }}
            className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-6"
          >
            {[
              { name: 'YOLOv8', sub: 'Neural Engine' },
              { name: 'FastAPI', sub: 'High-Performance API' },
              { name: 'React', sub: 'UI Subsystem' },
              { name: 'NumPy', sub: 'Tensor Math' },
              { name: 'OpenCV', sub: 'Spatial Vision' },
              { name: 'MongoDB', sub: 'Event Logging' },
            ].map((tech, i) => (
              <motion.div
                key={i}
                variants={scaleUp}
                className="glass-card p-6 rounded-2xl hover:border-white/20 transition-colors group cursor-default"
              >
                <div className="text-white font-bold text-lg mb-1 group-hover:text-transparent group-hover:bg-clip-text group-hover:bg-gradient-to-r group-hover:from-blue-400 group-hover:to-purple-500 transition-colors">{tech.name}</div>
                <div className="text-white/40 text-xs font-mono uppercase tracking-wider">{tech.sub}</div>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* ─── Footer ─── */}
      <footer className="py-12 px-6 border-t border-white/5 bg-black/50 backdrop-blur-md relative z-10 mt-20">
        <div className="max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-center space-y-6 md:space-y-0">
          <div className="flex items-center space-x-4">
            <img src="/logo.jpg" alt="VisionDrive Logo" className="w-10 h-10 object-contain rounded-xl grayscale opacity-80" />
            <span className="text-white/90 font-bold tracking-widest text-lg">VISIONDRIVE_</span>
          </div>
          <p className="text-white/30 text-sm font-mono uppercase tracking-widest">© 2026 Core Systems Offline</p>
          <div className="flex space-x-8">
            <a href="/features" className="text-white/50 hover:text-white font-mono text-xs tracking-widest uppercase transition-colors hover:glow">Documentation</a>
            <a href="/about" className="text-white/50 hover:text-white font-mono text-xs tracking-widest uppercase transition-colors hover:glow">About Node</a>
          </div>
        </div>
      </footer>

    </div>
  );
};

export default Home;
