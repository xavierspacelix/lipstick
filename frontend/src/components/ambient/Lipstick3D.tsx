"use client";

import { useRef, useState, useEffect } from "react";
import { motion, useMotionValue, useSpring } from "motion/react";

type LipstickColor = "primary" | "pinkish" | "brownish" | "dark";

interface Lipstick3DProps {
  color?: LipstickColor;
  className?: string;
}

const COLOR_MAP: Record<LipstickColor, { body: string; cap: string; bullet: string }> = {
  primary: {
    body: "#8C2F45",
    cap: "#C9A46A",
    bullet: "#B84A5C",
  },
  pinkish: {
    body: "#E1849C",
    cap: "#C9A46A",
    bullet: "#E1849C",
  },
  brownish: {
    body: "#9C6B4F",
    cap: "#C9A46A",
    bullet: "#9C6B4F",
  },
  dark: {
    body: "#4A1F2B",
    cap: "#C9A46A",
    bullet: "#4A1F2B",
  },
};

export function Lipstick3D({ color = "primary", className = "" }: Lipstick3DProps) {
  const ref = useRef<HTMLDivElement>(null);
  const [mouseInside, setMouseInside] = useState(false);

  const rotateX = useMotionValue(0);
  const rotateY = useMotionValue(0);

  const springRotateX = useSpring(rotateX, { stiffness: 200, damping: 30 });
  const springRotateY = useSpring(rotateY, { stiffness: 200, damping: 30 });

  function handleMouse(e: React.MouseEvent) {
    if (!ref.current) return;
    const rect = ref.current.getBoundingClientRect();
    const centerX = rect.left + rect.width / 2;
    const centerY = rect.top + rect.height / 2;
    const deltaX = (e.clientX - centerX) / (rect.width / 2);
    const deltaY = (e.clientY - centerY) / (rect.height / 2);
    rotateY.set(deltaX * 15);
    rotateX.set(-deltaY * 15);
  }

  function handleLeave() {
    rotateX.set(0);
    rotateY.set(0);
    setMouseInside(false);
  }

  const colors = COLOR_MAP[color];

  return (
    <motion.div
      ref={ref}
      onMouseMove={handleMouse}
      onMouseEnter={() => setMouseInside(true)}
      onMouseLeave={handleLeave}
      className={`perspective-[800px] ${className}`}
      initial={{ opacity: 0, y: 60 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 1.2, ease: [0.16, 1, 0.3, 1] }}
    >
      <motion.div
        className="relative cursor-pointer"
        style={{
          rotateX: springRotateX,
          rotateY: springRotateY,
          transformStyle: "preserve-3d",
        }}
      >
        <svg
          viewBox="0 0 200 500"
          className="h-auto w-full drop-shadow-2xl"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          <defs>
            <linearGradient id={`body-grad-${color}`} x1="0" y1="0" x2="1" y2="0">
              <stop offset="0%" stopColor={colors.body} stopOpacity="0.85" />
              <stop offset="30%" stopColor={colors.body} stopOpacity="1" />
              <stop offset="70%" stopColor={colors.body} stopOpacity="1" />
              <stop offset="100%" stopColor={colors.body} stopOpacity="0.8" />
            </linearGradient>
            <linearGradient id={`cap-grad-${color}`} x1="0" y1="0" x2="1" y2="0">
              <stop offset="0%" stopColor={colors.cap} stopOpacity="0.7" />
              <stop offset="30%" stopColor={colors.cap} stopOpacity="1" />
              <stop offset="70%" stopColor={colors.cap} stopOpacity="1" />
              <stop offset="100%" stopColor={colors.cap} stopOpacity="0.6" />
            </linearGradient>
            <linearGradient id={`bullet-grad-${color}`} x1="0" y1="0" x2="1" y2="0">
              <stop offset="0%" stopColor={colors.bullet} stopOpacity="0.9" />
              <stop offset="30%" stopColor={colors.bullet} stopOpacity="1" />
              <stop offset="70%" stopColor={colors.bullet} stopOpacity="1" />
              <stop offset="100%" stopColor={colors.bullet} stopOpacity="0.85" />
            </linearGradient>
            <radialGradient id={`shine-${color}`} cx="0.3" cy="0.3" r="0.5">
              <stop offset="0%" stopColor="white" stopOpacity="0.25" />
              <stop offset="100%" stopColor="white" stopOpacity="0" />
            </radialGradient>
            <linearGradient id={`metal-${color}`} x1="0" y1="0" x2="1" y2="0">
              <stop offset="0%" stopColor="#C9A46A" />
              <stop offset="20%" stopColor="#F5E6C8" />
              <stop offset="40%" stopColor="#C9A46A" />
              <stop offset="60%" stopColor="#F5E6C8" />
              <stop offset="80%" stopColor="#D4AF70" />
              <stop offset="100%" stopColor="#B8955A" />
            </linearGradient>
          </defs>

          {/* Shadow under lipstick */}
          <ellipse cx="100" cy="485" rx="30" ry="6" fill="rgba(0,0,0,0.1)" />

          {/* Body - main cylinder */}
          <rect x="70" y="220" width="60" height="220" rx="4" fill={`url(#body-grad-${color})`} />
          <rect x="70" y="220" width="60" height="220" rx="4" fill={`url(#shine-${color})`} />

          {/* Body label area */}
          <rect x="75" y="260" width="50" height="2" rx="1" fill="rgba(255,255,255,0.15)" />
          <rect x="78" y="270" width="44" height="1" rx="0.5" fill="rgba(255,255,255,0.1)" />
          <rect x="75" y="380" width="50" height="2" rx="1" fill="rgba(255,255,255,0.15)" />

          {/* Metal band - bottom */}
          <rect x="68" y="430" width="64" height="12" rx="2" fill={`url(#metal-${color})`} />
          <rect x="68" y="430" width="64" height="3" rx="1" fill="rgba(255,255,255,0.2)" />

          {/* Metal band - top */}
          <rect x="68" y="200" width="64" height="14" rx="2" fill={`url(#metal-${color})`} />
          <rect x="68" y="200" width="64" height="3" rx="1" fill="rgba(255,255,255,0.2)" />

          {/* Bullet - lipstick exposed */}
          <path
            d="M70 200 Q70 160 100 140 Q130 160 130 200Z"
            fill={`url(#bullet-grad-${color})`}
          />
          {/* Bullet tip cut */}
          <ellipse cx="100" cy="145" rx="18" ry="8" fill={colors.bullet} opacity="0.6" />
          <path
            d="M70 200 Q70 160 100 140 Q130 160 130 200Z"
            fill={`url(#shine-${color})`}
          />

          {/* Highlight streak on bullet */}
          <path
            d="M80 195 Q82 165 95 150"
            stroke="rgba(255,255,255,0.15)"
            strokeWidth="2"
            fill="none"
            strokeLinecap="round"
          />

          {/* Cap - top */}
          <rect x="65" y="30" width="70" height="170" rx="12" fill={`url(#cap-grad-${color})`} />
          <rect x="65" y="30" width="70" height="170" rx="12" fill={`url(#shine-${color})`} />

          {/* Cap dome */}
          <path d="M65 40 Q65 12 100 8 Q135 12 135 40Z" fill={colors.cap} />
          <path d="M65 40 Q65 12 100 8 Q135 12 135 40Z" fill="url(#shine)" opacity="0.3" />

          {/* Cap bottom rim */}
          <rect x="64" y="195" width="72" height="5" rx="2" fill={`url(#metal-${color})`} />
        </svg>
      </motion.div>
    </motion.div>
  );
}
