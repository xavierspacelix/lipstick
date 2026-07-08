"use client";

import { useRef } from "react";
import { motion, useScroll, useTransform } from "motion/react";

const categories = [
  {
    id: "pinkish",
    label: "Pinkish",
    description: "Soft rose, coral, and blush tones for fair to light skin",
    gradient: "from-[var(--lip-type-pinkish)] via-[#E1849C] to-[#F0A5B8]",
    swatches: ["#E1849C", "#D4708E", "#F0A5B8", "#C95A78", "#E899A8"],
  },
  {
    id: "brownish",
    label: "Brownish",
    description: "Warm nude, terra cotta, and mocha for medium to tan skin",
    gradient: "from-[var(--lip-type-brownish)] via-[#9C6B4F] to-[#B8856A]",
    swatches: ["#9C6B4F", "#B8856A", "#7D5538", "#C99B82", "#8B6045"],
  },
  {
    id: "dark",
    label: "Dark",
    description: "Deep berry, wine, and plum for deeper skin tones",
    gradient: "from-[var(--lip-type-dark)] via-[#4A1F2B] to-[#6B2D40]",
    swatches: ["#4A1F2B", "#6B2D40", "#8B3A54", "#3D1722", "#5C2536"],
  },
];

function ShadeCard({
  category,
  index,
}: {
  category: (typeof categories)[number];
  index: number;
}) {
  const ref = useRef<HTMLDivElement>(null);

  const { scrollYProgress } = useScroll({
    target: ref,
    offset: ["start end", "end start"],
  });

  const y = useTransform(scrollYProgress, [0, 0.5, 1], [60, 0, -40]);
  const scale = useTransform(scrollYProgress, [0, 0.3, 0.7, 1], [0.92, 1, 1, 0.96]);

  return (
    <motion.div
      ref={ref}
      className="group"
      style={{ y, scale }}
    >
      <motion.div
        className="overflow-hidden rounded-[var(--radius-lg)]"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: index * 0.15 + 0.2 }}
      >
        {/* Gradient backdrop */}
        <div
          className={`bg-gradient-to-br ${category.gradient} flex aspect-[3/4] flex-col items-center justify-end p-8`}
        >
          {/* Swatch ring */}
          <motion.div
            className="mb-8 flex -space-x-2"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: index * 0.15 + 0.4 }}
          >
            {category.swatches.map((swatch, i) => (
              <motion.div
                key={swatch}
                className="h-10 w-10 rounded-full border-2 border-white/40 shadow-lg"
                style={{ backgroundColor: swatch }}
                initial={{ opacity: 0, scale: 0, y: 20 }}
                animate={{ opacity: 1, scale: 1, y: 0 }}
                transition={{
                  delay: index * 0.15 + 0.4 + i * 0.08,
                  type: "spring",
                  stiffness: 200,
                  damping: 15,
                }}
                whileHover={{ scale: 1.3, zIndex: 10 }}
              />
            ))}
          </motion.div>

          {/* Label */}
          <motion.div
            className="w-full text-center"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.15 + 0.7 }}
          >
            <h3 className="font-display text-display-md text-white/90 drop-shadow-sm">
              {category.label}
            </h3>
            <p className="mt-2 text-body-sm text-white/70 drop-shadow-sm">
              {category.description}
            </p>

            <motion.button
              className="mt-6 inline-flex h-10 items-center gap-2 rounded-[var(--radius-full)] bg-white/20 px-5 text-body-sm font-medium text-white backdrop-blur-sm transition-colors hover:bg-white/30"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              Explore Shades
              <svg
                className="h-3.5 w-3.5"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                strokeWidth={2}
              >
                <path d="M5 12h14M13 5l7 7-7 7" />
              </svg>
            </motion.button>
          </motion.div>
        </div>
      </motion.div>
    </motion.div>
  );
}

export function ShadeShowcase() {
  return (
    <section className="relative overflow-hidden py-32">
      {/* Section heading */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        transition={{ duration: 0.5 }}
        className="mx-auto mb-20 max-w-xl px-4 text-center"
      >
        <span className="inline-block rounded-full border border-[var(--border-glass)] bg-white/60 px-4 py-1.5 text-body-sm text-[var(--ink-muted)] backdrop-blur-sm">
          Three Lip Categories
        </span>
        <h2 className="mt-6 font-display text-display-lg text-[var(--ink)]">
          Shades Curated for You
        </h2>
        <p className="mt-4 text-body-lg text-[var(--ink-muted)]">
          Our AI classifies your lip color into one of three categories, then
          recommends the perfect shades within that family.
        </p>
      </motion.div>

      {/* Cards grid */}
      <div className="mx-auto grid max-w-5xl gap-8 px-4 md:grid-cols-3">
        {categories.map((cat, i) => (
          <ShadeCard key={cat.id} category={cat} index={i} />
        ))}
      </div>
    </section>
  );
}
