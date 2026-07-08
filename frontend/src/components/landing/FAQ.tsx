"use client";

import { motion } from "motion/react";

const faqs = [
  {
    q: "What kind of photo should I upload?",
    a: "A clear, front-facing selfie with good lighting. Make sure your lips are visible and not covered by anything. Avoid heavy lipstick — the analysis works best on bare lips.",
  },
  {
    q: "How long does the analysis take?",
    a: "The entire pipeline runs in under five seconds. Face detection, lip segmentation, color extraction, classification, and recommendation happen automatically.",
  },
  {
    q: "Is my photo stored securely?",
    a: "Yes. Images are stored in your private storage bucket and are only accessible to you. We never share or use your photos beyond generating your recommendation.",
  },
  {
    q: "Can I redo an analysis?",
    a: "Absolutely. You can upload a new photo at any time for a fresh analysis. All past results are saved in your history.",
  },
  {
    q: "What lip types does the AI recognize?",
    a: "The model currently classifies lips into three categories: Pinkish, Brownish, and Dark. Each category has a curated set of recommended shades.",
  },
];

function FAQItem({
  q,
  a,
  index,
}: {
  q: string;
  a: string;
  index: number;
}) {
  return (
    <motion.details
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "-40px" }}
      transition={{
        delay: index * 0.08,
        duration: 0.4,
        ease: [0.16, 1, 0.3, 1],
      }}
      className="group rounded-[var(--radius-md)] border border-[var(--border-glass)] bg-white/60 shadow-[var(--shadow-glass)] backdrop-blur-sm transition-all duration-base hover:bg-white/80 hover:shadow-[var(--shadow-glass-lg)]"
    >
      <summary className="flex cursor-pointer items-center justify-between px-6 py-4 text-body-md font-medium text-[var(--ink)]">
        {q}
        <span className="ml-4 flex h-6 w-6 shrink-0 items-center justify-center rounded-full border border-[var(--border)] bg-white/60 text-sm text-[var(--primary)] transition-transform duration-base group-open:rotate-45">
          +
        </span>
      </summary>
      <div className="border-t border-[var(--border)]/50 px-6 py-4">
        <p className="text-body-sm leading-relaxed text-[var(--ink-muted)]">{a}</p>
      </div>
    </motion.details>
  );
}

export function FAQ() {
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
            Frequently Asked Questions
          </h2>
        </motion.div>

        <div className="mx-auto mt-12 max-w-2xl space-y-4">
          {faqs.map((faq, i) => (
            <FAQItem key={faq.q} {...faq} index={i} />
          ))}
        </div>
      </div>
    </section>
  );
}
