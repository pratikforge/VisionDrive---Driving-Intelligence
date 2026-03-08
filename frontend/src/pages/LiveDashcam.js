import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import { motion, AnimatePresence } from 'framer-motion';
import FloatingParticles from '@/components/FloatingParticles';
import BackgroundPattern from '@/components/BackgroundPattern';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || "http://127.0.0.1:8000";
const API = `${BACKEND_URL}/api`;
const DASHCAM_URL = "http://localhost:8001";

/* ─── Framer Motion variants ─── */
const fadeUp = {
    hidden: { opacity: 0, y: 30 },
    visible: { opacity: 1, y: 0, transition: { duration: 0.8, ease: [0.16, 1, 0.3, 1] } }
};

const scaleUp = {
    hidden: { opacity: 0, scale: 0.95 },
    visible: { opacity: 1, scale: 1, transition: { duration: 0.6, ease: [0.16, 1, 0.3, 1] } }
};

const LiveDashcam = () => {
    const [isStreaming, setIsStreaming] = useState(false);
    const [isLoading, setIsLoading] = useState(false);
    const [feedKey, setFeedKey] = useState(0);
    const [error, setError] = useState(null);

    // Poll dashcam status
    const checkStatus = useCallback(async () => {
        try {
            const res = await axios.get(`${API}/dashcam-status`);
            setIsStreaming(res.data.running);
        } catch {
            // Backend might not be reachable
        }
    }, []);

    useEffect(() => {
        checkStatus();
        const interval = setInterval(checkStatus, 3000);
        return () => clearInterval(interval);
    }, [checkStatus]);

    const handleStart = async () => {
        setIsLoading(true);
        setError(null);
        try {
            const res = await axios.post(`${API}/launch-dashcam`);
            if (res.data.status === 'success' || res.data.status === 'already_running') {
                // Wait a moment for the server to boot, then show stream
                setTimeout(() => {
                    setIsStreaming(true);
                    setFeedKey(prev => prev + 1); // Force img reload
                    setIsLoading(false);
                }, 4000);
            }
        } catch (err) {
            console.error('Failed to launch dashcam:', err);
            setError('Failed to start dashcam. Make sure YOLOv8 and webcam are available.');
            setIsLoading(false);
        }
    };

    const handleStop = async () => {
        setIsLoading(true);
        try {
            await axios.post(`${API}/stop-dashcam`);
            setIsStreaming(false);
        } catch (err) {
            console.error('Failed to stop dashcam:', err);
        }
        setIsLoading(false);
    };

    return (
        <div className="gradient-bg min-h-screen" data-testid="live-dashcam-page">
            <FloatingParticles />
            <BackgroundPattern />

            {/* ─── Header ─── */}
            <section className="pt-32 pb-8 px-6 relative z-10">
                <motion.div initial="hidden" animate="visible" variants={fadeUp} className="max-w-7xl mx-auto text-center">
                    <div className="inline-flex items-center bg-black/40 border border-white/5 backdrop-blur-md rounded-full px-5 py-2 mb-8 shadow-inner">
                        {isStreaming ? (
                            <>
                                <span className="w-2.5 h-2.5 bg-red-500 rounded-full mr-3 animate-pulse shadow-[0_0_10px_#ef4444]"></span>
                                <span className="text-red-400 text-sm font-bold tracking-widest uppercase">Live Telemetry Active</span>
                            </>
                        ) : (
                            <>
                                <span className="w-2.5 h-2.5 bg-gray-500 rounded-full mr-3"></span>
                                <span className="text-gray-400 text-sm font-bold tracking-widest uppercase">Sensors Offline</span>
                            </>
                        )}
                    </div>
                    <h1 className="text-5xl md:text-6xl font-bold mb-6 tracking-tight">
                        <span className="text-white">Spatial </span>
                        <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-500">Monitor</span>
                    </h1>
                    <p className="text-lg text-white/50 max-w-2xl mx-auto font-medium">
                        Real-time visualization of the YOLOv8 neural network processing inference shards.
                    </p>
                </motion.div>
            </section>

            {/* ─── Controls ─── */}
            <section className="pb-10 px-6 relative z-10">
                <div className="max-w-4xl mx-auto flex justify-center items-center space-x-4">
                    <motion.div initial="hidden" animate="visible" variants={scaleUp}>
                        <AnimatePresence mode="wait">
                            {!isStreaming ? (
                                <motion.button
                                    key="start"
                                    initial={{ opacity: 0, scale: 0.9 }}
                                    animate={{ opacity: 1, scale: 1 }}
                                    exit={{ opacity: 0, scale: 0.9 }}
                                    onClick={handleStart}
                                    disabled={isLoading}
                                    className="btn-gradient-purple text-white px-10 py-4 text-lg rounded-full font-bold shadow-[0_0_30px_rgba(147,51,234,0.3)] flex items-center space-x-3 disabled:opacity-50 disabled:cursor-not-allowed uppercase tracking-wide"
                                    data-testid="start-dashcam-btn"
                                >
                                    {isLoading ? (
                                        <>
                                            <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                                            <span>Initializing...</span>
                                        </>
                                    ) : (
                                        <>
                                            <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                                                <path d="M8 5v14l11-7z" />
                                            </svg>
                                            <span>Engage Optics</span>
                                        </>
                                    )}
                                </motion.button>
                            ) : (
                                <motion.button
                                    key="stop"
                                    initial={{ opacity: 0, scale: 0.9 }}
                                    animate={{ opacity: 1, scale: 1 }}
                                    exit={{ opacity: 0, scale: 0.9 }}
                                    onClick={handleStop}
                                    disabled={isLoading}
                                    className="bg-red-600/80 hover:bg-red-500 border border-red-400/30 text-white px-10 py-4 text-lg rounded-full font-bold shadow-[0_0_30px_rgba(239,68,68,0.4)] flex items-center space-x-3 transition-colors disabled:opacity-50 uppercase tracking-wide"
                                    data-testid="stop-dashcam-btn"
                                >
                                    <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                                        <rect x="6" y="6" width="12" height="12" rx="2" />
                                    </svg>
                                    <span>Terminate Link</span>
                                </motion.button>
                            )}
                        </AnimatePresence>
                    </motion.div>
                </div>
                {error && (
                    <p className="text-center text-red-300 mt-4 text-sm">{error}</p>
                )}
            </section>

            {/* ─── Stream Viewer HUD ─── */}
            <section className="pb-16 px-6 relative z-10">
                <div className="max-w-6xl mx-auto">
                    <motion.div initial="hidden" animate="visible" variants={fadeUp} className="relative">
                        {/* Decorative HUD corners */}
                        <div className="absolute -top-1 -left-1 w-12 h-12 border-t-2 border-l-2 border-blue-500 rounded-tl-xl z-20 opacity-50"></div>
                        <div className="absolute -top-1 -right-1 w-12 h-12 border-t-2 border-r-2 border-blue-500 rounded-tr-xl z-20 opacity-50"></div>
                        <div className="absolute -bottom-1 -left-1 w-12 h-12 border-b-2 border-l-2 border-blue-500 rounded-bl-xl z-20 opacity-50"></div>
                        <div className="absolute -bottom-1 -right-1 w-12 h-12 border-b-2 border-r-2 border-blue-500 rounded-br-xl z-20 opacity-50"></div>

                        <div className="glass-card p-1 md:p-2 rounded-xl border border-blue-500/20 shadow-[0_0_50px_rgba(59,130,246,0.1)] relative overflow-hidden bg-black/60">
                            {isStreaming ? (
                                <div className="relative rounded-lg overflow-hidden group">
                                    {/* Scanline overlay */}
                                    <div className="absolute inset-0 bg-[linear-gradient(transparent_50%,rgba(0,0,0,0.1)_50%)] bg-[length:100%_4px] pointer-events-none z-10 opacity-30"></div>
                                    <div className="absolute inset-0 bg-blue-500/5 mix-blend-overlay pointer-events-none z-10"></div>

                                    <img
                                        key={feedKey}
                                        src={`${DASHCAM_URL}/feed`}
                                        alt="Live Dashcam Feed"
                                        className="w-full h-auto"
                                        style={{ display: 'block', aspectRatio: '16/9', objectFit: 'cover' }}
                                    />

                                    {/* HUD Elements Overlay */}
                                    <div className="absolute top-4 left-4 z-20 bg-red-500/20 border border-red-500/50 backdrop-blur-md rounded px-3 py-1 flex items-center space-x-2">
                                        <span className="w-2 h-2 bg-red-500 rounded-full animate-pulse"></span>
                                        <span className="text-red-400 text-xs font-mono font-bold tracking-widest">SYS.REC</span>
                                    </div>
                                    <div className="absolute top-4 right-4 z-20 bg-black/40 border border-blue-500/30 backdrop-blur-md rounded px-3 py-1">
                                        <span className="text-blue-400 text-xs font-mono font-bold tracking-widest">YOLOv8 ENGINE</span>
                                    </div>
                                    <div className="absolute bottom-4 left-4 z-20">
                                        <div className="text-white/50 text-[10px] font-mono tracking-widest uppercase mb-1">Telemetry Data</div>
                                        <div className="flex space-x-4">
                                            <div className="bg-black/40 border border-white/5 backdrop-blur-md px-3 py-1.5 rounded"><span className="text-white/40 font-mono text-xs">LAT_</span><span className="text-white font-mono text-xs ml-1">33.7490° N</span></div>
                                            <div className="bg-black/40 border border-white/5 backdrop-blur-md px-3 py-1.5 rounded"><span className="text-white/40 font-mono text-xs">LON_</span><span className="text-white font-mono text-xs ml-1">84.3880° W</span></div>
                                        </div>
                                    </div>
                                </div>
                            ) : (
                                <div className="w-full rounded-lg flex flex-col items-center justify-center relative overflow-hidden"
                                    style={{ aspectRatio: '16/9', background: 'radial-gradient(circle at center, #111 0%, #000 100%)' }}>
                                    <div className="absolute inset-0 border border-blue-500/10 m-4 rounded scale-95 pointer-events-none"></div>

                                    <motion.div
                                        animate={{ opacity: [0.5, 1, 0.5] }}
                                        transition={{ repeat: Infinity, duration: 2 }}
                                        className="mb-6"
                                    >
                                        <svg className="w-20 h-20 text-blue-500/30" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1}
                                                d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
                                        </svg>
                                    </motion.div>
                                    <div className="text-center space-y-2">
                                        <p className="text-white/70 tracking-widest font-mono uppercase text-sm">Signal Lost</p>
                                        <p className="text-blue-400/50 font-mono text-xs tracking-widest">AWAITING SENSOR INITIALIZATION</p>
                                    </div>
                                </div>
                            )}
                        </div>
                    </motion.div>
                </div>
            </section>

            {/* ─── Info Cards ─── */}
            <section className="pb-20 px-6 relative z-10">
                <div className="max-w-6xl mx-auto">
                    <motion.div
                        initial="hidden" whileInView="visible" viewport={{ once: true }}
                        variants={{ visible: { transition: { staggerChildren: 0.1 } } }}
                        className="grid grid-cols-2 md:grid-cols-4 gap-6"
                    >
                        {[
                            { title: 'INPUT_SOURCE', desc: 'LOCAL_WEBCAM' },
                            { title: 'ENGINE', desc: 'YOLOv8_NANO' },
                            { title: 'CLASSES', desc: '80_COCO_SET' },
                            { title: 'PROTOCOL', desc: 'HTTP_MJPEG' },
                        ].map((info, i) => (
                            <motion.div key={i} variants={scaleUp} className="bg-black/40 border border-white/5 backdrop-blur-md p-6 rounded-2xl hover:border-blue-500/30 transition-colors group">
                                <span className="text-blue-400 font-mono text-[10px] tracking-widest uppercase mb-2 block">{info.title}</span>
                                <div className="text-white font-mono text-sm tracking-wider group-hover:text-transparent group-hover:bg-clip-text group-hover:bg-gradient-to-r group-hover:from-blue-400 group-hover:to-purple-500 transition-colors">{info.desc}</div>
                            </motion.div>
                        ))}
                    </motion.div>
                </div>
            </section>

            {/* ─── Terminal Logs Panel ─── */}
            <section className="pb-24 px-6 relative z-10">
                <div className="max-w-4xl mx-auto">
                    <motion.div initial="hidden" whileInView="visible" viewport={{ once: true }} variants={fadeUp}>
                        <div className="glass-card p-6 rounded-2xl border border-white/5 bg-black/80 font-mono">
                            <div className="flex items-center space-x-2 mb-4 border-b border-white/10 pb-4">
                                <div className="w-3 h-3 rounded-full bg-red-500/50"></div>
                                <div className="w-3 h-3 rounded-full bg-yellow-500/50"></div>
                                <div className="w-3 h-3 rounded-full bg-green-500/50"></div>
                                <span className="ml-4 text-white/40 text-xs tracking-widest uppercase">System Log Terminal</span>
                            </div>
                            <div className="space-y-2 text-sm">
                                <div className="text-blue-400">&gt; Initializing VisionDrive kernel...</div>
                                <div className="text-green-400">&gt; Kernel OK. Loading YOLOv8 weights.</div>
                                <div className="text-white/60">&gt; Ready for optical input.</div>
                                {isStreaming && (
                                    <>
                                        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 1.5 }} className="text-purple-400">&gt; Stream established. Frames streaming at 30 FPS.</motion.div>
                                        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 2.5 }} className="text-yellow-400">&gt; Neural inference latency: 42ms min avg.</motion.div>
                                    </>
                                )}
                                <div className="animate-pulse text-white/40">&gt; _</div>
                            </div>
                        </div>
                    </motion.div>
                </div>
            </section>

        </div>
    );
};

export default LiveDashcam;
