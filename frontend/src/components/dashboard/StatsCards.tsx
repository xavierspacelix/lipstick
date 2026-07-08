"use client";

import { useState, useEffect } from "react";
import { motion } from "motion/react";
import { ScanLine, Sparkles, Calendar, TrendingUp } from "lucide-react";
import { apiClient } from "@/lib/api-client";

interface Stats {
  total_analyses: number;
}

interface RecentItem {
  id: string;
  lip_type: string;
  confidence: number;
  top_recommendation: string | null;
  created_at: string;
}

export function StatsCards() {
  const [stats, setStats] = useState<Stats | null>(null);
  const [recent, setRecent] = useState<RecentItem[]>([]);

  useEffect(() => {
    async function fetch() {
      try {
        const [profileStats, history] = await Promise.all([
          apiClient<Stats>("/api/v1/profile/stats"),
          apiClient<RecentItem[]>("/api/v1/history"),
        ]);
        setStats(profileStats);
        setRecent(history);
      } catch {
        // silently fail — show defaults
      }
    }
    fetch();
  }, []);

  const total = stats?.total_analyses ?? 0;
  const lastAnalysis = recent[0];
  const lastDate = lastAnalysis
    ? new Date(lastAnalysis.created_at).toLocaleDateString("en-US", {
        month: "short",
        day: "numeric",
      })
    : "—";
  const topShade = recent.find((r) => r.top_recommendation)?.top_recommendation ?? "—";
  const lastLipType = recent.find((r) => r.lip_type)?.lip_type ?? "—";

  const cards = [
    {
      label: "Total Analyses",
      value: String(total),
      icon: ScanLine,
      change: total > 0 ? `${total} completed` : "No analyses yet",
      color: "var(--primary)",
    },
    {
      label: "Top Shade",
      value: topShade,
      icon: Sparkles,
      change: recent.length > 0 ? `From ${lastLipType} category` : "Upload to find out",
      color: "var(--lip-type-pinkish)",
    },
    {
      label: "Last Analysis",
      value: lastDate,
      icon: Calendar,
      change: lastAnalysis ? "View result" : "Not yet",
      color: "var(--accent)",
    },
    {
      label: "Best Match",
      value: recent.length > 0 ? `${(Math.max(...recent.map((r) => r.confidence), 0) * 100).toFixed(0)}%` : "—",
      icon: TrendingUp,
      change: recent.length > 0 ? "Top confidence score" : "No data yet",
      color: "var(--success)",
    },
  ];

  return (
    <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
      {cards.map((stat, i) => {
        const Icon = stat.icon;
        return (
          <motion.div
            key={stat.label}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.08, duration: 0.4, ease: [0.16, 1, 0.3, 1] }}
            className="group rounded-[var(--radius-md)] border border-[var(--border-glass)] bg-white/60 p-5 shadow-[var(--shadow-glass)] backdrop-blur-sm transition-all duration-base hover:bg-white/80 hover:shadow-[var(--shadow-glass-lg)]"
          >
            <div className="flex items-start justify-between">
              <div>
                <p className="text-body-sm text-[var(--ink-muted)]">{stat.label}</p>
                <p className="mt-1 font-display text-display-md text-[var(--ink)]">{stat.value}</p>
              </div>
              <div
                className="flex h-10 w-10 items-center justify-center rounded-[var(--radius-sm)] bg-white/80 shadow-sm backdrop-blur-sm"
                style={{ color: stat.color }}
              >
                <Icon className="h-5 w-5" />
              </div>
            </div>
            <p className="mt-3 text-body-sm text-[var(--ink-muted)]">{stat.change}</p>
          </motion.div>
        );
      })}
    </div>
  );
}
