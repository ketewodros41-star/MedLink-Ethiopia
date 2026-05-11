"use client";

import { useEffect, useState } from "react";
import { Loader2, Phone, ShieldCheck } from "lucide-react";

import { Navbar } from "@/components/navbar";
import { useAuth } from "@/lib/auth";
import { apiRequest } from "@/lib/api";

type PharmacyDirectoryItem = {
  id: string;
  name: string;
  city: string;
  region: string;
  contact_phone?: string | null;
  trust_score: number;
  verified_pharmacist: boolean;
  flags: string[];
};

export default function PharmaciesDirectory() {
  const { hydrated, token } = useAuth();
  const [pharmacies, setPharmacies] = useState<PharmacyDirectoryItem[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!hydrated) {
      return;
    }
    const run = async () => {
      setLoading(true);
      try {
        const payload = await apiRequest<{ results: PharmacyDirectoryItem[] }>("/api/v1/pharmacy/directory", { token });
        setPharmacies(payload.results);
      } finally {
        setLoading(false);
      }
    };
    void run();
  }, [hydrated, token]);

  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      <main className="mx-auto max-w-5xl px-4 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold tracking-tight">Verified pharmacy directory</h1>
          <p className="mt-2 text-sm text-muted-foreground">
            This page is connected to the backend trust engine and pharmacy registry.
          </p>
        </div>

        {!hydrated ? (
          <div className="rounded-2xl border border-border bg-card p-8 text-center shadow-sm">
            <Loader2 className="mx-auto h-6 w-6 animate-spin text-primary" />
          </div>
        ) : loading ? (
          <div className="rounded-2xl border border-border bg-card p-8 text-center shadow-sm">
            <Loader2 className="mx-auto h-6 w-6 animate-spin text-primary" />
          </div>
        ) : (
          <div className="grid gap-4 md:grid-cols-2">
            {pharmacies.map((pharmacy) => (
              <div key={pharmacy.id} className="rounded-2xl border border-border bg-card p-5 shadow-sm">
                <div className="mb-3 flex items-start justify-between gap-4">
                  <div>
                    <h2 className="text-xl font-semibold">{pharmacy.name}</h2>
                    <p className="text-sm text-muted-foreground">
                      {pharmacy.city}, {pharmacy.region}
                    </p>
                  </div>
                  <div className="rounded-full bg-primary/10 px-3 py-1 text-xs font-semibold text-primary">
                    Trust {Math.round(pharmacy.trust_score)}
                  </div>
                </div>
                <div className="space-y-2 text-sm">
                  <div className="flex items-center gap-2 text-emerald-700">
                    <ShieldCheck className="h-4 w-4" />
                    {pharmacy.verified_pharmacist ? "Verified pharmacist profile" : "Verification pending"}
                  </div>
                  {pharmacy.contact_phone ? (
                    <div className="flex items-center gap-2 text-muted-foreground">
                      <Phone className="h-4 w-4" />
                      {pharmacy.contact_phone}
                    </div>
                  ) : null}
                  {pharmacy.flags.length > 0 ? (
                    <p className="text-xs text-amber-700">Flags: {pharmacy.flags.join(", ")}</p>
                  ) : (
                    <p className="text-xs text-muted-foreground">No active trust flags.</p>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </main>
    </div>
  );
}
