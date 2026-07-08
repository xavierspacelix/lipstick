"use client";

import { usePathname } from "next/navigation";
import { useEffect } from "react";
import { motion } from "motion/react";
import { SmoothScroll } from "@/components/providers/SmoothScroll";
import { AuthProvider } from "@/context/auth";

function PageTransition({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();

  useEffect(() => {
    window.scrollTo(0, 0);
  }, [pathname]);

  return (
    <motion.div
      key={pathname}
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.15 }}
    >
      {children}
    </motion.div>
  );
}

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <AuthProvider>
      <SmoothScroll>
        <PageTransition>{children}</PageTransition>
      </SmoothScroll>
    </AuthProvider>
  );
}
