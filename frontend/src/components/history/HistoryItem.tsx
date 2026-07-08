"use client";

import Link from "next/link";
import { motion } from "motion/react";
import { Trash2, ArrowRight } from "lucide-react";

interface HistoryItemProps {
  id: string;
  lipType: string;
  confidence: number;
  topRecommendation: string | null;
  createdAt: string;
  onDelete: (id: string) => void;
  index: number;
}

const LIP_TYPE_COLORS: Record<string, string> = {
  Pinkish: "var(--lip-type-pinkish)",
  Brownish: "var(--lip-type-brownish)",
  Dark: "var(--lip-type-dark)",
};

export function HistoryItem({
  id,
  lipType,
  confidence,
  topRecommendation,
  createdAt,
  onDelete,
  index,
}: HistoryItemProps) {
  const date = new Date(createdAt);
  const formatted = date.toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
  });

  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.06, duration: 0.35, ease: [0.16, 1, 0.3, 1] }}
      className="group rounded-[var(--radius-md)] border border-[var(--border-glass)] bg-white/60 shadow-[var(--shadow-glass)] backdrop-blur-sm transition-all duration-base hover:bg-white/80 hover:shadow-[var(--shadow-glass-lg)]"
    >
      <div className="flex items-center gap-4 px-5 py-4">
        {/* Lip type color dot */}
        <div
          className="h-10 w-10 shrink-0 rounded-[var(--radius-sm)]"
          style={{ backgroundColor: LIP_TYPE_COLORS[lipType] ?? "#8C2F45" }}
        />

        {/* Details */}
        <div className="min-w-0 flex-1">
          <div className="flex items-center gap-3">
            <span
              className="rounded-[var(--radius-full)] px-2.5 py-0.5 text-data-sm font-medium text-white"
              style={{ backgroundColor: LIP_TYPE_COLORS[lipType] ?? "#8C2F45", opacity: 0.85 }}
            >
              {lipType}
            </span>
            <span className="font-mono text-data-sm text-[var(--ink-muted)]">
              {(confidence * 100).toFixed(0)}% match
            </span>
          </div>
          {topRecommendation && (
            <p className="mt-1 truncate text-body-md font-medium text-[var(--ink)]">
              {topRecommendation}
            </p>
          )}
          <p className="text-body-sm text-[var(--ink-muted)]">{formatted}</p>
        </div>

        {/* Actions */}
        <div className="flex items-center gap-2">
          <button
            onClick={() => onDelete(id)}
            className="flex h-8 w-8 items-center justify-center rounded-[var(--radius-sm)] text-[var(--ink-muted)] opacity-0 transition-all duration-base hover:bg-[var(--error)]/10 hover:text-[var(--error)] group-hover:opacity-100"
          >
            <Trash2 className="h-4 w-4" />
          </button>
          <Link
            href={`/analysis/${id}`}
            className="flex h-8 w-8 items-center justify-center rounded-[var(--radius-sm)] text-[var(--ink-muted)] transition-all duration-base hover:bg-[rgba(139,47,69,0.08)] hover:text-[var(--primary)]"
          >
            <ArrowRight className="h-4 w-4" />
          </Link>
        </div>
      </div>
    </motion.div>
  );
}
