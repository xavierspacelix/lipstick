"use client";

import { motion } from "motion/react";
import { useEffect, useState } from "react";

interface Swatch {
  x: number;
  y: number;
  size: number;
  color: string;
  delay: number;
}

const SWATCH_COLORS = [
  "var(--primary)",
  "var(--accent)",
  "var(--lip-type-pinkish)",
  "var(--lip-type-brownish)",
  "var(--lip-type-dark)",
  "var(--error)",
];

export function SwatchScatter() {
  const [swatches, setSwatches] = useState<Swatch[]>([]);

  useEffect(() => {
    const w = typeof window !== "undefined" ? window.innerWidth : 1200;
    const h = typeof window !== "undefined" ? window.innerHeight : 800;

    setSwatches(
      Array.from({ length: 8 }, (_, i) => ({
        x: 0.08 + Math.random() * 0.84,
        y: 0.08 + Math.random() * 0.84,
        size: 8 + Math.random() * 20,
        color: SWATCH_COLORS[i % SWATCH_COLORS.length],
        delay: Math.random() * 3,
      })),
    );
  }, []);

  return (
    <div className="pointer-events-none fixed inset-0 z-0 overflow-hidden">
      {swatches.map((s, i) => (
        <motion.div
          key={i}
          className="absolute rounded-full"
          style={{
            left: `${s.x * 100}%`,
            top: `${s.y * 100}%`,
            width: s.size,
            height: s.size,
            backgroundColor: s.color,
          }}
          animate={{
            y: [0, -15, 0],
            opacity: [0.15, 0.3, 0.15],
          }}
          transition={{
            duration: 4 + Math.random() * 3,
            delay: s.delay,
            repeat: Infinity,
            ease: "easeInOut",
          }}
        />
      ))}
    </div>
  );
}
