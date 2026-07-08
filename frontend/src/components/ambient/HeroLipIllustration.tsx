"use client";

import { motion } from "motion/react";

export function HeroLipIllustration() {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.8 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 1.2, ease: [0.16, 1, 0.3, 1] }}
      className="pointer-events-none absolute inset-0 flex items-center justify-center overflow-hidden"
    >
      <svg
        viewBox="0 0 400 180"
        className="h-auto w-[500px] opacity-[0.04]"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        <motion.path
          d="M80 90 C80 40, 140 30, 200 70 C260 30, 320 40, 320 90 C320 130, 260 160, 200 150 C140 160, 80 130, 80 90Z"
          stroke="var(--primary)"
          strokeWidth="1.5"
          initial={{ pathLength: 0 }}
          animate={{ pathLength: 1 }}
          transition={{ duration: 2, ease: [0.16, 1, 0.3, 1] }}
        />
        <motion.path
          d="M120 90 C120 65, 160 55, 200 80 C240 55, 280 65, 280 90 C280 110, 240 125, 200 120 C160 125, 120 110, 120 90Z"
          stroke="var(--accent)"
          strokeWidth="0.8"
          initial={{ pathLength: 0 }}
          animate={{ pathLength: 1 }}
          transition={{ duration: 2, delay: 0.3, ease: [0.16, 1, 0.3, 1] }}
        />
      </svg>
    </motion.div>
  );
}
