"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { motion } from "motion/react";
import { History, ArrowRight, SwatchBook } from "lucide-react";
import { apiClient } from "@/lib/api-client";

interface RecentItem {
  id: string;
  lip_type: string;
  confidence: number;
  top_recommendation: string | null;
  created_at: string;
}

const LIP_COLORS: Record<string, string> = {
  Pinkish: "#E1849C",
  Brownish: "#9C6B4F",
  Dark: "#4A1F2B",
};

export function RecentAnalyses() {
  const [items, setItems] = useState<RecentItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetch() {
      try {
        const data = await apiClient<RecentItem[]>("/api/v1/history");
        setItems(data.slice(0, 3));
      } catch (err) {
        setError(err instanceof Error ? err.message : null);
      } finally {
        setLoading(false);
      }
    }
    fetch();
  }, []);

  return (
    <div className="rounded-[var(--radius-md)] border border-[var(--border-glass)] bg-white/60 shadow-[var(--shadow-glass)] backdrop-blur-sm">
      <div className="flex items-center justify-between px-6 py-4">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-[var(--radius-sm)] bg-white/80 shadow-sm backdrop-blur-sm">
            <History className="h-5 w-5 text-[var(--primary)]" />
          </div>
          <div>
            <h3 className="font-display text-display-md text-[var(--ink)]">Recent Analyses</h3>
            <p className="text-body-sm text-[var(--ink-muted)]">Your latest results</p>
          </div>
        </div>
        <Link
          href="/history"
          className="flex items-center gap-1 rounded-[var(--radius-sm)] px-3 py-1.5 text-body-sm font-medium text-[var(--primary)] no-underline transition-all duration-base hover:bg-[rgba(139,47,69,0.08)]"
        >
          View all
          <ArrowRight className="h-3.5 w-3.5" />
        </Link>
      </div>

      <div className="border-t border-[var(--border)]/50 px-6 py-2">
        {loading && (
          <div className="space-y-3 py-2">
            {Array.from({ length: 3 }).map((_, i) => (
              <div key={i} className="flex animate-pulse items-center gap-4 px-2 py-3">
                <div className="h-10 w-10 rounded-[var(--radius-sm)] bg-[var(--border)]/50" />
                <div className="flex-1 space-y-1.5">
                  <div className="h-4 w-32 rounded bg-[var(--border)]/50" />
                  <div className="h-3 w-48 rounded bg-[var(--border)]/40" />
                </div>
              </div>
            ))}
          </div>
        )}

        {error && (
          <div className="px-2 py-6 text-center">
            <p className="text-body-sm text-[var(--ink-muted)]">Could not load recent analyses</p>
          </div>
        )}

        {!loading && !error && items.length === 0 && (
          <div className="px-2 py-6 text-center">
            <p className="text-body-sm text-[var(--ink-muted)]">No analyses yet</p>
          </div>
        )}

        {!loading && !error && items.map((item, i) => (
          <motion.div
            key={item.id}
            initial={{ opacity: 0, x: -10 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: i * 0.08, duration: 0.3 }}
          >
            <Link
              href={`/analysis/${item.id}`}
              className="flex items-center gap-4 rounded-[var(--radius-sm)] px-2 py-3 no-underline transition-all duration-base hover:bg-[rgba(139,47,69,0.04)]"
            >
              <div
                className="h-10 w-10 shrink-0 rounded-[var(--radius-sm)]"
                style={{ backgroundColor: LIP_COLORS[item.lip_type] ?? "#8C2F45" }}
              />
              <div className="min-w-0 flex-1">
                <p className="truncate text-body-md font-medium text-[var(--ink)]">
                  {item.top_recommendation ?? `${item.lip_type} analysis`}
                </p>
                <p className="text-body-sm text-[var(--ink-muted)]">
                  {item.lip_type} &middot; {(item.confidence * 100).toFixed(0)}% match
                </p>
              </div>
              <ArrowRight className="h-4 w-4 shrink-0 text-[var(--ink-muted)]" />
            </Link>
            {i < items.length - 1 && (
              <div className="ml-[56px] border-t border-[var(--border)]/30" />
            )}
          </motion.div>
        ))}
      </div>

      <div className="border-t border-[var(--border)]/50 px-6 py-4">
        <Link
          href="/analysis"
          className="flex items-center justify-center gap-2 rounded-[var(--radius-sm)] bg-[var(--primary)] py-2.5 text-body-sm font-medium text-[var(--primary-foreground)] no-underline transition-all duration-base hover:brightness-110"
        >
          <SwatchBook className="h-4 w-4" />
          New Analysis
        </Link>
      </div>
    </div>
  );
}
