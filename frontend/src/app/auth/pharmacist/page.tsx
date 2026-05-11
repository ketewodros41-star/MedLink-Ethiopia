"use client";

import { useState } from "react";
import { ArrowRight, ShieldCheck, Store } from "lucide-react";
import Link from "next/link";
import { useRouter } from "next/navigation";

import { useAuth } from "@/lib/auth";

export default function PharmacistLogin() {
  const router = useRouter();
  const { login } = useAuth();
  const [license, setLicense] = useState("pharmacist-demo");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setLoading(true);
    setError(null);
    try {
      await login("pharmacist", license);
      router.push("/pharmacy");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to authenticate");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen grid bg-background lg:grid-cols-2">
      <div className="relative hidden flex-col justify-between overflow-hidden bg-primary p-12 text-primary-foreground lg:flex">
        <div className="absolute -bottom-[20%] -left-[10%] h-[60%] w-[80%] rounded-full bg-emerald-400 opacity-20 blur-3xl" />
        <div className="relative z-10">
          <div className="mb-16 flex items-center gap-2">
            <ShieldCheck className="h-8 w-8" />
            <span className="text-2xl font-semibold tracking-tight">MedLink Ethiopia</span>
          </div>
          <div className="max-w-md space-y-6">
            <h1 className="text-4xl font-bold leading-tight">Operations access for pharmacists.</h1>
            <p className="text-lg leading-relaxed text-primary-foreground/80">
              Authenticate into a live demo session to verify stock, review reservations, and keep medicine discovery reliable.
            </p>
          </div>
        </div>
        <div className="relative z-10 pt-12 text-sm font-medium opacity-70">
          © 2026 MedLink Infrastructure. Authorized access only.
        </div>
      </div>

      <div className="flex flex-col justify-center p-8 md:p-16">
        <div className="mx-auto w-full max-w-sm space-y-8">
          <div className="text-center lg:text-left">
            <div className="mx-auto mb-6 flex h-12 w-12 items-center justify-center rounded-2xl bg-primary/10 text-primary lg:mx-0">
              <Store className="h-6 w-6" />
            </div>
            <h2 className="mb-2 text-3xl font-bold tracking-tight">Pharmacist Login</h2>
            <p className="text-sm text-muted-foreground">Create a pharmacist demo session against the backend auth endpoint.</p>
          </div>

          <form className="space-y-4" onSubmit={handleSubmit}>
            <div className="space-y-2">
              <label className="text-sm font-semibold">License Number or Account ID</label>
              <input
                value={license}
                onChange={(e) => setLicense(e.target.value)}
                required
                placeholder="e.g. PH-29834-A"
                className="w-full rounded-xl border border-border bg-muted/50 px-4 py-3 font-medium transition-all focus:border-primary focus:outline-none focus:ring-1 focus:ring-primary/50"
              />
            </div>

            <div className="space-y-2">
              <label className="text-sm font-semibold">Demo PIN</label>
              <input
                type="password"
                required
                defaultValue="demo"
                className="w-full rounded-xl border border-border bg-muted/50 px-4 py-3 font-medium transition-all focus:border-primary focus:outline-none focus:ring-1 focus:ring-primary/50"
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="mt-6 flex w-full items-center justify-center gap-2 rounded-xl bg-primary py-3.5 font-bold text-primary-foreground transition-all hover:bg-primary-800 disabled:cursor-not-allowed disabled:opacity-70"
            >
              {loading ? "Authenticating..." : (
                <>
                  Access Dashboard
                  <ArrowRight className="ml-1 h-4 w-4" />
                </>
              )}
            </button>
            {error ? <p className="text-sm text-rose-700">{error}</p> : null}
          </form>

          <div className="border-t border-border/50 pt-4 text-center text-sm text-muted-foreground">
            Are you a patient looking for medicine?{" "}
            <Link href="/auth" className="font-semibold text-primary hover:underline">
              Go to patient access
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
