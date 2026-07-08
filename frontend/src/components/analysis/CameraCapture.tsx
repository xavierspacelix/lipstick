"use client";

import { useRef, useState, useCallback, useEffect } from "react";
import { motion } from "motion/react";
import { Camera, FlipHorizontal, X } from "lucide-react";

interface CameraCaptureProps {
  onCapture: (blob: Blob) => void;
  onClose: () => void;
}

export function CameraCapture({ onCapture, onClose }: CameraCaptureProps) {
  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const streamRef = useRef<MediaStream | null>(null);
  const [facingMode, setFacingMode] = useState<"user" | "environment">("user");
  const [error, setError] = useState<string | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [cameraReady, setCameraReady] = useState(false);

  const startCamera = useCallback(async (mode: string) => {
    setError(null);
    setCameraReady(false);
    try {
      if (streamRef.current) {
        streamRef.current.getTracks().forEach((t) => t.stop());
        streamRef.current = null;
      }
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: mode, width: { ideal: 1280 }, height: { ideal: 720 } },
        audio: false,
      });
      streamRef.current = stream;
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        videoRef.current.onloadedmetadata = () => {
          videoRef.current?.play();
          setCameraReady(true);
        };
      }
    } catch {
      setError("Camera access denied. Allow camera permissions and try again.");
    }
  }, []);

  // Start camera on mount and when facingMode changes
  useEffect(() => { startCamera(facingMode); }, [facingMode, startCamera]);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      if (streamRef.current) {
        streamRef.current.getTracks().forEach((t) => t.stop());
        streamRef.current = null;
      }
    };
  }, []);

  const capture = useCallback(() => {
    const video = videoRef.current;
    const canvas = canvasRef.current;
    if (!video || !canvas) return;

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    ctx.drawImage(video, 0, 0);
    canvas.toBlob(
      (blob) => {
        if (blob) {
          setPreview(canvas.toDataURL("image/jpeg"));
          onCapture(blob);
        }
      },
      "image/jpeg",
      0.9,
    );
  }, [onCapture]);

  const toggleCamera = useCallback(() => {
    setFacingMode((prev) => (prev === "user" ? "environment" : "user"));
  }, []);

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm"
    >
      <div className="relative mx-4 w-full max-w-md overflow-hidden rounded-[var(--radius-lg)] bg-[var(--background)] shadow-2xl">
        {/* Header */}
        <div className="flex items-center justify-between border-b border-[var(--border)]/50 px-4 py-3">
          <h3 className="font-display text-display-md text-[var(--ink)]">Take a Photo</h3>
          <button
            onClick={onClose}
            className="flex h-8 w-8 items-center justify-center rounded-[var(--radius-sm)] text-[var(--ink-muted)] transition-colors hover:bg-white/60"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        {/* Camera / Preview */}
        <div className="relative aspect-[3/4] bg-black">
          {preview ? (
            <img src={preview} alt="Captured" className="h-full w-full object-cover" />
          ) : (
            <video
              ref={videoRef}
              autoPlay
              playsInline
              muted
              className="h-full w-full object-cover"
            />
          )}
          <canvas ref={canvasRef} className="hidden" />

          {error && (
            <div className="absolute inset-0 flex items-center justify-center bg-black/60 p-6 text-center">
              <p className="text-body-sm text-white">{error}</p>
            </div>
          )}
        </div>

        {/* Controls */}
        <div className="flex items-center justify-center gap-8 px-4 py-5">
          {preview ? (
            <div className="flex gap-4">
              <button
                onClick={() => { setPreview(null); startCamera(facingMode); }}
                className="rounded-[var(--radius-sm)] border border-[var(--border)] bg-white/60 px-5 py-2 text-body-sm font-medium text-[var(--ink)] backdrop-blur-sm transition-colors hover:bg-white/80"
              >
                Retake
              </button>
              <button
                onClick={onClose}
                className="rounded-[var(--radius-sm)] bg-[var(--primary)] px-5 py-2 text-body-sm font-medium text-[var(--primary-foreground)] transition-colors hover:brightness-110"
              >
                Use Photo
              </button>
            </div>
          ) : (
            <>
              <button
                onClick={toggleCamera}
                className="flex h-12 w-12 items-center justify-center rounded-full border border-[var(--border)] bg-white/60 text-[var(--ink-muted)] backdrop-blur-sm transition-colors hover:bg-white/80"
              >
                <FlipHorizontal className="h-5 w-5" />
              </button>
              <button
                onClick={capture}
                className="flex h-16 w-16 items-center justify-center rounded-full border-4 border-white bg-white/20 transition-colors hover:bg-white/30"
              >
                <Camera className="h-8 w-8 text-white" />
              </button>
              <div className="w-12" /> {/* spacer for symmetry */}
            </>
          )}
        </div>
      </div>
    </motion.div>
  );
}
