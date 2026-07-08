"use client";

import { useEffect, useRef, useCallback } from "react";
import Lenis from "lenis";

export function SmoothScroll({ children }: { children: React.ReactNode }) {
  const lenisRef = useRef<Lenis | null>(null);

  useEffect(() => {
    const lenis = new Lenis({
      duration: 1.2,
      easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
      orientation: "vertical",
      smoothWheel: true,
    });

    lenisRef.current = lenis;

    function raf(time: number) {
      lenis.raf(time);
      requestAnimationFrame(raf);
    }

    requestAnimationFrame(raf);

    return () => {
      lenis.destroy();
      lenisRef.current = null;
    };
  }, []);

  return <div data-lenis-container>{children}</div>;
}

export function useLenis() {
  const resize = useCallback(() => {
    if (typeof window !== "undefined" && (window as any).__lenis) {
      (window as any).__lenis.resize();
    }
  }, []);

  return { resize };
}
