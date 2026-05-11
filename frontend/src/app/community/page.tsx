"use client";

import { useCallback, useEffect, useState } from "react";
import { Activity, Camera, CheckCircle2, Loader2, MapPin, Users } from "lucide-react";
import Link from "next/link";

import { Navbar } from "@/components/navbar";
import { useAuth } from "@/lib/auth";
import { apiRequest } from "@/lib/api";

type FeedItem = {
  report_id: string;
  user_id: string;
  is_available: boolean;
  notes?: string | null;
  created_at: string;
  reputation_weight: number;
  medicine: { id: string; canonical_name: string };
  pharmacy: { id: string; name: string; city: string };
};

type PharmacyOption = { id: string; name: string; city: string };
type SearchResult = { medicine_id: string; canonical_name: string; strength?: string | null };

export default function CommunityWatch() {
  const { hydrated, token, user, login } = useAuth();
  const [feed, setFeed] = useState<FeedItem[]>([]);
  const [pharmacies, setPharmacies] = useState<PharmacyOption[]>([]);
  const [medicineQuery, setMedicineQuery] = useState("amoxicillin");
  const [medicineResults, setMedicineResults] = useState<SearchResult[]>([]);
  const [selectedMedicineId, setSelectedMedicineId] = useState<string>("");
  const [selectedPharmacyId, setSelectedPharmacyId] = useState<string>("");
  const [notes, setNotes] = useState("");
  const [isAvailable, setIsAvailable] = useState(true);
  const [message, setMessage] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const loadPage = useCallback(async () => {
    if (!token) return;
    setLoading(true);
    const [feedResponse, pharmacyResponse, searchResponse] = await Promise.all([
      apiRequest<{ results: FeedItem[] }>("/api/v1/community/feed", { token }),
      apiRequest<{ results: PharmacyOption[] }>("/api/v1/pharmacy/directory", { token }),
      apiRequest<{ results: SearchResult[] }>(`/api/v1/medicine/search?q=${encodeURIComponent(medicineQuery)}`, { token }),
    ]);
    setFeed(feedResponse.results);
    setPharmacies(pharmacyResponse.results);
    setMedicineResults(searchResponse.results);
    setSelectedMedicineId(searchResponse.results[0]?.medicine_id ?? "");
    setSelectedPharmacyId(pharmacyResponse.results[0]?.id ?? "");
    setLoading(false);
  }, [medicineQuery, token]);

  useEffect(() => {
    if (!hydrated) {
      return;
    }
    const timer = window.setTimeout(() => {
      void loadPage();
    }, 0);
    return () => window.clearTimeout(timer);
  }, [hydrated, token, loadPage]);

  const handleRefreshMedicine = async () => {
    if (!token || medicineQuery.trim().length < 2) return;
    const payload = await apiRequest<{ results: SearchResult[] }>(
      `/api/v1/medicine/search?q=${encodeURIComponent(medicineQuery)}`,
      { token },
    );
    setMedicineResults(payload.results);
    setSelectedMedicineId(payload.results[0]?.medicine_id ?? "");
  };

  const handleSubmit = async () => {
    if (!token || !selectedMedicineId || !selectedPharmacyId) return;
    await apiRequest("/api/v1/community/report", {
      method: "POST",
      token,
      body: {
        medicine_id: selectedMedicineId,
        pharmacy_id: selectedPharmacyId,
        is_available: isAvailable,
        notes: notes || (isAvailable ? "Community confirmation submitted from frontend." : "Unavailable during visit."),
      },
    });
    setMessage("Community report submitted.");
    setNotes("");
    await loadPage();
  };

  return (
    <div className="min-h-screen bg-muted/10 pb-20 md:pb-0">
      <Navbar />
      <main className="mx-auto max-w-5xl px-4 py-8">
        <div className="mb-8 flex flex-col gap-6 md:flex-row md:items-end md:justify-between">
          <div className="space-y-2">
            <span className="inline-flex items-center gap-1.5 rounded-full border border-primary/20 bg-primary/10 px-3 py-1 text-xs font-bold uppercase tracking-wider text-primary">
              <Users className="h-3.5 w-3.5" />
              Community Network
            </span>
            <h1 className="text-3xl font-bold tracking-tight">Community stock watch</h1>
            <p className="max-w-md text-sm text-muted-foreground">
              Submit real sightings and view recent community reports from the backend feed.
            </p>
          </div>
          {!user ? (
            <Link href="/auth" className="rounded-xl bg-primary px-5 py-3 font-semibold text-primary-foreground">
              Sign in to submit reports
            </Link>
          ) : null}
        </div>

        {!hydrated || loading ? (
          <div className="rounded-2xl border border-border bg-card p-8 text-center shadow-sm">
            <Loader2 className="mx-auto h-6 w-6 animate-spin text-primary" />
          </div>
        ) : (
          <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
            <div className="space-y-4 lg:col-span-2">
              {feed.length === 0 ? (
                <div className="rounded-2xl border border-border bg-card p-6 shadow-sm">
                  <p className="text-sm text-muted-foreground">No community reports yet. Submit the first one.</p>
                </div>
              ) : (
                feed.map((report) => (
                  <div key={report.report_id} className="rounded-2xl border border-border bg-card p-5 shadow-sm">
                    <div className="flex items-start gap-4">
                      <div className="flex h-12 w-12 flex-shrink-0 items-center justify-center rounded-full bg-emerald-100 text-lg font-bold text-emerald-700">
                        {report.user_id.slice(0, 1).toUpperCase()}
                      </div>
                      <div className="flex-1">
                        <div className="flex items-center justify-between">
                          <div className="flex items-center gap-2">
                            <h3 className="font-bold text-foreground">{report.user_id}</h3>
                            <span className="rounded bg-amber-100/50 px-1.5 py-0.5 text-[10px] font-bold uppercase text-amber-700">
                              Weight {Math.round(report.reputation_weight * 100)}
                            </span>
                          </div>
                          <span className="text-xs font-medium text-muted-foreground">
                            {new Date(report.created_at).toLocaleString()}
                          </span>
                        </div>
                        <p className="my-2 text-sm text-foreground">
                          {report.is_available ? "Confirmed availability for " : "Reported shortage for "}
                          <span className="rounded bg-primary/10 px-1 text-primary">{report.medicine.canonical_name}</span> at{" "}
                          <span className="font-semibold">{report.pharmacy.name}</span>.
                        </p>
                        <div className="my-4 flex flex-col items-start justify-between gap-3 rounded-xl bg-muted p-3 sm:flex-row sm:items-center">
                          <div className="flex items-center gap-2">
                            <MapPin className="h-4 w-4 text-muted-foreground" />
                            <span className="text-sm font-semibold">{report.pharmacy.city}</span>
                          </div>
                          <div className="flex items-center gap-2 rounded-lg border border-emerald-200 bg-emerald-50 px-3 py-1.5 text-xs font-semibold text-emerald-700">
                            <CheckCircle2 className="h-4 w-4" />
                            {report.is_available ? "Available" : "Unavailable"}
                          </div>
                        </div>
                        {report.notes ? <p className="text-sm text-muted-foreground">{report.notes}</p> : null}
                      </div>
                    </div>
                  </div>
                ))
              )}
            </div>

            <div className="space-y-6">
              <div className="rounded-3xl border border-border bg-card p-6 shadow-sm">
                <h3 className="mb-4 flex items-center gap-2 text-lg font-bold">
                  <Camera className="h-5 w-5 text-primary" />
                  Submit a report
                </h3>
                {!user ? (
                  <div className="space-y-3">
                    <p className="text-sm text-muted-foreground">
                      Reading the community feed is public. Submitting sightings requires a signed-in patient or pharmacist session.
                    </p>
                    <button
                      onClick={() => void login("patient", "patient-demo")}
                      className="w-full rounded-xl bg-primary px-4 py-3 font-semibold text-primary-foreground"
                    >
                      Continue as patient
                    </button>
                  </div>
                ) : (
                <div className="space-y-3">
                  <input
                    value={medicineQuery}
                    onChange={(e) => setMedicineQuery(e.target.value)}
                    className="w-full rounded-xl border border-border bg-muted/40 px-4 py-3 outline-none focus:border-primary"
                    placeholder="Search medicine"
                  />
                  <button onClick={handleRefreshMedicine} className="w-full rounded-xl border border-border px-4 py-3 text-sm font-semibold">
                    Refresh medicine matches
                  </button>
                  <select
                    value={selectedMedicineId}
                    onChange={(e) => setSelectedMedicineId(e.target.value)}
                    className="w-full rounded-xl border border-border bg-muted/40 px-4 py-3 outline-none"
                  >
                    {medicineResults.map((item) => (
                      <option key={item.medicine_id} value={item.medicine_id}>
                        {item.canonical_name} {item.strength ?? ""}
                      </option>
                    ))}
                  </select>
                  <select
                    value={selectedPharmacyId}
                    onChange={(e) => setSelectedPharmacyId(e.target.value)}
                    className="w-full rounded-xl border border-border bg-muted/40 px-4 py-3 outline-none"
                  >
                    {pharmacies.map((pharmacy) => (
                      <option key={pharmacy.id} value={pharmacy.id}>
                        {pharmacy.name} • {pharmacy.city}
                      </option>
                    ))}
                  </select>
                  <div className="flex gap-2">
                    <button
                      onClick={() => setIsAvailable(true)}
                      className={`flex-1 rounded-xl px-4 py-3 text-sm font-semibold ${isAvailable ? "bg-primary text-primary-foreground" : "border border-border"}`}
                    >
                      Available
                    </button>
                    <button
                      onClick={() => setIsAvailable(false)}
                      className={`flex-1 rounded-xl px-4 py-3 text-sm font-semibold ${!isAvailable ? "bg-rose-600 text-white" : "border border-border"}`}
                    >
                      Unavailable
                    </button>
                  </div>
                  <textarea
                    value={notes}
                    onChange={(e) => setNotes(e.target.value)}
                    rows={4}
                    className="w-full rounded-xl border border-border bg-muted/40 px-4 py-3 outline-none focus:border-primary"
                    placeholder="Notes about the sighting or shortage"
                  />
                  <button onClick={handleSubmit} className="w-full rounded-xl bg-primary px-4 py-3 font-semibold text-primary-foreground">
                    Submit report
                  </button>
                  {message ? <p className="text-sm text-emerald-700">{message}</p> : null}
                </div>
                )}
              </div>

              <div className="rounded-3xl border border-border bg-card p-6 shadow-sm">
                <h3 className="mb-4 flex items-center gap-2 text-lg font-bold">
                  <Activity className="h-5 w-5 text-rose-600" />
                  Why this matters
                </h3>
                <p className="text-sm text-muted-foreground">
                  Community reports feed the backend trust and shortage models. This turns the page from a mock social feed into a real operational signal surface.
                </p>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
