"use client";

import {
  createContext,
  useContext,
  useState,
  useEffect,
  useCallback,
  type ReactNode,
} from "react";
import { useRouter } from "next/navigation";
import { apiClient } from "@/lib/api-client";

interface User {
  id: string;
  name: string;
  email: string;
  total_analyses: number;
}

interface AuthContextType {
  user: User | null;
  loading: boolean;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (name: string, email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  refresh: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  const fetchUser = useCallback(async () => {
    try {
      const data = await apiClient<User>("/api/v1/profile");
      setUser(data);
    } catch {
      setUser(null);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchUser();
  }, [fetchUser]);

  const login = useCallback(
    async (email: string, password: string) => {
      const result = await apiClient<{ user_id: string; name: string; email: string }>(
        "/api/v1/login",
        { method: "POST", body: JSON.stringify({ email, password }) },
      );
      setUser({ id: result.user_id, name: result.name, email: result.email, total_analyses: 0 });
      await fetchUser();
    },
    [fetchUser],
  );

  const register = useCallback(
    async (name: string, email: string, password: string) => {
      await apiClient("/api/v1/register", {
        method: "POST",
        body: JSON.stringify({ name, email, password }),
      });
    },
    [],
  );

  const logout = useCallback(async () => {
    try {
      await apiClient("/api/v1/logout", { method: "POST" });
    } catch {
      // even if the server call fails, clear local state
    }
    setUser(null);
    router.push("/");
  }, [router]);

  const refresh = useCallback(async () => {
    await fetchUser();
  }, [fetchUser]);

  return (
    <AuthContext.Provider
      value={{ user, loading, isAuthenticated: !!user, login, register, logout, refresh }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}
