import React from 'react';

/**
 * Floating background particles — decorative animated shapes.
 * Pure CSS animations, no JS overhead.
 */
const FloatingParticles = () => {
    const particles = [
        { size: 6, x: '10%', y: '20%', delay: '0s', duration: '8s', opacity: 0.5 },
        { size: 4, x: '80%', y: '15%', delay: '2s', duration: '10s', opacity: 0.4 },
        { size: 8, x: '25%', y: '70%', delay: '4s', duration: '12s', opacity: 0.35 },
        { size: 5, x: '70%', y: '60%', delay: '1s', duration: '9s', opacity: 0.45 },
        { size: 3, x: '50%', y: '40%', delay: '3s', duration: '11s', opacity: 0.4 },
        { size: 7, x: '90%', y: '80%', delay: '5s', duration: '7s', opacity: 0.35 },
        { size: 4, x: '15%', y: '50%', delay: '6s', duration: '13s', opacity: 0.4 },
        { size: 6, x: '60%', y: '30%', delay: '2.5s', duration: '8.5s', opacity: 0.38 },
    ];

    return (
        <div className="fixed inset-0 pointer-events-none overflow-hidden z-0">
            {particles.map((p, i) => (
                <div
                    key={i}
                    className="particle"
                    style={{
                        width: `${p.size}px`,
                        height: `${p.size}px`,
                        left: p.x,
                        top: p.y,
                        animationDelay: p.delay,
                        animationDuration: p.duration,
                        opacity: p.opacity,
                    }}
                />
            ))}
            {/* Large blurred orbs for depth */}
            <div className="orb orb-1" />
            <div className="orb orb-2" />
            <div className="orb orb-3" />
            <div className="orb orb-4" />
        </div>
    );
};

export default FloatingParticles;
