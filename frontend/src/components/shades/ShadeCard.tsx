"use client";

import type { Lipstick } from "@/types";

const categoryGradients: Record<string, string> = {
  Red: "from-[#e74c3c] to-[#c0392b]",
  Berry: "from-[#8e44ad] to-[#6c3483]",
  Pink: "from-[#f472b6] to-[#db2777]",
  Coral: "from-[#f97316] to-[#ea580c]",
  Nude: "from-[#d4a574] to-[#b88863]",
  Brown: "from-[#8b6914] to-[#6b4c1a]",
  Mauve: "from-[#c9a0dc] to-[#a876c9]",
  Plum: "from-[#6b21a8] to-[#581c87]",
};

export function ShadeCard({ lipstick }: { lipstick: Lipstick }) {
  const grad = categoryGradients[lipstick.category] ?? "from-gray-400 to-gray-500";

  return (
    <div className="group rounded-[var(--radius-md)] border border-[var(--border-glass)] bg-white/60 p-4 shadow-[var(--shadow-glass)] backdrop-blur-sm transition-all duration-300 hover:bg-white/80 hover:shadow-lg">
      {/* Swatch */}
      <div
        className={`h-24 w-full rounded-[var(--radius-sm)] bg-gradient-to-br ${grad} relative overflow-hidden`}
      >
        <div
          className="absolute inset-0 opacity-60 mix-blend-multiply"
          style={{
            backgroundColor: `rgb(${lipstick.rgb.r}, ${lipstick.rgb.g}, ${lipstick.rgb.b})`,
          }}
        />
        <div className="absolute bottom-2 right-2 rounded-full border-2 border-white/60 shadow-sm"
          style={{
            width: 24,
            height: 24,
            backgroundColor: `rgb(${lipstick.rgb.r}, ${lipstick.rgb.g}, ${lipstick.rgb.b})`,
          }}
        />
      </div>

      {/* Info */}
      <div className="mt-3 space-y-1.5">
        <h3 className="font-display text-body-sm font-semibold text-[var(--ink)]">
          {lipstick.shade_name}
        </h3>
        <div className="flex items-center justify-between">
          <span className="text-[11px] uppercase tracking-wider text-[var(--ink-muted)]">
            {lipstick.category}
          </span>
          <span className="rounded-full bg-white/70 px-2 py-0.5 text-[10px] font-medium text-[var(--primary)] shadow-sm">
            {lipstick.lip_type_tag}
          </span>
        </div>
      </div>
    </div>
  );
}
