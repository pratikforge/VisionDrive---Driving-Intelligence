import { useEffect, useRef, useState } from 'react';

/**
 * Custom hook that reveals elements when they scroll into the viewport.
 * Uses IntersectionObserver for performant scroll-triggered animations.
 *
 * @param {Object} options - IntersectionObserver options
 * @returns {[React.RefObject, boolean]} - ref to attach, and isVisible state
 */
export function useScrollReveal(options = {}) {
    const ref = useRef(null);
    const [isVisible, setIsVisible] = useState(false);

    useEffect(() => {
        const observer = new IntersectionObserver(([entry]) => {
            if (entry.isIntersecting) {
                setIsVisible(true);
                observer.unobserve(entry.target); // Only trigger once
            }
        }, { threshold: 0.15, ...options });

        const el = ref.current;
        if (el) observer.observe(el);

        return () => { if (el) observer.unobserve(el); };
    }, [options]);

    return [ref, isVisible];
}

/**
 * Animated counter hook — counts up from 0 to a target value.
 * @param {number|string} end - target value (can be "25+" or "<50ms")
 * @param {number} duration - animation duration in ms
 * @param {boolean} start - whether to start counting
 */
export function useCounter(end, duration = 1500, start = false) {
    const [count, setCount] = useState(0);
    const numericEnd = parseInt(end, 10) || 0;

    useEffect(() => {
        if (!start || numericEnd === 0) return;

        let startTime = null;
        const step = (timestamp) => {
            if (!startTime) startTime = timestamp;
            const progress = Math.min((timestamp - startTime) / duration, 1);
            setCount(Math.floor(progress * numericEnd));
            if (progress < 1) requestAnimationFrame(step);
        };
        requestAnimationFrame(step);
    }, [start, numericEnd, duration]);

    return count;
}

export default useScrollReveal;
