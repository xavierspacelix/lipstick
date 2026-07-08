"use client";

import Link from "next/link";
import { motion } from "motion/react";
import { Upload } from "lucide-react";

export function QuickAnalyze() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.3, duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
      className="relative overflow-hidden rounded-[var(--radius-md)] border border-[var(--border-glass)] bg-gradient-to-br from-white/70 to-white/40 p-6 shadow-[var(--shadow-glass)] backdrop-blur-sm"
    >
      <div
        className="pointer-events-none absolute -top-12 -right-12 h-40 w-40 rounded-[var(--radius-full)] opacity-[0.06]"
        style={{ background: "radial-gradient(circle, var(--primary) 0%, transparent 70%)" }}
      />

      <div className="relative">
        <div className="flex h-12 w-12 items-center justify-center rounded-[var(--radius-sm)] bg-white/80 shadow-sm backdrop-blur-sm">
          <Upload className="h-6 w-6 text-[var(--primary)]" />
        </div>
        <h3 className="mt-4 font-display text-display-md text-[var(--ink)]">
          Quick Analyze
        </h3>
        <p className="mt-1 text-body-sm text-[var(--ink-muted)]">
          Upload a selfie and get your three perfect lipstick shades in seconds.
        </p>
        <Link
          href="/analysis"
          className="mt-4 inline-flex h-10 items-center gap-2 rounded-[var(--radius-sm)] bg-[var(--primary)] px-5 text-body-sm font-medium text-[var(--primary-foreground)] no-underline transition-all duration-base hover:brightness-110"
        >
          Upload Photo
          <Upload className="h-3.5 w-3.5" />
        </Link>
      </div>
    </motion.div>
  );
}
