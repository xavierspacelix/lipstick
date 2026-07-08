"use client";

import { motion } from "motion/react";
import { useAuth } from "@/context/auth";
import { StatsCards } from "@/components/dashboard/StatsCards";
import { RecentAnalyses } from "@/components/dashboard/RecentAnalyses";
import { QuickAnalyze } from "@/components/dashboard/QuickAnalyze";

export default function DashboardPage() {
  const { user } = useAuth();

  return (
    <div className="mx-auto max-w-[1120px] px-4 py-8">
      {/* Welcome header */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
      >
        <span className="inline-block rounded-full border border-[var(--border-glass)] bg-white/60 px-3 py-1 text-[11px] font-medium uppercase tracking-wider text-[var(--ink-muted)] backdrop-blur-sm">
          Dashboard
        </span>
        <h1 className="mt-4 font-display text-display-xl text-[var(--ink)]">
          Welcome back{user ? `, ${user.name.split(" ")[0]}` : ""}
        </h1>
        <p className="mt-2 text-body-lg text-[var(--ink-muted)]">
          Upload a photo to find your perfect shade, or pick up where you left off.
        </p>
      </motion.div>

      {/* Stats row */}
      <div className="mt-10">
        <StatsCards />
      </div>

      {/* Bottom row */}
      <div className="mt-8 grid gap-6 lg:grid-cols-3">
        <div className="lg:col-span-2">
          <RecentAnalyses />
        </div>
        <div>
          <QuickAnalyze />
        </div>
      </div>
    </div>
  );
}
