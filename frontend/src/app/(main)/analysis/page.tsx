"use client";

import { useState, useCallback, useRef } from "react";
import { useRouter } from "next/navigation";
import { motion, AnimatePresence } from "motion/react";
import { Camera, Plus, X } from "lucide-react";
import { CameraCapture } from "@/components/analysis/CameraCapture";
import { AnalysisProgress } from "@/components/analysis/AnalysisProgress";

type FlowState = "upload" | "analyzing" | "done" | "error";

const MAX_PHOTOS = 3;

export default function AnalysisPage() {
  const router = useRouter();
  const [files, setFiles] = useState<File[]>([]);
  const [previews, setPreviews] = useState<string[]>([]);
  const [state, setState] = useState<FlowState>("upload");
  const [step, setStep] = useState(0);
  const [error, setError] = useState<string | null>(null);
  const [showCamera, setShowCamera] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const addFiles = useCallback((newFiles: FileList | File[]) => {
    const remaining = MAX_PHOTOS - files.length;
    const toAdd = Array.from(newFiles).slice(0, remaining);
    setFiles((prev) => [...prev, ...toAdd]);
    for (const f of toAdd) {
      const url = URL.createObjectURL(f);
      setPreviews((prev) => [...prev, url]);
    }
  }, [files.length]);

  const removeFile = useCallback((index: number) => {
    setFiles((prev) => prev.filter((_, i) => i !== index));
    setPreviews((prev) => {
      URL.revokeObjectURL(prev[index]);
      return prev.filter((_, i) => i !== index);
    });
  }, []);

  const handleCameraCapture = useCallback((blob: Blob) => {
    if (files.length >= MAX_PHOTOS) return;
    const f = new File([blob], `camera-${Date.now()}.jpg`, { type: "image/jpeg" });
    setFiles((prev) => [...prev, f]);
    setPreviews((prev) => [...prev, URL.createObjectURL(f)]);
    setShowCamera(false);
  }, [files.length]);

  const handleSubmit = useCallback(async () => {
    if (files.length === 0) return;
    setState("analyzing");
    setStep(0);
    setError(null);

    try {
      const progressInterval = setInterval(() => {
        setStep((prev) => Math.min(prev + 1, 3));
      }, 900);

      const formData = new FormData();
      for (const f of files) {
        formData.append("images", f);
      }

      const res = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/api/v1/analysis`,
        {
          method: "POST",
          credentials: "include",
          body: formData,
        },
      );

      clearInterval(progressInterval);

      if (!res.ok) {
        const err = await res.json().catch(() => ({ detail: "Analysis failed" }));
        throw new Error(err.detail ?? "Analysis failed");
      }

      const data = await res.json();
      setState("done");
      router.push(`/analysis/${data.id}`);
    } catch (err) {
      setState("error");
      setError(err instanceof Error ? err.message : "Something went wrong");
    }
  }, [files, router]);

  const handleReset = useCallback(() => {
    for (const p of previews) URL.revokeObjectURL(p);
    setFiles([]);
    setPreviews([]);
    setState("upload");
    setStep(0);
    setError(null);
  }, [previews]);

  return (
    <div className="mx-auto max-w-[640px] px-4 py-8">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
      >
        <span className="inline-block rounded-full border border-[var(--border-glass)] bg-white/60 px-3 py-1 text-[11px] font-medium uppercase tracking-wider text-[var(--ink-muted)] backdrop-blur-sm">
          Analysis
        </span>
        <h1 className="mt-4 font-display text-display-xl text-[var(--ink)]">
          Find Your Shade
        </h1>
        <p className="mt-2 text-body-lg text-[var(--ink-muted)]">
          Add up to 3 front-facing selfies with bare lips for better accuracy.
        </p>
      </motion.div>

      {/* Upload area */}
      <div className="mt-8">
        {state === "upload" && (
          <motion.div
            key="upload"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="space-y-4"
          >
            {/* Hidden file input */}
            <input
              ref={fileInputRef}
              type="file"
              accept="image/jpeg,image/png"
              multiple
              className="hidden"
              onChange={(e) => e.target.files && addFiles(e.target.files)}
            />

            {/* Photo slots */}
            <div className="grid grid-cols-3 gap-3">
              {Array.from({ length: MAX_PHOTOS }).map((_, i) => {
                const filled = i < files.length;
                return (
                  <motion.button
                    key={i}
                    onClick={() => filled ? null : fileInputRef.current?.click()}
                    whileHover={filled ? undefined : { scale: 1.02 }}
                    whileTap={filled ? undefined : { scale: 0.98 }}
                    className="relative aspect-[3/4] overflow-hidden rounded-[var(--radius-md)] border-2 border-dashed border-[var(--border)] bg-white/40 backdrop-blur-sm transition-all"
                    style={{
                      borderColor: filled ? "var(--primary)" : "var(--border)",
                      borderStyle: filled ? "solid" : "dashed",
                    }}
                  >
                    {filled ? (
                      <>
                        <img
                          src={previews[i]}
                          alt={`Photo ${i + 1}`}
                          className="h-full w-full object-cover"
                        />
                        <button
                          onClick={(e) => { e.stopPropagation(); removeFile(i); }}
                          className="absolute right-1.5 top-1.5 flex h-6 w-6 items-center justify-center rounded-full bg-black/50 text-white backdrop-blur-sm transition-colors hover:bg-black/70"
                        >
                          <X className="h-3.5 w-3.5" />
                        </button>
                        {i === 0 && (
                          <span className="absolute bottom-1.5 left-1.5 rounded-full bg-[var(--primary)]/80 px-2 py-0.5 text-[10px] font-medium text-white backdrop-blur-sm">
                            Primary
                          </span>
                        )}
                      </>
                    ) : (
                      <div className="flex h-full flex-col items-center justify-center gap-1 text-[var(--ink-muted)]">
                        <Plus className="h-6 w-6" />
                        <span className="text-[11px] font-medium">Photo {i + 1}</span>
                      </div>
                    )}
                  </motion.button>
                );
              })}
            </div>

            {/* Add more + Camera */}
            <div className="flex gap-3">
              {files.length < MAX_PHOTOS && (
                <button
                  onClick={() => fileInputRef.current?.click()}
                  className="flex flex-1 items-center justify-center gap-2 rounded-[var(--radius-md)] border-2 border-dashed border-[var(--border)] bg-white/40 px-4 py-3 text-body-sm font-medium text-[var(--ink-muted)] backdrop-blur-sm transition-all hover:border-[var(--primary)]/50 hover:bg-white/60"
                >
                  <Plus className="h-4 w-4" />
                  Add Photo
                </button>
              )}
              {files.length < MAX_PHOTOS && (
                <button
                  onClick={() => setShowCamera(true)}
                  className="flex flex-1 items-center justify-center gap-2 rounded-[var(--radius-md)] border-2 border-dashed border-[var(--border)] bg-white/40 px-4 py-3 text-body-sm font-medium text-[var(--ink-muted)] backdrop-blur-sm transition-all hover:border-[var(--primary)]/50 hover:bg-white/60"
                >
                  <Camera className="h-4 w-4" />
                  Camera
                </button>
              )}
            </div>

            {/* Submit */}
            {files.length > 0 && (
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className="flex items-center justify-between rounded-[var(--radius-sm)] border border-[var(--border-glass)] bg-white/60 px-4 py-3 shadow-[var(--shadow-glass)] backdrop-blur-sm"
              >
                <span className="text-body-sm text-[var(--ink-muted)]">
                  {files.length} of {MAX_PHOTOS} photo{files.length > 1 ? "s" : ""}
                </span>
                <button
                  onClick={handleSubmit}
                  className="inline-flex h-9 items-center gap-2 rounded-[var(--radius-sm)] bg-[var(--primary)] px-4 text-body-sm font-medium text-[var(--primary-foreground)] transition-all duration-base hover:brightness-110"
                >
                  Analyze Photos
                </button>
              </motion.div>
            )}
          </motion.div>
        )}

        {/* Progress */}
        {(state === "analyzing" || state === "error") && (
          <motion.div
            key="progress"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="space-y-6"
          >
            <AnalysisProgress currentStep={step} error={error} />
            {state === "error" && (
              <div className="flex justify-center">
                <button
                  onClick={handleReset}
                  className="rounded-[var(--radius-sm)] px-4 py-2 text-body-sm font-medium text-[var(--ink-muted)] transition-all duration-base hover:bg-white/60"
                >
                  Try again
                </button>
              </div>
            )}
          </motion.div>
        )}
      </div>

      {/* Camera modal */}
      <AnimatePresence>
        {showCamera && (
          <CameraCapture
            onCapture={handleCameraCapture}
            onClose={() => setShowCamera(false)}
          />
        )}
      </AnimatePresence>
    </div>
  );
}
