"use client";

import { motion } from "motion/react";
import { Palette, Globe, Bell } from "lucide-react";

const settings = [
  {
    icon: Palette,
    title: "Appearance",
    description: "Theme preferences are coming soon",
    disabled: true,
  },
  {
    icon: Globe,
    title: "Language",
    description: "English (default)",
    disabled: true,
  },
  {
    icon: Bell,
    title: "Notifications",
    description: "Notification preferences are coming soon",
    disabled: true,
  },
];

export default function SettingsPage() {
  return (
    <div className="mx-auto max-w-[640px] px-4 py-8">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <span className="inline-block rounded-full border border-[var(--border-glass)] bg-white/60 px-3 py-1 text-[11px] font-medium uppercase tracking-wider text-[var(--ink-muted)] backdrop-blur-sm">
          Settings
        </span>
        <h1 className="mt-4 font-display text-display-xl text-[var(--ink)]">Settings</h1>
        <p className="mt-2 text-body-lg text-[var(--ink-muted)]">
          Manage your preferences
        </p>
      </motion.div>

      <div className="mt-10 space-y-3">
        {settings.map((item, i) => {
          const Icon = item.icon;
          return (
            <motion.div
              key={item.title}
              initial={{ opacity: 0, y: 16 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.06, duration: 0.35 }}
              className="flex items-center gap-4 rounded-[var(--radius-md)] border border-[var(--border-glass)] bg-white/60 px-5 py-4 shadow-[var(--shadow-glass)] backdrop-blur-sm"
            >
              <div className="flex h-10 w-10 items-center justify-center rounded-[var(--radius-sm)] bg-white/80 shadow-sm backdrop-blur-sm">
                <Icon className="h-5 w-5 text-[var(--ink-muted)]" />
              </div>
              <div className="flex-1">
                <p className="text-body-md font-medium text-[var(--ink)]">{item.title}</p>
                <p className="text-body-sm text-[var(--ink-muted)]">{item.description}</p>
              </div>
              {item.disabled && (
                <span className="rounded-[var(--radius-full)] bg-[var(--border)]/50 px-2.5 py-0.5 text-[11px] font-medium uppercase tracking-wider text-[var(--ink-muted)]">
                  Soon
                </span>
              )}
            </motion.div>
          );
        })}
      </div>
    </div>
  );
}
