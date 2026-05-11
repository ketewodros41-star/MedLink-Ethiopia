"use client";

import { useState } from "react";
import { ArrowRight, ShieldCheck, User } from "lucide-react";
import { useRouter } from "next/navigation";

import { Navbar } from "@/components/navbar";
import { useAuth } from "@/lib/auth";

export default function AuthPage() {
  const router = useRouter();
  const { login } = useAuth();
  const [username, setUsername] = useState("patient-demo");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handlePatientLogin = async () => {
    setLoading(true);
    setError(null);
    try {
      await login("patient", username);
      router.push("/search?q=amoxicillin");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to log in");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      <main className="mx-auto flex min-h-[calc(100vh-4rem)] max-w-5xl items-center px-4 py-12">
        <div className="grid w-full gap-8 lg:grid-cols-2">
          <section className="rounded-3xl border border-border bg-card p-8 shadow-sm">
            <p className="mb-2 text-sm font-semibold uppercase tracking-[0.2em] text-primary">Patient Access</p>
            <h1 className="mb-4 text-4xl font-bold tracking-tight">Try the patient journey.</h1>
            <p className="mb-8 max-w-md text-muted-foreground">
              Sign into a demo patient session to search medicines, upload prescriptions, and manage reservations against the live backend.
            </p>
            <label className="mb-2 block text-sm font-semibold">Display Name</label>
            <input
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="mb-4 w-full rounded-xl border border-border bg-muted/40 px-4 py-3 outline-none focus:border-primary"
              placeholder="patient-demo"
            />
            <button
              onClick={handlePatientLogin}
              disabled={loading}
              className="flex w-full items-center justify-center gap-2 rounded-xl bg-primary px-5 py-3.5 font-semibold text-primary-foreground transition-colors hover:bg-primary-800 disabled:opacity-60"
            >
              <User className="h-4 w-4" />
              {loading ? "Signing in..." : "Continue as Patient"}
            </button>
            {error ? <p className="mt-3 text-sm text-rose-700">{error}</p> : null}
          </section>

          <section className="rounded-3xl bg-primary p-8 text-primary-foreground shadow-sm">
            <p className="mb-2 text-sm font-semibold uppercase tracking-[0.2em] text-primary-foreground/70">Operations Access</p>
            <h2 className="mb-4 text-4xl font-bold tracking-tight">Pharmacy operations portal.</h2>
            <p className="mb-8 max-w-md text-primary-foreground/80">
              Pharmacists can verify inventory, review incoming reservations, and keep medicine availability current for nearby patients.
            </p>
            <a
              href="/auth/pharmacist"
              className="inline-flex items-center gap-2 rounded-xl bg-white px-5 py-3.5 font-semibold text-primary transition-transform hover:translate-x-0.5"
            >
              <ShieldCheck className="h-4 w-4" />
              Open Pharmacist Login
              <ArrowRight className="h-4 w-4" />
            </a>
          </section>
        </div>
      </main>
    </div>
  );
}
