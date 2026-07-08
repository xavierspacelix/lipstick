import { Hero } from "@/components/landing/Hero";
import { Features } from "@/components/landing/Features";
import { ShadeShowcase } from "@/components/landing/ShadeShowcase";
import { FAQ } from "@/components/landing/FAQ";
import { AmbientBackground } from "@/components/ambient/AmbientBackground";
import { SwatchScatter } from "@/components/ambient/SwatchScatter";

export default function Home() {
  return (
    <>
      <AmbientBackground />
      <SwatchScatter />
      <Hero />
      <Features />
      <ShadeShowcase />
      <FAQ />
    </>
  );
}
