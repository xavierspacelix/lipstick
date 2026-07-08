import type { Metadata } from "next";
import { Fraunces, IBM_Plex_Mono, Geist } from "next/font/google";
import "./globals.css";
import { cn } from "@/lib/utils";
import { Providers } from "./providers";

const fraunces = Fraunces({
  subsets: ["latin"],
  variable: "--font-display",
  axes: ["opsz"],
});

const plexMono = IBM_Plex_Mono({
  subsets: ["latin"],
  weight: ["500"],
  variable: "--font-mono",
});

const geist = Geist({ subsets: ["latin"], variable: "--font-sans" });

export const metadata: Metadata = {
  title: "Lipstick AI",
  description: "Discover your perfect lipstick shade with AI",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="en"
      className={cn(fraunces.variable, plexMono.variable, "font-sans", geist.variable)}
    >
      <body className="min-h-screen bg-background font-sans text-ink antialiased">
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
