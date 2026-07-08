"use client";

import { useState } from "react";
import { motion } from "motion/react";

interface CroppedLipPreviewProps {
  imageUrl?: string;
  brushedImageUrl?: string | null;
  rgb?: { r: number; g: number; b: number };
  className?: string;
}

export function CroppedLipPreview({ imageUrl, brushedImageUrl, rgb, className = "" }: CroppedLipPreviewProps) {
  const [showBrushed, setShowBrushed] = useState(false);

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.4, ease: [0.16, 1, 0.3, 1] }}
      className={`rounded-[var(--radius-md)] border border-[var(--border-glass)] bg-white/60 p-4 shadow-[var(--shadow-glass)] backdrop-blur-sm ${className}`}
    >
      <div className="flex items-center justify-between">
        <div>
          <h4 className="font-display text-display-md text-[var(--ink)]">Extracted Lip Region</h4>
          <p className="text-body-sm text-[var(--ink-muted)]">Segmented by AI</p>
        </div>
        {brushedImageUrl && (
          <button
            onClick={() => setShowBrushed((prev) => !prev)}
            className="rounded-[var(--radius-sm)] border border-[var(--border)] bg-white/60 px-3 py-1.5 text-[11px] font-medium uppercase tracking-wider text-[var(--ink-muted)] backdrop-blur-sm transition-colors hover:bg-white/80"
          >
            {showBrushed ? "Original" : "Try-On"}
          </button>
        )}
      </div>

      <div className="mt-4 overflow-hidden rounded-[var(--radius-sm)] bg-white/80">
        {showBrushed && brushedImageUrl ? (
          <img
            src={brushedImageUrl}
            alt="Lip with top shade applied"
            className="w-full object-contain"
          />
        ) : imageUrl ? (
          <img
            src={imageUrl}
            alt="Cropped lip"
            className="w-full object-contain"
          />
        ) : (
          <div className="flex aspect-[4/3] items-center justify-center">
            <p className="text-body-sm text-[var(--ink-muted)]">No preview available</p>
          </div>
        )}
      </div>

      {rgb && (
        <div className="mt-4 flex items-center gap-3">
          <div
            className="h-8 w-8 rounded-[var(--radius-sm)] border border-[var(--border)]"
            style={{ backgroundColor: `rgb(${rgb.r}, ${rgb.g}, ${rgb.b})` }}
          />
          <div className="font-mono text-data-sm text-[var(--ink-muted)]">
            RGB({rgb.r}, {rgb.g}, {rgb.b})
          </div>
        </div>
      )}
    </motion.div>
  );
}
