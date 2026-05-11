"use client";

import { Suspense, useEffect, useMemo, useState } from "react";
import { Activity, AlertCircle, ArrowRight, Loader2, Search, ShieldCheck } from "lucide-react";
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";

import { Navbar } from "@/components/navbar";
import { useAuth } from "@/lib/auth";
import { apiRequest } from "@/lib/api";

type SearchResult = {
  medicine_id: string;
  canonical_name: string;
  generic_name: string;
  strength?: string | null;
  form?: string | null;
  matched_alias?: string;
};

function SearchContent() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const initialQuery = useMemo(() => searchParams.get("q") ?? "", [searchParams]);
  const { hydrated, token } = useAuth();
  const [query, setQuery] = useState(initialQuery);
  const [results, setResults] = useState<SearchResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [searchFailure, setSearchFailure] = useState(false);

  useEffect(() => {
    if (!hydrated || initialQuery.trim().length < 2) {
      return;
    }

    const controller = new AbortController();
    const run = async () => {
      setLoading(true);
      setError(null);
      try {
        const payload = await apiRequest<{ results: SearchResult[]; search_failure: boolean }>(
          `/api/v1/medicine/search?q=${encodeURIComponent(initialQuery)}`,
          { token },
        );
        if (!controller.signal.aborted) {
          setResults(payload.results);
          setSearchFailure(payload.search_failure);
          setQuery(initialQuery);
        }
      } catch (err: unknown) {
        if (!controller.signal.aborted) {
          setError(err instanceof Error ? err.message : "Unable to load search results");
          setResults([]);
        }
      } finally {
        if (!controller.signal.aborted) {
          setLoading(false);
        }
      }
    };

    void run();

    return () => controller.abort();
  }, [hydrated, token, initialQuery]);

  const handleSubmit = () => {
    if (query.trim().length < 2) {
      return;
    }
    router.push(`/search?q=${encodeURIComponent(query.trim())}`);
  };

  return (
    <div className="min-h-screen bg-muted/20">
      <Navbar />
      <main className="mx-auto w-full max-w-5xl px-4 py-8">
        <div className="mb-8 flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
          <div>
            <h1 className="text-2xl font-semibold">
              Search medicines and nearby verified stock
            </h1>
            <p className="mt-1 text-sm text-muted-foreground">
              Brand names, generics, and common aliases resolve against the backend registry.
            </p>
          </div>

          <div className="relative w-full md:w-80">
            <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
            <input
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter") {
                  handleSubmit();
                }
              }}
              className="w-full rounded-xl border border-border bg-background py-3 pl-10 pr-24 text-sm outline-none focus:border-primary"
              placeholder="Search medicine or symptom"
            />
            <button
              onClick={handleSubmit}
              className="absolute right-2 top-1/2 -translate-y-1/2 rounded-lg bg-primary px-3 py-2 text-xs font-semibold text-primary-foreground"
            >
              Search
            </button>
          </div>
        </div>

        {!hydrated ? (
          <div className="rounded-2xl border border-border bg-card p-8 text-center shadow-sm">
            <Loader2 className="mx-auto mb-3 h-6 w-6 animate-spin text-primary" />
            <p className="text-sm text-muted-foreground">Preparing session...</p>
          </div>
        ) : loading ? (
          <div className="rounded-2xl border border-border bg-card p-8 text-center shadow-sm">
            <Loader2 className="mx-auto mb-3 h-6 w-6 animate-spin text-primary" />
            <p className="text-sm text-muted-foreground">Searching verified medicine records...</p>
          </div>
        ) : error ? (
          <div className="rounded-2xl border border-rose-200 bg-rose-50 p-8 shadow-sm">
            <div className="flex items-start gap-3">
              <AlertCircle className="mt-0.5 h-5 w-5 text-rose-700" />
              <div>
                <h2 className="font-semibold text-rose-900">Search failed</h2>
                <p className="mt-1 text-sm text-rose-700">{error}</p>
              </div>
            </div>
          </div>
        ) : results.length === 0 ? (
          <div className="rounded-2xl border border-border bg-card p-8 shadow-sm">
            <h2 className="text-xl font-semibold">No verified medicine match found</h2>
            <p className="mt-2 text-sm text-muted-foreground">
              This query has been captured as search-failure intelligence in the backend. Try a generic name, dosage, or another description.
            </p>
            {searchFailure ? (
              <p className="mt-3 text-xs font-medium text-primary">
                Search failure recorded for shortage and distributor analytics.
              </p>
            ) : null}
          </div>
        ) : (
          <div className="space-y-4">
            {results.map((result, index) => (
              <Link
                key={result.medicine_id}
                href={`/medicine/${result.medicine_id}`}
                className="block rounded-2xl border border-border bg-card p-5 shadow-sm transition-colors hover:border-primary/50"
              >
                <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
                  <div className="flex items-start gap-4">
                    <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-primary/10">
                      <Activity className="h-6 w-6 text-primary" />
                    </div>
                    <div>
                      <div className="flex flex-wrap items-center gap-2">
                        <h3 className="text-xl font-bold tracking-tight text-foreground">
                          {result.canonical_name}
                          {result.strength ? ` ${result.strength}` : ""}
                        </h3>
                        {index === 0 ? (
                          <span className="rounded-sm bg-primary/10 px-2 py-0.5 text-[10px] font-semibold uppercase tracking-widest text-primary">
                            Best Match
                          </span>
                        ) : null}
                      </div>
                      <p className="mb-2 text-sm text-muted-foreground">
                        {result.generic_name}
                        {result.form ? ` • ${result.form}` : ""}
                      </p>
                      <div className="flex items-center gap-1.5 rounded-md bg-emerald-50 px-2 py-1 text-xs font-medium text-emerald-700">
                        <ShieldCheck className="h-3.5 w-3.5" />
                        Matched via {result.matched_alias ?? "canonical registry"}
                      </div>
                    </div>
                  </div>

                  <div className="flex items-center gap-6 border-t border-border pt-4 md:border-l md:border-t-0 md:pl-6 md:pt-0">
                    <div>
                      <p className="text-sm font-semibold text-foreground">Open detail</p>
                      <p className="text-xs text-muted-foreground">Availability and reservation flow</p>
                    </div>
                    <div className="flex h-10 w-10 items-center justify-center rounded-full bg-primary/5 transition-colors group-hover:bg-primary group-hover:text-primary-foreground">
                      <ArrowRight className="h-5 w-5" />
                    </div>
                  </div>
                </div>
              </Link>
            ))}
          </div>
        )}
      </main>
    </div>
  );
}

export default function SearchPage() {
  return (
    <Suspense
      fallback={
        <div className="min-h-screen bg-muted/20">
          <Navbar />
          <main className="mx-auto w-full max-w-5xl px-4 py-8">
            <div className="rounded-2xl border border-border bg-card p-8 text-center shadow-sm">
              <Loader2 className="mx-auto mb-3 h-6 w-6 animate-spin text-primary" />
              <p className="text-sm text-muted-foreground">Loading search...</p>
            </div>
          </main>
        </div>
      }
    >
      <SearchContent />
    </Suspense>
  );
}
