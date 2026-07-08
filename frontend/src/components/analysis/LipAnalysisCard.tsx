"use client";

import { motion } from "motion/react";

interface LipAnalysisCardProps {
  lipType: string;
  confidence: number;
  rgb: { r: number; g: number; b: number };
  className?: string;
}

export function LipAnalysisCard({ lipType, confidence, rgb, className = "" }: LipAnalysisCardProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, ease: [0.16, 1, 0.3, 1] }}
      className={`rounded-[var(--radius-md)] border border-[var(--border-glass)] bg-white/60 p-5 shadow-[var(--shadow-glass)] backdrop-blur-sm ${className}`}
    >
      <h4 className="font-display text-display-md text-[var(--ink)]">Lip Analysis</h4>
      <p className="text-body-sm text-[var(--ink-muted)]">What the AI detected</p>

      <div className="mt-5 space-y-4">
        {/* Lip type badge */}
        <div className="flex items-center justify-between">
          <span className="text-body-sm text-[var(--ink-muted)]">Lip Type</span>
          <span
            className="rounded-[var(--radius-full)] px-3 py-1 text-data-sm font-medium"
            style={{
              backgroundColor: `var(--lip-type-${lipType.toLowerCase()})`,
              color: "white",
              opacity: 0.9,
            }}
          >
            {lipType}
          </span>
        </div>

        {/* Confidence bar */}
        <div>
          <div className="flex items-center justify-between">
            <span className="text-body-sm text-[var(--ink-muted)]">Confidence</span>
            <span className="font-mono text-data-sm text-[var(--ink)]">
              {(confidence * 100).toFixed(0)}%
            </span>
          </div>
          <div className="mt-1.5 h-2 overflow-hidden rounded-full bg-white/60">
            <motion.div
              className="h-full rounded-full bg-[var(--primary)]"
              initial={{ width: 0 }}
              animate={{ width: `${confidence * 100}%` }}
              transition={{ duration: 0.8, ease: [0.16, 1, 0.3, 1] }}
            />
          </div>
        </div>

        {/* RGB swatch */}
        <div>
          <span className="text-body-sm text-[var(--ink-muted)]">Detected Color</span>
          <div className="mt-2 flex items-center gap-3">
            <div
              className="h-10 w-10 rounded-[var(--radius-sm)] border border-[var(--border)]"
              style={{ backgroundColor: `rgb(${rgb.r}, ${rgb.g}, ${rgb.b})` }}
            />
            <span className="font-mono text-data-md text-[var(--ink)]">
              rgb({rgb.r}, {rgb.g}, {rgb.b})
            </span>
          </div>
        </div>
      </div>
    </motion.div>
  );
}
