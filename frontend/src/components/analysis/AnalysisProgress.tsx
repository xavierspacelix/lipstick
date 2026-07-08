"use client";

import { motion } from "motion/react";
import { Scan, Scissors, Eye, Sparkles } from "lucide-react";

const steps = [
  { id: "detect", label: "Detecting face", icon: Scan },
  { id: "segment", label: "Segmenting lips", icon: Scissors },
  { id: "extract", label: "Extracting color", icon: Eye },
  { id: "recommend", label: "Generating recommendations", icon: Sparkles },
];

interface AnalysisProgressProps {
  currentStep: number;
  error?: string | null;
  progress?: number;
}

export function AnalysisProgress({ currentStep, error, progress }: AnalysisProgressProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="rounded-[var(--radius-md)] border border-[var(--border-glass)] bg-white/60 p-6 shadow-[var(--shadow-glass)] backdrop-blur-sm"
    >
      <h4 className="font-display text-display-md text-[var(--ink)]">Analyzing your photo</h4>
      <p className="text-body-sm text-[var(--ink-muted)]">
        This takes about 5 seconds
      </p>

      <div className="mt-6 space-y-4">
        {steps.map((step, i) => {
          const Icon = step.icon;
          const isActive = i === currentStep;
          const isDone = i < currentStep;
          const isPending = i > currentStep;

          return (
            <div key={step.id} className="flex items-center gap-4">
              {/* Icon */}
              <motion.div
                className={`flex h-9 w-9 shrink-0 items-center justify-center rounded-[var(--radius-sm)] transition-all duration-base ${
                  isDone
                    ? "bg-[var(--success)]/10 text-[var(--success)]"
                    : isActive
                      ? "bg-[var(--primary)]/10 text-[var(--primary)]"
                      : "bg-white/60 text-[var(--ink-muted)]"
                }`}
                animate={
                  isActive
                    ? { scale: [1, 1.1, 1] }
                    : {}
                }
                transition={{ repeat: isActive ? Infinity : 0, duration: 1.5 }}
              >
                {isDone ? (
                  <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
                    <path d="M5 13l4 4L19 7" />
                  </svg>
                ) : (
                  <Icon className="h-4 w-4" />
                )}
              </motion.div>

              {/* Label */}
              <div className="flex-1">
                <p
                  className={`text-body-sm font-medium ${
                    isDone
                      ? "text-[var(--success)]"
                      : isActive
                        ? "text-[var(--ink)]"
                        : "text-[var(--ink-muted)]"
                  }`}
                >
                  {step.label}
                  {isActive && (
                    <span className="ml-2 inline-block">
                      <span className="animate-pulse">...</span>
                    </span>
                  )}
                </p>
              </div>

              {/* Progress indicator */}
              <div className="flex items-center gap-2">
                {isDone && (
                  <span className="text-data-sm text-[var(--success)]">Done</span>
                )}
                {isActive && (
                  <motion.div
                    className="h-1.5 w-16 overflow-hidden rounded-full bg-white/60"
                  >
                    <motion.div
                      className="h-full rounded-full bg-[var(--primary)]"
                      animate={{ width: progress ? `${progress}%` : ["0%", "100%"] }}
                      transition={{
                        duration: progress ? 0.3 : 3,
                        repeat: progress ? 0 : Infinity,
                        ease: "easeInOut",
                      }}
                    />
                  </motion.div>
                )}
              </div>
            </div>
          );
        })}
      </div>

      {error && (
        <motion.div
          initial={{ opacity: 0, y: -8 }}
          animate={{ opacity: 1, y: 0 }}
          className="mt-4 rounded-[var(--radius-sm)] border border-[var(--error)]/20 bg-[var(--error)]/5 px-4 py-3"
        >
          <p className="text-body-sm text-[var(--error)]">{error}</p>
        </motion.div>
      )}
    </motion.div>
  );
}
