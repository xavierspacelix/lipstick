"use client";

import { motion } from "motion/react";
import { ScanLine, Sparkles, History, Shield } from "lucide-react";

const features = [
  {
    icon: ScanLine,
    title: "AI-Powered Analysis",
    description:
      "Computer vision detects your face, segments your lips, and extracts precise RGB color values — all in under five seconds.",
  },
  {
    icon: Sparkles,
    title: "Smart Recommendations",
    description:
      "A hybrid recommendation engine combines deep learning classification with color-matching algorithms for your three best shades.",
  },
  {
    icon: History,
    title: "Personal History",
    description:
      "Every analysis is saved. Revisit past recommendations anytime without uploading another photo.",
  },
  {
    icon: Shield,
    title: "Private by Design",
    description:
      "Your images are stored securely in your own private bucket. Only you can see your analysis history.",
  },
];

function FeatureCard({
  icon: Icon,
  title,
  description,
  index,
}: {
  icon: React.ComponentType<{ className?: string }>;
  title: string;
  description: string;
  index: number;
}) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 40 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "-80px" }}
      transition={{
        delay: index * 0.1,
        duration: 0.5,
        ease: [0.16, 1, 0.3, 1],
      }}
      className="group rounded-[var(--radius-md)] border border-[var(--border-glass)] bg-white/60 p-6 shadow-[var(--shadow-glass)] backdrop-blur-sm transition-all duration-base hover:bg-white/80 hover:shadow-[var(--shadow-glass-lg)]"
    >
      <div className="flex h-12 w-12 items-center justify-center rounded-[var(--radius-sm)] bg-white/80 shadow-sm backdrop-blur-sm">
        <Icon className="h-6 w-6 text-[var(--primary)]" />
      </div>
      <h3 className="mt-5 font-display text-display-md text-[var(--ink)]">
        {title}
      </h3>
      <p className="mt-2 text-body-sm leading-relaxed text-[var(--ink-muted)]">
        {description}
      </p>
    </motion.div>
  );
}

export function Features() {
  return (
    <section className="relative py-24">
      <div className="mx-auto max-w-[1120px] px-4">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
          className="mx-auto max-w-xl text-center"
        >
          <h2 className="font-display text-display-lg text-[var(--ink)]">
            How It Works
          </h2>
          <p className="mt-4 text-body-lg text-[var(--ink-muted)]">
            From selfie to shade match in seconds
          </p>
        </motion.div>

        <div className="mt-16 grid gap-6 md:grid-cols-2 lg:grid-cols-4">
          {features.map((feature, i) => (
            <FeatureCard key={feature.title} {...feature} index={i} />
          ))}
        </div>
      </div>
    </section>
  );
}
