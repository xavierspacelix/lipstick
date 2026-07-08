"use client";

import { useCallback, useState, useRef } from "react";
import { motion, AnimatePresence } from "motion/react";
import { Upload, X, Image as ImageIcon, AlertCircle } from "lucide-react";

const ACCEPTED_TYPES = ["image/jpeg", "image/jpg", "image/png"];
const MAX_SIZE = 10 * 1024 * 1024; // 10MB

interface UploadDropzoneProps {
  onFileSelect: (file: File) => void;
}

export function UploadDropzone({ onFileSelect }: UploadDropzoneProps) {
  const [dragOver, setDragOver] = useState(false);
  const [preview, setPreview] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const validateFile = useCallback((file: File) => {
    if (!ACCEPTED_TYPES.includes(file.type)) {
      setError("Only JPG, JPEG, and PNG files are accepted");
      return false;
    }
    if (file.size > MAX_SIZE) {
      setError("File size must be under 10MB");
      return false;
    }
    return true;
  }, []);

  const handleFile = useCallback(
    (file: File) => {
      setError(null);
      if (!validateFile(file)) return;
      const reader = new FileReader();
      reader.onload = (e) => {
        const dataUrl = e.target?.result as string;
        setPreview(dataUrl);
        onFileSelect(file);
      };
      reader.readAsDataURL(file);
    },
    [validateFile, onFileSelect],
  );

  const handleDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault();
      setDragOver(false);
      const file = e.dataTransfer.files[0];
      if (file) handleFile(file);
    },
    [handleFile],
  );

  const handleInput = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      const file = e.target.files?.[0];
      if (file) handleFile(file);
    },
    [handleFile],
  );

  const handleReset = useCallback(() => {
    setPreview(null);
    setError(null);
    if (inputRef.current) inputRef.current.value = "";
  }, []);

  return (
    <div className="w-full">
      <div
        onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
        onDragLeave={() => setDragOver(false)}
        onDrop={handleDrop}
        onClick={() => !preview && inputRef.current?.click()}
        className={`relative cursor-pointer rounded-[var(--radius-md)] border-2 border-dashed p-8 text-center transition-all duration-base ${
          dragOver
            ? "border-[var(--primary)] bg-[rgba(139,47,69,0.04)]"
            : preview
              ? "border-[var(--border-glass)] bg-white/60"
              : "border-[var(--border)] bg-white/40 hover:border-[var(--primary)]/50 hover:bg-white/60"
        }`}
        style={{
          background: dragOver
            ? "rgba(139, 47, 69, 0.04)"
            : preview
              ? undefined
              : undefined,
        }}
      >
        <input
          ref={inputRef}
          type="file"
          accept=".jpg,.jpeg,.png"
          className="hidden"
          onChange={handleInput}
        />

        <AnimatePresence mode="wait">
          {preview ? (
            <motion.div
              key="preview"
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.95 }}
              className="relative mx-auto max-w-xs"
            >
              <img
                src={preview}
                alt="Preview"
                className="max-h-64 w-full rounded-[var(--radius-sm)] object-contain"
              />
              <button
                onClick={(e) => { e.stopPropagation(); handleReset(); }}
                className="absolute -top-3 -right-3 flex h-7 w-7 items-center justify-center rounded-full bg-white shadow-md backdrop-blur-sm transition-all duration-base hover:scale-110"
              >
                <X className="h-4 w-4 text-[var(--ink-muted)]" />
              </button>
              <p className="mt-3 text-body-sm text-[var(--ink-muted)]">
                Tap to change photo
              </p>
            </motion.div>
          ) : (
            <motion.div
              key="empty"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
            >
              <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-[var(--radius-sm)] bg-white/80 shadow-sm backdrop-blur-sm">
                {dragOver ? (
                  <ImageIcon className="h-8 w-8 text-[var(--primary)]" />
                ) : (
                  <Upload className="h-8 w-8 text-[var(--primary)]" />
                )}
              </div>
              <p className="mt-5 font-display text-display-md text-[var(--ink)]">
                {dragOver ? "Drop your photo here" : "Upload a selfie"}
              </p>
              <p className="mt-2 text-body-sm text-[var(--ink-muted)]">
                Drag & drop or tap to browse
              </p>
              <p className="mt-1 text-body-sm text-[var(--ink-muted)]/60">
                JPG, JPEG, PNG &middot; Max 10MB
              </p>
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      <AnimatePresence>
        {error && (
          <motion.div
            initial={{ opacity: 0, y: -8 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -8 }}
            className="mt-3 flex items-center gap-2 rounded-[var(--radius-sm)] border border-[var(--error)]/20 bg-[var(--error)]/5 px-4 py-2"
          >
            <AlertCircle className="h-4 w-4 shrink-0 text-[var(--error)]" />
            <p className="text-body-sm text-[var(--error)]">{error}</p>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
