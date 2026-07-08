"use client";

import { useEffect, useRef } from "react";

const COLORS = [
  "rgba(140, 47, 69, 0.08)",
  "rgba(201, 164, 106, 0.06)",
  "rgba(219, 112, 147, 0.05)",
  "rgba(255, 255, 255, 0.4)",
];

interface Orb {
  x: number;
  y: number;
  vx: number;
  vy: number;
  size: number;
  color: string;
  blur: number;
}

export function AmbientBackground() {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    let animId: number;

    const resize = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    };
    resize();
    window.addEventListener("resize", resize);

    const orbs: Orb[] = Array.from({ length: 6 }, (_, i) => ({
      x: Math.random() * canvas.width,
      y: Math.random() * canvas.height,
      vx: (Math.random() - 0.5) * 0.3,
      vy: (Math.random() - 0.5) * 0.3,
      size: 200 + Math.random() * 300,
      color: COLORS[i % COLORS.length],
      blur: 80 + Math.random() * 60,
    }));

    function draw() {
      ctx!.clearRect(0, 0, canvas!.width, canvas!.height);

      for (const orb of orbs) {
        orb.x += orb.vx;
        orb.y += orb.vy;

        if (orb.x < -orb.size) orb.x = canvas!.width + orb.size;
        if (orb.x > canvas!.width + orb.size) orb.x = -orb.size;
        if (orb.y < -orb.size) orb.y = canvas!.height + orb.size;
        if (orb.y > canvas!.height + orb.size) orb.y = -orb.size;

        ctx!.save();
        ctx!.filter = `blur(${orb.blur}px)`;
        ctx!.beginPath();
        ctx!.arc(orb.x, orb.y, orb.size / 2, 0, Math.PI * 2);
        ctx!.fillStyle = orb.color;
        ctx!.fill();
        ctx!.restore();
      }

      animId = requestAnimationFrame(draw);
    }

    draw();

    return () => {
      cancelAnimationFrame(animId);
      window.removeEventListener("resize", resize);
    };
  }, []);

  return (
    <canvas
      ref={canvasRef}
      className="pointer-events-none fixed inset-0 z-0"
      style={{ width: "100vw", height: "100vh" }}
    />
  );
}
