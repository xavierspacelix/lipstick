"use client";

import { useState, useEffect, useCallback } from "react";
import { motion } from "motion/react";
import { History as HistoryIcon } from "lucide-react";
import { HistoryItem } from "./HistoryItem";
import { apiClient } from "@/lib/api-client";

interface AnalysisSummary {
  id: string;
  lip_type: string;
  confidence: number;
  top_recommendation: string | null;
  created_at: string;
}

export function HistoryList() {
  const [items, setItems] = useState<AnalysisSummary[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchHistory = useCallback(async () => {
    try {
      const data = await apiClient<AnalysisSummary[]>("/api/v1/history");
      setItems(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load history");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchHistory();
  }, [fetchHistory]);

  const handleDelete = useCallback(
    async (id: string) => {
      try {
        await apiClient(`/api/v1/history/${id}`, { method: "DELETE" });
        setItems((prev) => prev.filter((item) => item.id !== id));
      } catch {
        setError("Failed to delete analysis");
      }
    },
    [],
  );

  if (loading) {
    return (
      <div className="space-y-3">
        {Array.from({ length: 4 }).map((_, i) => (
          <div
            key={i}
            className="animate-pulse rounded-[var(--radius-md)] border border-[var(--border-glass)] bg-white/40 p-5"
          >
            <div className="flex items-center gap-4">
              <div className="h-10 w-10 rounded-[var(--radius-sm)] bg-[var(--border)]/50" />
              <div className="flex-1 space-y-2">
                <div className="h-4 w-24 rounded bg-[var(--border)]/50" />
                <div className="h-3 w-40 rounded bg-[var(--border)]/40" />
              </div>
            </div>
          </div>
        ))}
      </div>
    );
  }

  if (error) {
    return (
      <div className="rounded-[var(--radius-md)] border border-[var(--error)]/20 bg-[var(--error)]/5 p-6 text-center">
        <p className="text-body-md text-[var(--error)]">{error}</p>
        <button
          onClick={fetchHistory}
          className="mt-3 text-body-sm font-medium text-[var(--primary)] hover:underline"
        >
          Try again
        </button>
      </div>
    );
  }

  if (items.length === 0) {
    return (
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="rounded-[var(--radius-md)] border border-[var(--border-glass)] bg-white/60 p-12 text-center shadow-[var(--shadow-glass)] backdrop-blur-sm"
      >
        <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-[var(--radius-sm)] bg-white/80 shadow-sm backdrop-blur-sm">
          <HistoryIcon className="h-8 w-8 text-[var(--ink-muted)]" />
        </div>
        <h3 className="mt-5 font-display text-display-md text-[var(--ink)]">
          No analyses yet
        </h3>
        <p className="mt-2 text-body-sm text-[var(--ink-muted)]">
          Upload your first photo to get lipstick recommendations.
        </p>
      </motion.div>
    );
  }

  return (
    <div className="space-y-3">
      {items.map((item, i) => (
        <HistoryItem
          key={item.id}
          id={item.id}
          lipType={item.lip_type}
          confidence={item.confidence}
          topRecommendation={item.top_recommendation}
          createdAt={item.created_at}
          onDelete={handleDelete}
          index={i}
        />
      ))}
    </div>
  );
}
