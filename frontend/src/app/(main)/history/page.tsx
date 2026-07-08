"use client";

import { motion } from "motion/react";
import { HistoryList } from "@/components/history/HistoryList";

export default function HistoryPage() {
  return (
    <div className="mx-auto max-w-[800px] px-4 py-8">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
      >
        <span className="inline-block rounded-full border border-[var(--border-glass)] bg-white/60 px-3 py-1 text-[11px] font-medium uppercase tracking-wider text-[var(--ink-muted)] backdrop-blur-sm">
          History
        </span>
        <h1 className="mt-4 font-display text-display-xl text-[var(--ink)]">
          Past Analyses
        </h1>
        <p className="mt-2 text-body-lg text-[var(--ink-muted)]">
          All your lip color analyses, saved and ready to revisit.
        </p>
      </motion.div>

      <div className="mt-10">
        <HistoryList />
      </div>
    </div>
  );
}
