"use client";

import { useEffect, useState } from "react";
import { Calendar, Clock, Loader2 } from "lucide-react";
import Link from "next/link";

import { Navbar } from "@/components/navbar";
import { useAuth } from "@/lib/auth";
import { apiRequest } from "@/lib/api";

type ReservationItem = {
  reservation_id: string;
  status: string;
  quantity: number;
  expires_at: string;
  medicine: { canonical_name: string; strength?: string | null; form?: string | null };
  pharmacy: { name: string; city: string };
};

export default function ReservationsPage() {
  const { hydrated, token, user, login } = useAuth();
  const [reservations, setReservations] = useState<ReservationItem[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!hydrated || !token || !user?.roles.includes("patient")) {
      return;
    }
    const run = async () => {
      setLoading(true);
      try {
        const payload = await apiRequest<{ results: ReservationItem[] }>("/api/v1/reservations/mine", { token });
        setReservations(payload.results);
      } catch (err: unknown) {
        setError(err instanceof Error ? err.message : "Unable to load reservations");
      } finally {
        setLoading(false);
      }
    };
    void run();
  }, [hydrated, token, user]);

  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      <main className="mx-auto max-w-4xl px-4 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold tracking-tight">Your reservations</h1>
          <p className="mt-2 text-sm text-muted-foreground">
            Live reservation state comes from the backend, including expiry and pharmacy context.
          </p>
        </div>

        {!hydrated ? (
          <div className="rounded-2xl border border-border bg-card p-8 text-center shadow-sm">
            <Loader2 className="mx-auto mb-3 h-6 w-6 animate-spin text-primary" />
            <p className="text-sm text-muted-foreground">Preparing session...</p>
          </div>
        ) : !user ? (
          <div className="rounded-2xl border border-border bg-card p-8 shadow-sm">
            <h2 className="text-xl font-semibold">Patient access required</h2>
            <p className="mt-2 text-sm text-muted-foreground">
              Sign into the patient demo session to view and create reservations.
            </p>
            <button
              onClick={() => void login("patient", "patient-demo")}
              className="mt-5 rounded-xl bg-primary px-5 py-3 text-sm font-semibold text-primary-foreground"
            >
              Continue as patient
            </button>
          </div>
        ) : loading ? (
          <div className="rounded-2xl border border-border bg-card p-8 text-center shadow-sm">
            <Loader2 className="mx-auto mb-3 h-6 w-6 animate-spin text-primary" />
            <p className="text-sm text-muted-foreground">Loading your reservation history...</p>
          </div>
        ) : error ? (
          <div className="rounded-2xl border border-rose-200 bg-rose-50 p-6 text-sm text-rose-800 shadow-sm">{error}</div>
        ) : reservations.length === 0 ? (
          <div className="rounded-2xl border border-border bg-card p-8 shadow-sm">
            <div className="mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-primary/10 text-primary">
              <Calendar className="h-8 w-8" />
            </div>
            <h2 className="text-2xl font-bold">No reservations yet</h2>
            <p className="mt-2 text-sm text-muted-foreground">
              Search a medicine and reserve it before traveling to the pharmacy.
            </p>
            <Link href="/search?q=amoxicillin" className="mt-5 inline-block rounded-xl bg-primary px-5 py-3 text-sm font-semibold text-primary-foreground">
              Start searching
            </Link>
          </div>
        ) : (
          <div className="space-y-4">
            {reservations.map((reservation) => (
              <div key={reservation.reservation_id} className="rounded-2xl border border-border bg-card p-5 shadow-sm">
                <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
                  <div>
                    <h3 className="text-xl font-semibold">
                      {reservation.medicine.canonical_name}
                      {reservation.medicine.strength ? ` ${reservation.medicine.strength}` : ""}
                    </h3>
                    <p className="text-sm text-muted-foreground">
                      {reservation.pharmacy.name} • {reservation.pharmacy.city}
                    </p>
                  </div>
                  <div className="flex flex-wrap items-center gap-2">
                    <span className="rounded-full bg-primary/10 px-3 py-1 text-xs font-semibold uppercase tracking-wide text-primary">
                      {reservation.status}
                    </span>
                    <span className="flex items-center gap-1 text-xs font-medium text-muted-foreground">
                      <Clock className="h-3.5 w-3.5" />
                      Expires {new Date(reservation.expires_at).toLocaleString()}
                    </span>
                  </div>
                </div>
                <p className="mt-3 text-sm text-foreground">Quantity reserved: {reservation.quantity}</p>
              </div>
            ))}
          </div>
        )}
      </main>
    </div>
  );
}
