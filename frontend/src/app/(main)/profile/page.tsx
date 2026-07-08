"use client";

import { useState } from "react";
import { motion } from "motion/react";
import { User, Mail, BarChart3, LogOut } from "lucide-react";
import { useAuth } from "@/context/auth";
import { apiClient } from "@/lib/api-client";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

export default function ProfilePage() {
  const { user, logout } = useAuth();
  const [saving, setSaving] = useState(false);
  const [name, setName] = useState(user?.name ?? "");
  const [saveMsg, setSaveMsg] = useState<string | null>(null);

  const [currentPw, setCurrentPw] = useState("");
  const [newPw, setNewPw] = useState("");
  const [pwMsg, setPwMsg] = useState<string | null>(null);
  const [pwError, setPwError] = useState<string | null>(null);

  async function handleUpdateName(e: React.FormEvent) {
    e.preventDefault();
    setSaving(true);
    setSaveMsg(null);
    try {
      await apiClient("/api/v1/profile", {
        method: "PATCH",
        body: JSON.stringify({ name }),
      });
      setSaveMsg("Name updated");
    } catch (err) {
      setSaveMsg(err instanceof Error ? err.message : "Failed to update");
    } finally {
      setSaving(false);
    }
  }

  async function handleChangePassword(e: React.FormEvent) {
    e.preventDefault();
    if (newPw.length < 8) {
      setPwError("Password must be at least 8 characters");
      return;
    }
    setPwError(null);
    setPwMsg(null);
    try {
      await apiClient("/api/v1/profile/password", {
        method: "PATCH",
        body: JSON.stringify({ current_password: currentPw, new_password: newPw }),
      });
      setPwMsg("Password updated");
      setCurrentPw("");
      setNewPw("");
    } catch (err) {
      setPwError(err instanceof Error ? err.message : "Failed to update password");
    }
  }

  return (
    <div className="mx-auto max-w-[640px] px-4 py-8">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <span className="inline-block rounded-full border border-[var(--border-glass)] bg-white/60 px-3 py-1 text-[11px] font-medium uppercase tracking-wider text-[var(--ink-muted)] backdrop-blur-sm">
          Profile
        </span>
        <h1 className="mt-4 font-display text-display-xl text-[var(--ink)]">
          {user?.name ?? "Your Profile"}
        </h1>
      </motion.div>

      <div className="mt-10 space-y-6">
        {/* User info card */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="rounded-[var(--radius-md)] border border-[var(--border-glass)] bg-white/60 p-6 shadow-[var(--shadow-glass)] backdrop-blur-sm"
        >
          <h3 className="font-display text-display-md text-[var(--ink)]">Account Info</h3>
          <div className="mt-4 space-y-3">
            <div className="flex items-center gap-3 text-body-sm text-[var(--ink-muted)]">
              <User className="h-4 w-4 shrink-0" />
              <span>{user?.name ?? "—"}</span>
            </div>
            <div className="flex items-center gap-3 text-body-sm text-[var(--ink-muted)]">
              <Mail className="h-4 w-4 shrink-0" />
              <span>{user?.email ?? "—"}</span>
            </div>
            <div className="flex items-center gap-3 text-body-sm text-[var(--ink-muted)]">
              <BarChart3 className="h-4 w-4 shrink-0" />
              <span>{user?.total_analyses ?? 0} analyses</span>
            </div>
          </div>
        </motion.div>

        {/* Edit name */}
        <motion.form
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.15 }}
          onSubmit={handleUpdateName}
          className="rounded-[var(--radius-md)] border border-[var(--border-glass)] bg-white/60 p-6 shadow-[var(--shadow-glass)] backdrop-blur-sm"
        >
          <h3 className="font-display text-display-md text-[var(--ink)]">Edit Name</h3>
          <div className="mt-4 space-y-2">
            <Label htmlFor="name" className="text-body-sm font-medium text-[var(--ink)]">Name</Label>
            <Input
              id="name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="border-[var(--border)] bg-white/70 backdrop-blur-sm"
            />
          </div>
          {saveMsg && (
            <p className={`mt-2 text-body-sm ${saveMsg === "Name updated" ? "text-[var(--success)]" : "text-[var(--error)]"}`}>
              {saveMsg}
            </p>
          )}
          <Button type="submit" className="mt-4" disabled={saving}>
            {saving ? "Saving..." : "Save"}
          </Button>
        </motion.form>

        {/* Change password */}
        <motion.form
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          onSubmit={handleChangePassword}
          className="rounded-[var(--radius-md)] border border-[var(--border-glass)] bg-white/60 p-6 shadow-[var(--shadow-glass)] backdrop-blur-sm"
        >
          <h3 className="font-display text-display-md text-[var(--ink)]">Change Password</h3>
          <div className="mt-4 space-y-3">
            <div className="space-y-2">
              <Label htmlFor="currentPw" className="text-body-sm font-medium text-[var(--ink)]">Current Password</Label>
              <Input
                id="currentPw"
                type="password"
                value={currentPw}
                onChange={(e) => setCurrentPw(e.target.value)}
                className="border-[var(--border)] bg-white/70 backdrop-blur-sm"
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="newPw" className="text-body-sm font-medium text-[var(--ink)]">New Password</Label>
              <Input
                id="newPw"
                type="password"
                value={newPw}
                onChange={(e) => setNewPw(e.target.value)}
                placeholder="At least 8 characters"
                className="border-[var(--border)] bg-white/70 backdrop-blur-sm"
              />
            </div>
          </div>
          {pwMsg && <p className="mt-2 text-body-sm text-[var(--success)]">{pwMsg}</p>}
          {pwError && <p className="mt-2 text-body-sm text-[var(--error)]">{pwError}</p>}
          <Button type="submit" className="mt-4">Update Password</Button>
        </motion.form>

        {/* Logout */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.25 }}
        >
          <button
            onClick={logout}
            className="flex w-full items-center justify-center gap-2 rounded-[var(--radius-md)] border border-[var(--error)]/20 bg-[var(--error)]/5 py-3 text-body-sm font-medium text-[var(--error)] transition-all duration-base hover:bg-[var(--error)]/10"
          >
            <LogOut className="h-4 w-4" />
            Sign Out
          </button>
        </motion.div>
      </div>
    </div>
  );
}
