"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { motion } from "motion/react";
import { LayoutDashboard, ScanLine, History, User, LogOut, Palette } from "lucide-react";
import { useAuth } from "@/context/auth";

const navItems = [
  { href: "/dashboard", label: "Dashboard", icon: LayoutDashboard },
  { href: "/analysis", label: "Analyze", icon: ScanLine },
  { href: "/shades", label: "Shades", icon: Palette },
  { href: "/history", label: "History", icon: History },
  { href: "/profile", label: "Profile", icon: User },
];

export function Navbar() {
  const pathname = usePathname();
  const { user, logout } = useAuth();

  return (
    <header className="fixed top-4 left-1/2 z-50 -translate-x-1/2">
      <div className="flex h-12 items-center justify-between gap-4 rounded-[var(--radius-md)] border border-[var(--border-glass)] bg-white/70 px-4 shadow-[var(--shadow-glass)] backdrop-blur-xl md:h-14 md:gap-6 md:px-5">
        <Link
          href="/dashboard"
          className="shrink-0 font-display text-base md:text-display-md text-[var(--primary)] no-underline"
        >
          Lipstick AI
        </Link>

        <nav className="hidden items-center justify-center gap-1 md:flex md:flex-1">
          {navItems.map((item) => {
            const isActive = pathname.startsWith(item.href);
            return (
              <motion.div
                key={item.href}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                <Link
                  href={item.href}
                  className="relative flex items-center gap-2 rounded-[var(--radius-sm)] px-3 py-2 text-body-sm font-medium no-underline transition-all duration-fast"
                  style={{
                    color: isActive ? "var(--primary)" : "var(--ink-muted)",
                  }}
                >
                  {isActive && (
                    <motion.span
                      layoutId="nav-active"
                      className="absolute inset-0 rounded-[var(--radius-sm)]"
                      style={{ background: "rgba(139, 47, 69, 0.08)" }}
                      transition={{ type: "spring", stiffness: 380, damping: 30 }}
                    />
                  )}
                  <item.icon className="relative h-4 w-4" />
                  <span className="relative">{item.label}</span>
                </Link>
              </motion.div>
            );
          })}
        </nav>

        <div className="flex items-center gap-3">
          {/* Desktop user menu */}
          <div className="hidden items-center gap-3 md:flex">
            {user && (
              <span className="text-body-sm text-[var(--ink-muted)]">{user.name}</span>
            )}
            <motion.button
              onClick={logout}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="flex h-8 w-8 items-center justify-center rounded-[var(--radius-full)] bg-white/80 text-[var(--ink-muted)] shadow-sm backdrop-blur-sm transition-colors hover:text-[var(--error)]"
            >
              <LogOut className="h-4 w-4" />
            </motion.button>
          </div>

          {/* Mobile profile link */}
          <Link href="/profile" className="md:hidden">
            <div className="flex h-8 w-8 items-center justify-center rounded-[var(--radius-full)] bg-white/80 shadow-sm backdrop-blur-sm">
              <User className="h-4 w-4 text-[var(--ink-muted)]" />
            </div>
          </Link>
        </div>
      </div>
    </header>
  );
}
