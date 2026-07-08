"use client";

import Link from "next/link";
import { motion } from "motion/react";
import { Lipstick3D } from "@/components/ambient/Lipstick3D";

export function Hero() {
  return (
    <section className="relative min-h-screen overflow-hidden pt-32 md:pt-44">
      {/* Atmosphere glow */}
      <div
        className="pointer-events-none absolute top-1/3 left-1/2 h-[700px] w-[700px] -translate-x-1/2 -translate-y-1/2 rounded-[var(--radius-full)] opacity-[0.04]"
        style={{ background: "radial-gradient(circle, var(--primary) 0%, transparent 70%)" }}
      />

      <div className="relative mx-auto max-w-[1120px] px-4">
        <div className="grid items-center gap-16 md:grid-cols-2">
          {/* Text side */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.7, ease: [0.16, 1, 0.3, 1] }}
          >
            <motion.span
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.1, duration: 0.4 }}
              className="inline-block rounded-full border border-[var(--border-glass)] bg-white/60 px-4 py-1.5 text-body-sm text-[var(--ink-muted)] backdrop-blur-sm"
            >
              AI-Powered Beauty Analysis
            </motion.span>

            <motion.h1
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2, duration: 0.7, ease: [0.16, 1, 0.3, 1] }}
              className="mt-8 font-display text-display-xl leading-[1.1] tracking-tight text-[var(--ink)]"
            >
              Your Perfect
              <span className="block text-[var(--primary)]">Lipstick Match</span>
            </motion.h1>

            <motion.p
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.35, duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
              className="mt-6 max-w-md text-body-lg leading-relaxed text-[var(--ink-muted)]"
            >
              Upload a selfie. AI analyzes your natural lip color.
              Three perfect shades. No guesswork.
            </motion.p>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.5, duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
              className="mt-10 flex items-center gap-4"
            >
              <Link
                href="/register"
                className="inline-flex h-12 items-center gap-2 rounded-[var(--radius-sm)] bg-[var(--primary)] px-6 text-body-sm font-medium text-[var(--primary-foreground)] no-underline transition-all duration-base hover:brightness-110"
              >
                Get Started Free
              </Link>
              <Link
                href="/login"
                className="inline-flex h-12 items-center gap-2 rounded-[var(--radius-sm)] border border-[var(--border)] bg-white/60 px-6 text-body-sm font-medium text-[var(--ink)] no-underline shadow-[var(--shadow-glass)] backdrop-blur-sm transition-all duration-base hover:bg-white/80"
              >
                Sign In
              </Link>
            </motion.div>
          </motion.div>

          {/* Lipstick visual side */}
          <motion.div
            className="hidden md:flex md:items-center md:justify-center"
            initial={{ opacity: 0, x: 60 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.3, duration: 1, ease: [0.16, 1, 0.3, 1] }}
          >
            <div className="relative">
              {/* Glow behind lipstick */}
              <div
                className="pointer-events-none absolute inset-0 -top-20 -bottom-20 -left-20 -right-20 rounded-[var(--radius-full)] opacity-[0.07]"
                style={{
                  background:
                    "radial-gradient(ellipse at center, var(--primary) 0%, transparent 70%)",
                }}
              />
              <Lipstick3D color="primary" className="relative w-56" />
            </div>
          </motion.div>
        </div>
      </div>

      {/* Scroll indicator */}
      <motion.div
        className="absolute bottom-8 left-1/2 -translate-x-1/2"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1.5, duration: 0.8 }}
      >
        <motion.div
          className="flex flex-col items-center gap-2"
          animate={{ y: [0, 6, 0] }}
          transition={{ duration: 2, repeat: Infinity, ease: "easeInOut" }}
        >
          <span className="text-[11px] font-medium uppercase tracking-[0.15em] text-[var(--ink-muted)]/50">
            Scroll
          </span>
          <svg
            className="h-4 w-4 text-[var(--ink-muted)]/40"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            strokeWidth={1.5}
          >
            <path d="M12 5v14M5 12l7 7 7-7" />
          </svg>
        </motion.div>
      </motion.div>
    </section>
  );
}
