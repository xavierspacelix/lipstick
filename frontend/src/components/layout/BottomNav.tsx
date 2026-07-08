"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { motion } from "motion/react";
import { LayoutDashboard, ScanLine, History, User, Palette } from "lucide-react";

const navItems = [
  { href: "/dashboard", label: "Dashboard", icon: LayoutDashboard },
  { href: "/analysis", label: "Analyze", icon: ScanLine },
  { href: "/shades", label: "Shades", icon: Palette },
  { href: "/history", label: "History", icon: History },
  { href: "/profile", label: "Profile", icon: User },
];

export function BottomNav() {
  const pathname = usePathname();

  return (
    <nav className="fixed bottom-4 left-1/2 z-50 -translate-x-1/2 md:hidden">
      <div className="flex items-center gap-1 rounded-[var(--radius-md)] border border-[var(--border-glass)] bg-white/70 px-3 py-2 shadow-[var(--shadow-glass)] backdrop-blur-xl">
        {navItems.map((item) => {
          const isActive = pathname.startsWith(item.href);
          const Icon = item.icon;
          return (
            <motion.div
              key={item.href}
              whileHover={{ scale: 1.1 }}
              whileTap={{ scale: 0.9 }}
            >
              <Link
                href={item.href}
                className="relative flex flex-col items-center gap-0.5 rounded-[var(--radius-sm)] px-4 py-2 no-underline"
              >
                {isActive && (
                  <motion.span
                    layoutId="bottom-nav-active"
                    className="absolute inset-0 rounded-[var(--radius-sm)]"
                    style={{ background: "rgba(139, 47, 69, 0.08)" }}
                    transition={{ type: "spring", stiffness: 380, damping: 30 }}
                  />
                )}
                <Icon
                  className="relative h-5 w-5"
                  style={{
                    color: isActive ? "var(--primary)" : "var(--ink-muted)",
                    fill: isActive ? "var(--primary)" : "none",
                  }}
                />
                <span
                  className="relative text-[10px] font-medium"
                  style={{
                    color: isActive ? "var(--primary)" : "var(--ink-muted)",
                  }}
                >
                  {item.label}
                </span>
              </Link>
            </motion.div>
          );
        })}
      </div>
    </nav>
  );
}
