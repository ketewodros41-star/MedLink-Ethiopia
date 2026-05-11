"use client";

import { useEffect, useMemo, useState } from "react";
import {
  AlertCircle,
  ArrowLeft,
  CheckCircle2,
  Clock,
  Loader2,
  MapPin,
  ShieldCheck,
} from "lucide-react";
import Link from "next/link";
import { useParams, useRouter } from "next/navigation";

import { Navbar } from "@/components/navbar";
import { useAuth } from "@/lib/auth";
import { apiRequest } from "@/lib/api";

type MedicineDetail = {
  medicine: {
    id: string;
    canonical_name: string;
    generic_name: string;
    strength?: string | null;
    form?: string | null;
    therapeutic_class?: string | null;
  };
};

type Availability = {
  pharmacies: Array<{
    pharmacy_id: string;
    name: string;
    city: string;
    region: string;
    distance_km: number;
    quantity_available: number;
    state: string;
    confidence_score: number;
    trust_score: number;
    verified_pharmacist: boolean;
  }>;
};

export default function MedicineDetailPage() {
  const params = useParams<{ id: string }>();
  const router = useRouter();
  const { hydrated, user, token } = useAuth();
  const [detail, setDetail] = useState<MedicineDetail | null>(null);
  const [availability, setAvailability] = useState<Availability["pharmacies"]>([]);
  const [loading, setLoading] = useState(false);
  const [reserveLoading, setReserveLoading] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [message, setMessage] = useState<string | null>(null);

  const medicineId = useMemo(() => String(params.id ?? ""), [params.id]);

  useEffect(() => {
    if (!hydrated || !medicineId) {
      return;
    }
    const run = async () => {
      setLoading(true);
      setError(null);
      try {
        const [detailResponse, availabilityResponse] = await Promise.all([
          apiRequest<MedicineDetail>(`/api/v1/medicine/${medicineId}`, { token }),
          apiRequest<Availability>(`/api/v1/medicine/${medicineId}/availability`, { token }),
        ]);
        setDetail(detailResponse);
        setAvailability(availabilityResponse.pharmacies);
      } catch (err: unknown) {
        setError(err instanceof Error ? err.message : "Unable to load medicine details");
      } finally {
        setLoading(false);
      }
    };

    void run();
  }, [hydrated, token, medicineId]);

  const handleReserve = async (pharmacyId: string) => {
    if (!token || !detail) return;
    setReserveLoading(pharmacyId);
    setMessage(null);
    setError(null);
    try {
      await apiRequest("/api/v1/reservations/", {
        method: "POST",
        token,
        body: { pharmacy_id: pharmacyId, medicine_id: detail.medicine.id, quantity: 1 },
      });
      setMessage("Reservation created. Redirecting to your reservations.");
      setTimeout(() => router.push("/reservations"), 900);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Unable to reserve medicine");
    } finally {
      setReserveLoading(null);
    }
  };

  return (
    <div className="min-h-screen bg-muted/10 pb-20 md:pb-0">
      <Navbar />
      <main className="mx-auto w-full max-w-5xl px-4 py-8">
        <Link
          href="/search"
          className="mb-6 inline-flex items-center gap-2 text-sm font-medium text-muted-foreground transition-colors hover:text-foreground"
        >
          <ArrowLeft className="h-4 w-4" />
          Back to results
        </Link>

        {!hydrated ? (
          <div className="rounded-2xl border border-border bg-card p-8 text-center shadow-sm">
            <Loader2 className="mx-auto mb-3 h-6 w-6 animate-spin text-primary" />
            <p className="text-sm text-muted-foreground">Loading session...</p>
          </div>
        ) : loading ? (
          <div className="rounded-2xl border border-border bg-card p-8 text-center shadow-sm">
            <Loader2 className="mx-auto mb-3 h-6 w-6 animate-spin text-primary" />
            <p className="text-sm text-muted-foreground">Loading medicine availability...</p>
          </div>
        ) : error ? (
          <div className="rounded-2xl border border-rose-200 bg-rose-50 p-6 shadow-sm">
            <div className="flex items-start gap-3">
              <AlertCircle className="mt-0.5 h-5 w-5 text-rose-700" />
              <div>
                <h2 className="font-semibold text-rose-900">Unable to load medicine page</h2>
                <p className="mt-1 text-sm text-rose-700">{error}</p>
              </div>
            </div>
          </div>
        ) : detail ? (
          <div className="grid grid-cols-1 gap-8 lg:grid-cols-3">
            <div className="space-y-6 lg:col-span-1">
              <div className="rounded-3xl border border-border bg-card p-6 shadow-sm">
                <span className="mb-3 inline-block rounded-sm bg-primary/10 px-2 py-0.5 text-[10px] font-semibold uppercase tracking-widest text-primary">
                  Verified Registry
                </span>
                <h1 className="mb-2 text-3xl font-bold tracking-tight text-foreground">
                  {detail.medicine.canonical_name}
                  {detail.medicine.strength ? ` ${detail.medicine.strength}` : ""}
                </h1>
                <p className="mb-6 font-medium text-muted-foreground">
                  {detail.medicine.generic_name}
                  {detail.medicine.form ? ` • ${detail.medicine.form}` : ""}
                </p>

                <div className="space-y-4 border-t border-border/50 pt-4">
                  <div className="flex items-start gap-3">
                    <ShieldCheck className="mt-0.5 h-5 w-5 flex-shrink-0 text-emerald-600" />
                    <div>
                      <p className="text-sm font-semibold text-emerald-700">Backend trust and freshness scoring enabled</p>
                      <p className="mt-0.5 text-xs leading-relaxed text-muted-foreground">
                        Pharmacies are ranked by trust, inventory confidence, and distance rather than naive stock booleans.
                      </p>
                    </div>
                  </div>
                  <div className="flex items-start gap-3">
                    <Clock className="mt-0.5 h-5 w-5 flex-shrink-0 text-primary" />
                    <div>
                      <p className="text-sm font-semibold">Operational note</p>
                      <p className="mt-0.5 text-xs leading-relaxed text-muted-foreground">
                        Reservations are time-bound and inventory confidence changes with verification freshness.
                      </p>
                    </div>
                  </div>
                </div>
              </div>

              {message ? <div className="rounded-2xl border border-emerald-200 bg-emerald-50 p-4 text-sm text-emerald-800">{message}</div> : null}
            </div>

            <div className="space-y-4 lg:col-span-2">
              <div className="mb-2 flex items-center justify-between">
                <h2 className="text-xl font-semibold">Available near you</h2>
                <span className="rounded-md bg-muted px-2 py-1 text-xs font-medium text-muted-foreground">
                  Addis Ababa demo radius
                </span>
              </div>

              {availability.length === 0 ? (
                <div className="rounded-2xl border border-border bg-card p-6 shadow-sm">
                  <h3 className="font-semibold">No nearby verified availability</h3>
                  <p className="mt-2 text-sm text-muted-foreground">
                    Try a broader search or check the community page for recent sightings and shortage signals.
                  </p>
                </div>
              ) : (
                availability.map((pharmacy) => (
                  <div key={pharmacy.pharmacy_id} className="rounded-2xl border border-border bg-card p-5 shadow-sm">
                    <div className="flex flex-col gap-4 sm:flex-row sm:justify-between">
                      <div className="space-y-1">
                        <div className="flex flex-wrap items-center gap-2">
                          <h3 className="text-lg font-bold">{pharmacy.name}</h3>
                          <div className="flex items-center gap-1 rounded bg-primary/10 px-1.5 py-0.5 text-xs font-bold text-primary">
                            <ShieldCheck className="h-3 w-3" />
                            Trust {Math.round(pharmacy.trust_score)}
                          </div>
                        </div>
                        <p className="flex items-center gap-1 text-sm text-muted-foreground">
                          <MapPin className="h-3 w-3" />
                          {pharmacy.city}, {pharmacy.region} • {pharmacy.distance_km} km away
                        </p>
                        <p className="text-xs text-muted-foreground">
                          {pharmacy.quantity_available} in stock • state {pharmacy.state.replaceAll("_", " ")} • confidence{" "}
                          {Math.round(pharmacy.confidence_score * 100)}%
                        </p>
                      </div>

                      <div className="flex flex-wrap gap-2 sm:items-center">
                        <button
                          onClick={() => handleReserve(pharmacy.pharmacy_id)}
                          disabled={reserveLoading === pharmacy.pharmacy_id || !user?.roles.includes("patient")}
                          className="flex items-center justify-center gap-2 rounded-xl bg-primary px-4 py-2.5 text-sm font-medium text-primary-foreground shadow-sm transition-colors hover:bg-primary-800 disabled:opacity-60"
                        >
                          {reserveLoading === pharmacy.pharmacy_id ? <Loader2 className="h-4 w-4 animate-spin" /> : <CheckCircle2 className="h-4 w-4" />}
                          Reserve Now
                        </button>
                        {!user ? (
                          <Link href="/auth" className="rounded-xl border border-border px-4 py-2.5 text-sm font-medium">
                            Sign in to reserve
                          </Link>
                        ) : null}
                      </div>
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>
        ) : null}
      </main>
    </div>
  );
}
