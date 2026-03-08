import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { motion } from 'framer-motion';
import VideoModal from '@/components/VideoModal';
import FloatingParticles from '@/components/FloatingParticles';
import BackgroundPattern from '@/components/BackgroundPattern';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || "http://127.0.0.1:8000";
const API = `${BACKEND_URL}/api`;

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
      staggerChildren: 0.1
    }
  }
};

const scaleUp = {
  hidden: { opacity: 0, scale: 0.95 },
  visible: { opacity: 1, scale: 1, transition: { duration: 0.5, ease: [0.16, 1, 0.3, 1] } }
};

const Features = () => {
  const [videos, setVideos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedVideo, setSelectedVideo] = useState(null);

  useEffect(() => {
    fetchVideos();
  }, []);

  const fetchVideos = async () => {
    try {
      const response = await axios.get(`${API}/blackbox-videos`);
      const videosWithUrl = response.data.map(v => ({
        ...v,
        url: `${BACKEND_URL}${v.path}`
      }));
      setVideos(videosWithUrl);
    } catch (error) {
      console.error('Failed to fetch videos:', error);
    } finally {
      setLoading(false);
    }
  };

  const openVideoModal = (video) => setSelectedVideo(video);
  const closeVideoModal = () => setSelectedVideo(null);

  return (
    <div className="gradient-bg min-h-screen" data-testid="features-page">
      <FloatingParticles />
      <BackgroundPattern />

      {/* ─── Header ─── */}
      <section className="pt-32 pb-12 px-6 relative z-10">
        <motion.div initial="hidden" animate="visible" variants={fadeUp} className="max-w-7xl mx-auto text-center">
          <div className="inline-flex items-center bg-black/40 border border-white/5 backdrop-blur-md rounded-full px-5 py-2 mb-8 shadow-inner">
            <span className="w-2 h-2 bg-red-500 rounded-full mr-3 animate-pulse shadow-[0_0_10px_#ef4444]"></span>
            <span className="text-red-400 text-sm font-bold tracking-widest uppercase">Secure Storage Node</span>
          </div>
          <h1 className="text-5xl md:text-6xl font-bold mb-6 tracking-tight">
            <span className="text-white">Black Box </span>
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-red-400 via-orange-400 to-yellow-500">Vault</span>
          </h1>
          <p className="text-lg text-white/50 max-w-2xl mx-auto font-medium">
            Encrypted spatial memory fragments. Auto-locked telemetry and optical shards from priority incidents.
          </p>
        </motion.div>
      </section>

      {/* ─── Info Bar ─── */}
      <section className="pb-16 px-6 relative z-10">
        <div className="max-w-5xl mx-auto">
          <motion.div
            initial="hidden" animate="visible" variants={staggerContainer}
            className="grid grid-cols-1 md:grid-cols-3 gap-6"
          >
            {[
              { label: 'RETENTION_CAPACITY', value: '5 CYCLE_SHARDS', icon: '💾' },
              { label: 'SHARD_DURATION', value: '10 SECONDS', icon: '⏱️' },
              { label: 'ENCODING_MATRIX', value: 'H.264_AVC', icon: '🧬' },
            ].map((info, i) => (
              <motion.div key={i} variants={scaleUp} className="bg-black/40 border border-white/5 backdrop-blur-md p-6 rounded-2xl hover:border-red-500/30 transition-colors group text-center">
                <span className="text-3xl mb-4 block filter grayscale group-hover:grayscale-0 transition-all">{info.icon}</span>
                <div className="text-white font-mono text-lg tracking-wider group-hover:text-red-400 transition-colors">{info.value}</div>
                <div className="text-white/40 font-mono text-[10px] tracking-widest uppercase mt-2 block">{info.label}</div>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* ─── Video Grid ─── */}
      <section className="pb-24 px-6 relative z-10">
        <div className="max-w-6xl mx-auto">
          {loading ? (
            <div className="text-center py-20 flex flex-col items-center">
              <div className="w-16 h-16 border-4 border-white/10 border-t-red-500 rounded-full animate-spin shadow-[0_0_30px_rgba(239,68,68,0.3)]"></div>
              <p className="text-red-400/80 font-mono tracking-widest text-sm mt-8 uppercase animate-pulse">Decrypting secure fragments...</p>
            </div>
          ) : videos.length === 0 ? (
            <motion.div initial="hidden" animate="visible" variants={scaleUp} className="text-center py-16">
              <div className="glass-card border border-white/5 bg-black/60 max-w-2xl mx-auto p-12 rounded-3xl relative overflow-hidden group">
                <div className="absolute inset-0 bg-red-500/5 mix-blend-overlay pointer-events-none group-hover:bg-red-500/10 transition-colors"></div>
                <div className="w-20 h-20 mx-auto bg-black border border-white/10 rounded-full flex items-center justify-center mb-6 shadow-inner relative z-10">
                  <svg className="w-10 h-10 text-white/30" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
                  </svg>
                </div>
                <h3 className="text-white text-2xl font-bold mb-3 tracking-wide relative z-10">VAULT EMPTY</h3>
                <p className="text-white/50 mb-8 font-mono text-sm uppercase relative z-10">NO OPTICAL SHARDS DETECTED IN STORAGE</p>
                <div className="flex justify-center space-x-4 relative z-10">
                  <div className="bg-black/80 border border-white/10 rounded-lg px-5 py-3 text-white/40 text-xs font-mono">
                    TERMINATE_KEY: <span className="font-bold text-white ml-2">Q</span>
                  </div>
                  <div className="bg-red-900/20 border border-red-500/30 rounded-lg px-5 py-3 text-red-500/60 text-xs font-mono">
                    EMERGENCY_LOCK_KEY: <span className="font-bold text-red-500 ml-2">B</span>
                  </div>
                </div>
              </div>
            </motion.div>
          ) : (
            <>
              <motion.div initial="hidden" animate="visible" variants={fadeUp} className="flex justify-between items-end mb-8 border-b border-white/10 pb-4">
                <div>
                  <h2 className="text-2xl font-bold text-white tracking-wide">
                    {videos.length} FRAGMENT{videos.length !== 1 ? 'S' : ''} DETECTED
                  </h2>
                  <p className="text-white/40 font-mono text-[10px] tracking-widest uppercase mt-1">Ready for playback analysis</p>
                </div>
                <button
                  onClick={fetchVideos}
                  className="bg-black/50 hover:bg-white/10 border border-white/10 text-white/80 px-5 py-2.5 rounded-xl text-sm transition-all flex items-center space-x-2 shadow-sm font-mono tracking-wider uppercase"
                >
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                  </svg>
                  <span>Resync</span>
                </button>
              </motion.div>

              <motion.div initial="hidden" animate="visible" variants={staggerContainer} className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                {videos.map((video, index) => (
                  <motion.div key={index} variants={scaleUp}>
                    <div
                      className="bg-black/60 border border-white/5 p-4 cursor-pointer hover:border-red-500/40 hover:shadow-[0_0_30px_rgba(239,68,68,0.15)] transition-all duration-300 rounded-2xl group flex flex-col h-full relative overflow-hidden"
                      onClick={() => openVideoModal(video)}
                    >
                      {/* Decorative grid lines */}
                      <div className="absolute inset-0 bg-[linear-gradient(rgba(255,255,255,0.02)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.02)_1px,transparent_1px)] bg-[size:20px_20px] pointer-events-none opacity-0 group-hover:opacity-100 transition-opacity"></div>

                      <div className="aspect-video bg-black border border-white/10 rounded-xl mb-5 flex items-center justify-center relative overflow-hidden group-hover:border-red-500/30 transition-colors">
                        <div className="absolute inset-0 bg-gradient-to-t from-red-900/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
                        <svg className="w-16 h-16 text-white/20 group-hover:text-red-400 group-hover:scale-110 transition-all z-10 drop-shadow-lg" fill="currentColor" viewBox="0 0 24 24">
                          <path d="M8 5v14l11-7z" />
                        </svg>

                        {/* HUD record badge */}
                        <div className="absolute top-3 right-3 bg-red-600/90 backdrop-blur-md rounded px-2 py-1 flex items-center space-x-1.5 z-10 shadow-lg">
                          <span className="w-1.5 h-1.5 bg-white rounded-full animate-pulse"></span>
                          <span className="text-white text-[10px] font-mono font-bold tracking-widest">SECURE</span>
                        </div>

                        {/* Fake timestamps overlay */}
                        <div className="absolute bottom-2 left-3 text-white/30 font-mono text-[10px] z-10 group-hover:text-red-300/60 transition-colors">CH_0{index + 1}</div>
                      </div>

                      <div className="flex-grow space-y-3 relative z-10">
                        <h3 className="text-white font-mono font-medium truncate text-sm px-1 group-hover:text-red-100 transition-colors" title={video.filename}>
                          <span className="text-red-500 mr-2 opacity-50">&gt;</span>{video.filename}
                        </h3>
                        <div className="flex justify-between items-end border-t border-white/5 pt-3 mt-auto">
                          <div className="space-y-1">
                            <p className="text-white/40 font-mono text-[10px] uppercase">Logged</p>
                            <p className="text-white/60 text-xs font-mono tracking-wide">
                              {new Date(video.modified).toLocaleDateString()} <span className="text-white/30 px-1">|</span> {new Date(video.modified).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                            </p>
                          </div>
                          <div className="text-right space-y-1">
                            <p className="text-white/40 font-mono text-[10px] uppercase">Size</p>
                            <p className="text-white/50 text-xs font-mono group-hover:text-red-400 group-hover:font-bold transition-all">
                              {(video.size / 1024 / 1024).toFixed(1)} MB
                            </p>
                          </div>
                        </div>
                      </div>
                    </div>
                  </motion.div>
                ))}
              </motion.div>
            </>
          )}
        </div>
      </section>

      {selectedVideo && <VideoModal video={selectedVideo} onClose={closeVideoModal} />}
    </div>
  );
};

export default Features;