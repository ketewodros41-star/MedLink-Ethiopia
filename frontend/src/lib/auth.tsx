"use client";

import { createContext, useContext, useEffect, useMemo, useState } from "react";

import { apiRequest } from "@/lib/api";

type AuthUser = {
  sub: string;
  roles: string[];
  profile?: string;
  pharmacy_id?: string;
  pharmacy_name?: string;
  exp?: string;
};

type AuthContextValue = {
  token: string | null;
  user: AuthUser | null;
  hydrated: boolean;
  login: (role: "patient" | "pharmacist" | "admin", username: string) => Promise<void>;
  logout: () => void;
};

const TOKEN_KEY = "medlink.demo.token";
const USER_KEY = "medlink.demo.user";

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [token, setToken] = useState<string | null>(null);
  const [user, setUser] = useState<AuthUser | null>(null);
  const [hydrated, setHydrated] = useState(false);

  useEffect(() => {
    queueMicrotask(() => {
      const storedToken = window.localStorage.getItem(TOKEN_KEY);
      const storedUser = window.localStorage.getItem(USER_KEY);
      if (storedToken) {
        setToken(storedToken);
      }
      if (storedUser) {
        setUser(JSON.parse(storedUser) as AuthUser);
      }
      setHydrated(true);
    });
  }, []);

  const login = async (role: "patient" | "pharmacist" | "admin", username: string) => {
    const response = await apiRequest<{ access_token: string; user: AuthUser }>("/api/v1/auth/demo-login", {
      method: "POST",
      body: { role, username },
    });
    setToken(response.access_token);
    setUser(response.user);
    window.localStorage.setItem(TOKEN_KEY, response.access_token);
    window.localStorage.setItem(USER_KEY, JSON.stringify(response.user));
  };

  const logout = () => {
    setToken(null);
    setUser(null);
    window.localStorage.removeItem(TOKEN_KEY);
    window.localStorage.removeItem(USER_KEY);
  };

  const value = useMemo(
    () => ({ token, user, hydrated, login, logout }),
    [token, user, hydrated],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within AuthProvider");
  }
  return context;
}
