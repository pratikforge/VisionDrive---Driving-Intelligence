import React from 'react';

/**
 * BackgroundPattern — Layered geometric SVG pattern overlay.
 * Adds a subtle grid, diagonal accent lines, and glowing corner dots
 * so that empty sections of the gradient background feel visually rich.
 *
 * Usage: drop <BackgroundPattern /> inside any page wrapper
 *        (alongside FloatingParticles).
 */
const BackgroundPattern = () => {
    return (
        <div className="fixed inset-0 pointer-events-none overflow-hidden z-[1]">

            {/* ─── 1. Subtle grid ─── */}
            <svg className="absolute inset-0 w-full h-full opacity-[0.15]" xmlns="http://www.w3.org/2000/svg">
                <defs>
                    <pattern id="grid-sm" width="40" height="40" patternUnits="userSpaceOnUse">
                        <path d="M 40 0 L 0 0 0 40" fill="none" stroke="white" strokeWidth="0.5" />
                    </pattern>
                    <pattern id="grid-lg" width="200" height="200" patternUnits="userSpaceOnUse">
                        <rect width="200" height="200" fill="url(#grid-sm)" />
                        <path d="M 200 0 L 0 0 0 200" fill="none" stroke="white" strokeWidth="1" />
                    </pattern>
                </defs>
                <rect width="100%" height="100%" fill="url(#grid-lg)" />
            </svg>

            {/* ─── 2. Diagonal accent lines ─── */}
            <svg className="absolute inset-0 w-full h-full opacity-[0.12]" xmlns="http://www.w3.org/2000/svg">
                <defs>
                    <pattern id="diag" width="60" height="60" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
                        <line x1="0" y1="0" x2="0" y2="60" stroke="white" strokeWidth="0.5" />
                    </pattern>
                </defs>
                <rect width="100%" height="100%" fill="url(#diag)" />
            </svg>

            {/* ─── 3. Dotted matrix ─── */}
            <svg className="absolute inset-0 w-full h-full opacity-[0.18]" xmlns="http://www.w3.org/2000/svg">
                <defs>
                    <pattern id="dots" width="30" height="30" patternUnits="userSpaceOnUse">
                        <circle cx="15" cy="15" r="1" fill="white" />
                    </pattern>
                </defs>
                <rect width="100%" height="100%" fill="url(#dots)" />
            </svg>

            {/* ─── 4. Glowing circuit traces (decorative paths) ─── */}
            <svg className="absolute inset-0 w-full h-full" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="none" viewBox="0 0 1440 900">
                {/* Top-left trace */}
                <path
                    d="M0 200 Q 200 180, 300 280 T 600 220"
                    fill="none"
                    stroke="rgba(155,61,255,0.25)"
                    strokeWidth="1.5"
                    className="circuit-trace circuit-trace-1"
                />
                {/* Top-right trace */}
                <path
                    d="M1440 100 Q 1200 150, 1100 250 T 800 180"
                    fill="none"
                    stroke="rgba(255,90,60,0.25)"
                    strokeWidth="1.5"
                    className="circuit-trace circuit-trace-2"
                />
                {/* Bottom trace */}
                <path
                    d="M100 700 Q 400 650, 500 750 T 900 680 T 1300 760"
                    fill="none"
                    stroke="rgba(255,158,61,0.2)"
                    strokeWidth="1.5"
                    className="circuit-trace circuit-trace-3"
                />
                {/* Middle horizontal */}
                <path
                    d="M0 450 L 200 450 L 250 400 L 400 400 L 450 450 L 700 450"
                    fill="none"
                    stroke="rgba(155,61,255,0.15)"
                    strokeWidth="1"
                    className="circuit-trace circuit-trace-4"
                />
                {/* Right descending */}
                <path
                    d="M1440 500 L 1200 500 L 1150 550 L 1000 550 L 950 500 L 800 500"
                    fill="none"
                    stroke="rgba(255,90,60,0.15)"
                    strokeWidth="1"
                    className="circuit-trace circuit-trace-5"
                />

                {/* Node dots along the traces */}
                {[
                    { cx: 300, cy: 280 },
                    { cx: 600, cy: 220 },
                    { cx: 1100, cy: 250 },
                    { cx: 800, cy: 180 },
                    { cx: 500, cy: 750 },
                    { cx: 900, cy: 680 },
                    { cx: 250, cy: 400 },
                    { cx: 450, cy: 450 },
                    { cx: 1150, cy: 550 },
                    { cx: 950, cy: 500 },
                ].map((dot, i) => (
                    <circle
                        key={i}
                        cx={dot.cx}
                        cy={dot.cy}
                        r="3"
                        fill="rgba(255,255,255,0.3)"
                        className="circuit-node"
                        style={{ animationDelay: `${i * 0.8}s` }}
                    />
                ))}
            </svg>

            {/* ─── 5. Hexagonal accent (top-right) ─── */}
            <svg
                className="absolute -top-20 -right-20 w-[500px] h-[500px] opacity-[0.12] hex-rotate"
                viewBox="0 0 200 200"
                xmlns="http://www.w3.org/2000/svg"
            >
                <defs>
                    <pattern id="hex" width="28" height="49" patternUnits="userSpaceOnUse" patternTransform="scale(2)">
                        <polygon points="14,2 25,9 25,23 14,30 3,23 3,9" fill="none" stroke="white" strokeWidth="0.5" />
                        <polygon points="14,26 25,33 25,47 14,54 3,47 3,33" fill="none" stroke="white" strokeWidth="0.5" transform="translate(14,0)" />
                    </pattern>
                </defs>
                <rect width="200" height="200" fill="url(#hex)" />
            </svg>

            {/* ─── 6. Concentric rings (bottom-left) ─── */}
            <svg
                className="absolute -bottom-32 -left-32 w-[400px] h-[400px] opacity-[0.15] ring-pulse"
                viewBox="0 0 400 400"
                xmlns="http://www.w3.org/2000/svg"
            >
                {[60, 100, 140, 180, 200].map((r, i) => (
                    <circle
                        key={i}
                        cx="200"
                        cy="200"
                        r={r}
                        fill="none"
                        stroke="rgba(255,158,61,0.6)"
                        strokeWidth="0.5"
                        strokeDasharray="8 12"
                    />
                ))}
            </svg>

            {/* ─── 7. Floating plus signs ─── */}
            {[
                { x: '5%', y: '35%', size: 16, delay: 0 },
                { x: '92%', y: '45%', size: 12, delay: 2 },
                { x: '48%', y: '85%', size: 14, delay: 4 },
                { x: '75%', y: '12%', size: 10, delay: 1.5 },
                { x: '20%', y: '75%', size: 18, delay: 3 },
                { x: '85%', y: '70%', size: 11, delay: 5 },
            ].map((p, i) => (
                <svg
                    key={i}
                    className="absolute opacity-[0.25] float-decoration"
                    style={{
                        left: p.x,
                        top: p.y,
                        width: `${p.size}px`,
                        height: `${p.size}px`,
                        animationDelay: `${p.delay}s`,
                    }}
                    viewBox="0 0 16 16"
                    xmlns="http://www.w3.org/2000/svg"
                >
                    <line x1="8" y1="2" x2="8" y2="14" stroke="white" strokeWidth="1.5" strokeLinecap="round" />
                    <line x1="2" y1="8" x2="14" y2="8" stroke="white" strokeWidth="1.5" strokeLinecap="round" />
                </svg>
            ))}

            {/* ─── 8. Diamond shapes ─── */}
            {[
                { x: '30%', y: '20%', size: 10, delay: 1 },
                { x: '65%', y: '55%', size: 8, delay: 3 },
                { x: '15%', y: '90%', size: 12, delay: 2 },
                { x: '88%', y: '25%', size: 9, delay: 4 },
            ].map((d, i) => (
                <svg
                    key={i}
                    className="absolute opacity-[0.2] float-decoration"
                    style={{
                        left: d.x,
                        top: d.y,
                        width: `${d.size}px`,
                        height: `${d.size}px`,
                        animationDelay: `${d.delay}s`,
                    }}
                    viewBox="0 0 16 16"
                    xmlns="http://www.w3.org/2000/svg"
                >
                    <polygon points="8,1 15,8 8,15 1,8" fill="none" stroke="white" strokeWidth="1" />
                </svg>
            ))}
        </div>
    );
};

export default BackgroundPattern;
