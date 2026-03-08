import React from 'react';
import { motion } from 'framer-motion';
import FloatingParticles from '@/components/FloatingParticles';
import BackgroundPattern from '@/components/BackgroundPattern';

/* ─── Framer Motion Variants ─── */
const fadeUp = {
  hidden: { opacity: 0, y: 30 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.8, ease: [0.16, 1, 0.3, 1] } }
};

const staggerContainer = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.15
    }
  }
};

const fadeRight = {
  hidden: { opacity: 0, x: -30 },
  visible: { opacity: 1, x: 0, transition: { duration: 0.6, ease: [0.16, 1, 0.3, 1] } }
};

const scaleUp = {
  hidden: { opacity: 0, scale: 0.95 },
  visible: { opacity: 1, scale: 1, transition: { duration: 0.6, ease: [0.16, 1, 0.3, 1] } }
};

const About = () => {
  return (
    <div className="gradient-bg" data-testid="about-page">
      <FloatingParticles />
      <BackgroundPattern />

      {/* ─── Header ─── */}
      <section className="pt-32 pb-16 px-6 relative z-10">
        <motion.div initial="hidden" animate="visible" variants={fadeUp} className="max-w-4xl mx-auto text-center">
          <div className="inline-flex items-center bg-black/40 border border-white/5 backdrop-blur-md rounded-full px-5 py-2 mb-8 shadow-inner">
            <span className="w-2 h-2 bg-blue-500 rounded-full mr-3 animate-pulse shadow-[0_0_10px_#3b82f6]"></span>
            <span className="text-blue-400 text-sm font-bold tracking-widest uppercase">System Architecture Overview</span>
          </div>
          <h1 className="text-5xl md:text-7xl font-bold mb-6 tracking-tight" data-testid="about-heading">
            <span className="text-white">Project </span>
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-500">VisionDrive</span>
          </h1>
          <p className="text-xl text-white/50 max-w-3xl mx-auto leading-relaxed font-medium">
            Building the next generation of spatial intelligence for vehicles. Combining neural-network risk fusion, augmented reality telemetrics, and immutable event logging.
          </p>
        </motion.div>
      </section>

      {/* ─── Mission Card ─── */}
      <section className="pb-20 px-6 relative z-10">
        <div className="max-w-6xl mx-auto">
          <motion.div initial="hidden" whileInView="visible" viewport={{ once: true }} variants={scaleUp}>
            <div className="bg-black/40 border border-white/5 backdrop-blur-md p-10 md:p-14 rounded-[2rem] shadow-2xl relative overflow-hidden group hover:border-blue-500/20 transition-colors duration-500">
              {/* Decorative grid lines */}
              <div className="absolute inset-0 bg-[linear-gradient(rgba(255,255,255,0.02)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.02)_1px,transparent_1px)] bg-[size:30px_30px] pointer-events-none opacity-0 group-hover:opacity-100 transition-opacity duration-700"></div>

              <div className="grid md:grid-cols-2 gap-12 relative z-10">
                <div className="space-y-6">
                  <div className="flex items-center space-x-3 mb-2">
                    <svg className="w-6 h-6 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" /></svg>
                    <h2 className="text-3xl font-bold text-white tracking-wide">Core Objective</h2>
                  </div>
                  <p className="text-white/70 text-lg leading-relaxed font-light" data-testid="about-description">
                    Utilizing state-of-the-art computer vision models like YOLOv8 to democratize advanced driver-assistance systems. We transform standard optical hardware into a sophisticated spatial awareness engine.
                  </p>
                  <p className="text-white/50 text-base leading-relaxed font-light">
                    The autonomous Black Box module serves as an immutable ledger, ensuring critical temporal fragments are securely encoded and retrievable during anomalous events.
                  </p>
                </div>

                <div className="space-y-4">
                  <h3 className="text-sm font-mono tracking-widest text-blue-400 uppercase mb-4">System Capabilities</h3>
                  <motion.div variants={staggerContainer} className="space-y-3">
                    {[
                      { icon: '◉', text: 'Real-time AR spatial projection matrix', color: 'text-purple-400' },
                      { icon: '⚠', text: 'Neural-net driven collision probability vectors', color: 'text-red-400' },
                      { icon: '⚙', text: 'Automated temporal shard encryption (Black Box)', color: 'text-orange-400' },
                      { icon: '◎', text: 'Monocular sensor fusion architecture', color: 'text-blue-400' },
                      { icon: '⚡', text: 'Automated distress signaling protocol', color: 'text-red-500' },
                      { icon: '◰', text: 'Global coordinates mapping integration', color: 'text-green-400' },
                    ].map((item, i) => (
                      <motion.div key={i} variants={fadeRight}>
                        <div className="flex items-start space-x-4 bg-black/50 border border-white/5 hover:border-white/20 hover:bg-white/5 rounded-xl px-4 py-3.5 transition-all duration-300">
                          <span className={`text-xl font-mono leading-none ${item.color}`}>{item.icon}</span>
                          <span className="text-white/80 text-sm font-medium tracking-wide">{item.text}</span>
                        </div>
                      </motion.div>
                    ))}
                  </motion.div>
                </div>
              </div>
            </div>
          </motion.div>
        </div>
      </section>

      {/* ─── System Architecture ─── */}
      <section className="py-20 px-6 relative z-10 border-t border-white/5 bg-black/20">
        <div className="max-w-6xl mx-auto">
          <motion.div initial="hidden" whileInView="visible" viewport={{ once: true }} variants={fadeUp} className="text-center mb-16">
            <h2 className="text-4xl font-bold text-white tracking-tight">Pipeline Architecture</h2>
            <div className="w-24 h-1 bg-gradient-to-r from-blue-500 to-purple-500 mx-auto mt-6 rounded-full opacity-50"></div>
          </motion.div>

          <motion.div
            initial="hidden" whileInView="visible" viewport={{ once: true }} variants={staggerContainer}
            className="grid md:grid-cols-3 gap-8 relative"
          >
            {/* Connecting line for desktop */}
            <div className="hidden md:block absolute top-[4.5rem] left-[15%] right-[15%] h-[2px] bg-gradient-to-r from-blue-500/20 via-purple-500/20 to-blue-500/20 z-0 border-t border-dashed border-white/10"></div>

            {[
              {
                step: '01', title: 'Sensory Input',
                desc: 'Monocular optical feed ingestion. High-frame-rate frame capturing via OpenCV hardware interfaces.',
                color: 'from-blue-600 to-cyan-500', shadow: 'shadow-[0_0_30px_rgba(59,130,246,0.2)]'
              },
              {
                step: '02', title: 'Neural Compute',
                desc: 'YOLOv8 nano models process inference graphs. Risk fusion heuristics compute spatial danger vectors.',
                color: 'from-purple-600 to-pink-500', shadow: 'shadow-[0_0_30px_rgba(168,85,247,0.2)]'
              },
              {
                step: '03', title: 'HUD & Storage',
                desc: 'Overlay injection into the video pipeline. Simultaneous h.264 chunked encoding for isolated Black Box retention.',
                color: 'from-orange-500 to-red-500', shadow: 'shadow-[0_0_30px_rgba(239,68,68,0.2)]'
              },
            ].map((item, i) => (
              <motion.div key={i} variants={fadeUp} className="relative z-10">
                <div className="bg-black/60 border border-white/5 backdrop-blur-md p-8 rounded-[2rem] text-center hover:border-white/20 transition-all duration-300 h-full group hover:-translate-y-2">
                  <div className={`w-16 h-16 mx-auto rounded-2xl bg-gradient-to-br ${item.color} ${item.shadow} flex items-center justify-center text-white font-mono font-bold text-xl mb-8 group-hover:scale-110 transition-transform duration-500 rotate-3 group-hover:rotate-6`}>
                    {item.step}
                  </div>
                  <h3 className="text-xl font-bold text-white mb-4 tracking-wide">{item.title}</h3>
                  <p className="text-white/50 text-sm leading-relaxed font-light">{item.desc}</p>
                </div>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* ─── Project Info ─── */}
      <section className="py-24 px-6 relative z-10">
        <div className="max-w-4xl mx-auto">
          <motion.div initial="hidden" whileInView="visible" viewport={{ once: true }} variants={scaleUp}>
            <div className="bg-gradient-to-br from-blue-900/20 to-purple-900/20 border border-white/10 backdrop-blur-md p-12 rounded-[3rem] text-center shadow-[0_0_50px_rgba(59,130,246,0.1)] relative overflow-hidden">
              <div className="absolute top-0 right-0 w-64 h-64 bg-blue-500/10 rounded-full blur-[100px] pointer-events-none"></div>
              <div className="absolute bottom-0 left-0 w-64 h-64 bg-purple-500/10 rounded-full blur-[100px] pointer-events-none"></div>

              <h2 className="text-sm font-mono tracking-widest text-blue-400 uppercase mb-4 relative z-10">Academic Development</h2>
              <h3 className="text-3xl md:text-4xl font-bold text-white mb-6 relative z-10 tracking-tight">Thakur Shyamnarayan Engineering College</h3>
              <p className="text-white/60 text-lg mb-10 max-w-2xl mx-auto font-light leading-relaxed relative z-10">
                VisionDrive is engineered as a culminating technical showcase for advanced undergraduate robotics and computer vision studies.
              </p>

              <div className="flex flex-wrap justify-center gap-4 relative z-10">
                {[
                  { val: '2026', label: 'BUILD_YEAR' },
                  { val: 'PYTHON/REACT', label: 'TECH_STACK' },
                  { val: 'YOLOv8', label: 'NEURAL_ENGINE' },
                ].map((d, i) => (
                  <div key={i} className="bg-black/40 border border-white/10 rounded-2xl px-8 py-5 hover:border-blue-500/40 transition-colors group">
                    <div className="text-2xl font-bold text-white tracking-wide group-hover:text-blue-400 transition-colors">{d.val}</div>
                    <div className="text-white/40 font-mono text-[10px] tracking-widest mt-2">{d.label}</div>
                  </div>
                ))}
              </div>
            </div>
          </motion.div>
        </div>
      </section>

      {/* ─── Footer ─── */}
      <footer className="py-8 px-6 border-t border-white/5 bg-black/40 relative z-10">
        <div className="max-w-7xl mx-auto flex flex-col items-center justify-between opacity-50 hover:opacity-100 transition-opacity">
          <p className="text-white/60 font-mono text-xs tracking-widest uppercase">
            © {new Date().getFullYear()} VISIONDRIVE // THAKUR SHYAMNARAYAN ENGINEERING COLLEGE
          </p>
        </div>
      </footer>
    </div>
  );
};

export default About;
