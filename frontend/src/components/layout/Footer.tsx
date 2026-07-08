export function Footer() {
  return (
    <footer className="relative border-t border-[var(--border)]/50 bg-white/40 py-12 backdrop-blur-sm">
      <div className="mx-auto max-w-[1120px] px-4 text-center">
        <p className="font-display text-display-md text-[var(--primary)]">Lipstick AI</p>
        <p className="mt-2 text-body-sm text-[var(--ink-muted)]">
          Discover your perfect shade — powered by AI
        </p>
        <p className="mt-6 text-body-sm text-[var(--ink-muted)]">
          &copy; {new Date().getFullYear()} Lipstick AI. All rights reserved.
        </p>
      </div>
    </footer>
  );
}
