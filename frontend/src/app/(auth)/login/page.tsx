"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useAuth } from "@/context/auth";

const loginSchema = z.object({
  email: z.string().email("Enter a valid email"),
  password: z.string().min(1, "Password is required"),
});

type LoginForm = z.infer<typeof loginSchema>;

export default function LoginPage() {
  const router = useRouter();
  const { login } = useAuth();
  const [error, setError] = useState<string | null>(null);

  const form = useForm<LoginForm>({
    resolver: zodResolver(loginSchema),
    defaultValues: { email: "", password: "" },
  });

  async function onSubmit(data: LoginForm) {
    setError(null);
    try {
      await login(data.email, data.password);
      router.push("/dashboard");
    } catch (e) {
      setError(e instanceof Error ? e.message : "Login failed");
    }
  }

  return (
    <main className="relative flex min-h-screen items-center justify-center p-4">
      <div
        className="absolute top-1/2 left-1/2 h-[500px] w-[500px] -translate-x-1/2 -translate-y-1/2 rounded-[var(--radius-full)] opacity-[0.03]"
        style={{ background: "radial-gradient(circle, var(--primary) 0%, transparent 70%)" }}
      />
      <div className="relative w-full max-w-sm rounded-[var(--radius-lg)] border border-[var(--border-glass)] bg-white/60 p-8 shadow-[var(--shadow-glass-lg)] backdrop-blur-xl">
        <div className="text-center">
          <Link href="/" className="font-display text-display-md text-[var(--primary)] no-underline">
            Lipstick AI
          </Link>
          <h1 className="mt-6 font-display text-display-md text-[var(--ink)]">Welcome back</h1>
          <p className="mt-1 text-body-sm text-[var(--ink-muted)]">Sign in to your account</p>
        </div>

        <form onSubmit={form.handleSubmit(onSubmit)} className="mt-8 space-y-5">
          {error && (
            <p className="rounded-[var(--radius-sm)] border border-[var(--error)]/20 bg-[var(--error)]/5 px-3 py-2 text-body-sm text-[var(--error)]">
              {error}
            </p>
          )}
          <div className="space-y-2">
            <Label htmlFor="email" className="text-body-sm font-medium text-[var(--ink)]">
              Email
            </Label>
            <Input
              id="email"
              type="email"
              placeholder="you@example.com"
              className="border-[var(--border)] bg-white/70 backdrop-blur-sm"
              {...form.register("email")}
            />
            {form.formState.errors.email && (
              <p className="text-body-sm text-[var(--error)]">{form.formState.errors.email.message}</p>
            )}
          </div>
          <div className="space-y-2">
            <Label htmlFor="password" className="text-body-sm font-medium text-[var(--ink)]">
              Password
            </Label>
            <Input
              id="password"
              type="password"
              placeholder="Your password"
              className="border-[var(--border)] bg-white/70 backdrop-blur-sm"
              {...form.register("password")}
            />
            {form.formState.errors.password && (
              <p className="text-body-sm text-[var(--error)]">{form.formState.errors.password.message}</p>
            )}
          </div>
          <Button type="submit" className="w-full" disabled={form.formState.isSubmitting}>
            {form.formState.isSubmitting ? "Signing in..." : "Sign in"}
          </Button>
        </form>

        <p className="mt-8 text-center text-body-sm text-[var(--ink-muted)]">
          Don&apos;t have an account?{" "}
          <Link href="/register" className="font-medium text-[var(--primary)] hover:underline">
            Create one
          </Link>
        </p>
      </div>
    </main>
  );
}
