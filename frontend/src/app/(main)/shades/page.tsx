"use client";

import { useEffect, useState, useCallback } from "react";
import { motion } from "motion/react";
import { apiClient } from "@/lib/api-client";
import type { Lipstick, LipType } from "@/types";
import { ShadeCard } from "@/components/shades/ShadeCard";

const lipTypeFilters: Array<{ label: string; value: LipType | null }> = [
  { label: "All", value: null },
  { label: "Pinkish", value: "Pinkish" },
  { label: "Brownish", value: "Brownish" },
  { label: "Dark", value: "Dark" },
];

export default function ShadesPage() {
  const [lipsticks, setLipsticks] = useState<Lipstick[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeFilter, setActiveFilter] = useState<LipType | null>(null);

  const fetchLipsticks = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const params = activeFilter ? `?lip_type=${activeFilter}` : "";
      const data = await apiClient<Lipstick[]>(`/api/v1/lipsticks${params}`);
      setLipsticks(data);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to load shades");
    } finally {
      setLoading(false);
    }
  }, [activeFilter]);

  useEffect(() => {
    fetchLipsticks();
  }, [fetchLipsticks]);

  return (
    <div className="mx-auto max-w-[1120px] px-4 py-8">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
      >
        <span className="inline-block rounded-full border border-[var(--border-glass)] bg-white/60 px-3 py-1 text-[11px] font-medium uppercase tracking-wider text-[var(--ink-muted)] backdrop-blur-sm">
          Shade Library
        </span>
        <h1 className="mt-4 font-display text-display-xl text-[var(--ink)]">
          Browse Lipstick Shades
        </h1>
        <p className="mt-2 text-body-lg text-[var(--ink-muted)]">
          Explore our curated collection of {lipsticks.length || "..."} shades.
        </p>
      </motion.div>

      {/* Filters */}
      <div className="mt-8 flex flex-wrap gap-2">
        {lipTypeFilters.map((f) => (
          <motion.button
            key={f.label}
            onClick={() => setActiveFilter(f.value)}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className="relative rounded-full px-4 py-1.5 text-body-sm font-medium transition-colors"
            style={{
              backgroundColor:
                activeFilter === f.value
                  ? "var(--primary)"
                  : "rgba(255, 255, 255, 0.6)",
              color:
                activeFilter === f.value ? "#fff" : "var(--ink-muted)",
              border:
                activeFilter === f.value
                  ? "1px solid var(--primary)"
                  : "1px solid var(--border-glass)",
            }}
          >
            {f.label}
          </motion.button>
        ))}
      </div>

      {/* Grid */}
      <div className="mt-6">
        {loading && (
          <div className="grid grid-cols-2 gap-4 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5">
            {Array.from({ length: 10 }).map((_, i) => (
              <div
                key={i}
                className="animate-pulse rounded-[var(--radius-md)] bg-white/40 p-4"
              >
                <div className="h-24 rounded-[var(--radius-sm)] bg-white/60" />
                <div className="mt-3 space-y-2">
                  <div className="h-4 w-3/4 rounded bg-white/60" />
                  <div className="h-3 w-1/2 rounded bg-white/40" />
                </div>
              </div>
            ))}
          </div>
        )}

        {error && (
          <div className="rounded-[var(--radius-md)] border border-red-200 bg-red-50/60 p-4 text-body-sm text-red-600 backdrop-blur-sm">
            {error}
            <button
              onClick={fetchLipsticks}
              className="ml-2 underline hover:no-underline"
            >
              Retry
            </button>
          </div>
        )}

        {!loading && !error && lipsticks.length === 0 && (
          <div className="flex flex-col items-center justify-center py-20 text-center">
            <p className="text-body-lg text-[var(--ink-muted)]">
              No shades found for this filter.
            </p>
          </div>
        )}

        {!loading && !error && lipsticks.length > 0 && (
          <div className="grid grid-cols-2 gap-4 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5">
            {lipsticks.map((ls) => (
              <motion.div
                key={ls.id}
                initial={{ opacity: 0, y: 12 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.3 }}
              >
                <ShadeCard lipstick={ls} />
              </motion.div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
