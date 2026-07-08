"use client";

import { motion } from "motion/react";
import type { Recommendation } from "@/types/analysis";

interface RecommendationCardProps {
  recommendation: Recommendation;
  index: number;
}

function rgbToHex(r: number, g: number, b: number) {
  return "#" + [r, g, b].map((x) => x.toString(16).padStart(2, "0")).join("");
}

export function RecommendationCard({ recommendation, index }: RecommendationCardProps) {
  const hex = rgbToHex(recommendation.rgb.r, recommendation.rgb.g, recommendation.rgb.b);

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.1, duration: 0.4, ease: [0.16, 1, 0.3, 1] }}
      className="group rounded-[var(--radius-md)] border border-[var(--border-glass)] bg-white/60 p-5 shadow-[var(--shadow-glass)] backdrop-blur-sm transition-all duration-base hover:bg-white/80 hover:shadow-[var(--shadow-glass-lg)]"
    >
      <div className="flex items-start gap-4">
        {/* Color swatch */}
        <div className="relative shrink-0">
          <div
            className="h-14 w-14 rounded-[var(--radius-sm)] border border-[var(--border)] shadow-sm"
            style={{ backgroundColor: hex }}
          />
          <div className="absolute -top-2 -right-2 flex h-6 w-6 items-center justify-center rounded-full bg-white text-[10px] font-bold shadow-sm text-[var(--ink-muted)]">
            {index + 1}
          </div>
        </div>

        {/* Details */}
        <div className="min-w-0 flex-1">
          <h4 className="font-display text-display-md text-[var(--ink)]">
            {recommendation.shade_name}
          </h4>
          <div className="mt-1 flex flex-wrap items-center gap-3">
            <span
              className="rounded-[var(--radius-full)] px-2.5 py-0.5 text-data-sm font-medium text-white"
              style={{
                backgroundColor: `var(--lip-type-${recommendation.category.toLowerCase()})`,
                opacity: 0.85,
              }}
            >
              {recommendation.category}
            </span>
            <span className="font-mono text-data-sm text-[var(--ink-muted)]">{hex}</span>
          </div>
          <div className="mt-3 flex items-center gap-2">
            <div className="h-1.5 flex-1 overflow-hidden rounded-full bg-white/60">
              <motion.div
                className="h-full rounded-full bg-[var(--primary)]"
                initial={{ width: 0 }}
                animate={{ width: `${Math.round(recommendation.score)}%` }}
                transition={{ duration: 0.8, delay: index * 0.1, ease: [0.16, 1, 0.3, 1] }}
              />
            </div>
            <span className="font-mono text-data-sm text-[var(--ink)]">
              {Math.round(recommendation.score)}%
            </span>
          </div>
        </div>
      </div>
    </motion.div>
  );
}
