"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { motion } from "motion/react";
import Link from "next/link";
import { ArrowLeft, RefreshCw } from "lucide-react";
import { LipAnalysisCard } from "@/components/analysis/LipAnalysisCard";
import { RecommendationCard } from "@/components/analysis/RecommendationCard";
import { CroppedLipPreview } from "@/components/analysis/CroppedLipPreview";
import { apiClient } from "@/lib/api-client";
import type { AnalysisResult } from "@/types/analysis";

export default function AnalysisResultPage() {
  const params = useParams();
  const id = params.id as string;
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchResult() {
      try {
        const data = await apiClient<AnalysisResult>(`/api/v1/analysis/${id}`);
        setResult(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to load result");
      } finally {
        setLoading(false);
      }
    }
    fetchResult();
  }, [id]);

  if (loading) {
    return (
      <div className="mx-auto max-w-[1120px] px-4 py-8">
        <div className="flex items-center justify-center py-32">
          <motion.div
            animate={{ rotate: 360 }}
            transition={{ duration: 1.5, repeat: Infinity, ease: "linear" }}
          >
            <RefreshCw className="h-6 w-6 text-[var(--primary)]" />
          </motion.div>
        </div>
      </div>
    );
  }

  if (error || !result) {
    return (
      <div className="mx-auto max-w-[1120px] px-4 py-8">
        <div className="rounded-[var(--radius-md)] border border-[var(--error)]/20 bg-[var(--error)]/5 p-6 text-center">
          <p className="text-body-md text-[var(--error)]">{error ?? "Analysis not found"}</p>
          <Link
            href="/analysis"
            className="mt-4 inline-flex items-center gap-2 text-body-sm font-medium text-[var(--primary)]"
          >
            Try again
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-[1120px] px-4 py-8">
      {/* Back + header */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4, ease: [0.16, 1, 0.3, 1] }}
        className="space-y-6"
      >
        <Link
          href="/analysis"
          className="mb-2 inline-flex items-center gap-1.5 text-body-sm text-[var(--ink-muted)] no-underline transition-colors hover:text-[var(--ink)]"
        >
          <ArrowLeft className="h-4 w-4" />
          New Analysis
        </Link>

        <span className="inline-block rounded-full border border-[var(--border-glass)] bg-white/60 px-3 py-1 text-[11px] font-medium uppercase tracking-wider text-[var(--ink-muted)] backdrop-blur-sm">
          Results
        </span>
        <h1 className="font-display text-display-xl text-[var(--ink)]">
          Your Perfect Shades
        </h1>
        <p className="text-body-lg text-[var(--ink-muted)]">
          Based on your lip analysis, here are your top three matches.
        </p>
      </motion.div>

      {/* Two-column layout */}
      <div className="mt-10 grid gap-6 lg:grid-cols-3">
        {/* Left sidebar - analysis details */}
        <div className="space-y-6 lg:col-span-1">
          <CroppedLipPreview
            imageUrl={result.cropped_lip_image_url}
            brushedImageUrl={result.brushed_lip_image_url}
            rgb={result.rgb}
          />
          <LipAnalysisCard
            lipType={result.lip_type}
            confidence={result.confidence}
            rgb={result.rgb}
          />

          {/* Original image link */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3, duration: 0.4 }}
            className="overflow-hidden rounded-[var(--radius-md)] border border-[var(--border-glass)] bg-white/60 shadow-[var(--shadow-glass)] backdrop-blur-sm"
          >
            <img
              src={result.original_image_url}
              alt="Original"
              className="w-full object-contain"
            />
            <div className="px-4 py-3">
              <p className="text-body-sm text-[var(--ink-muted)]">Original photo</p>
            </div>
          </motion.div>
        </div>

        {/* Right - recommendations */}
        <div className="space-y-4 lg:col-span-2">
          <motion.h2
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1, duration: 0.4 }}
            className="font-display text-display-lg text-[var(--ink)]"
          >
            Top 3 Recommendations
          </motion.h2>

          {result.recommendations.map((rec, i) => (
            <RecommendationCard key={rec.shade_name} recommendation={rec} index={i} />
          ))}
        </div>
      </div>
    </div>
  );
}
