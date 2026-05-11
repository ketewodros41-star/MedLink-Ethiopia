"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import { BellRing, Check, Loader2, Search, Store, X } from "lucide-react";

import { useAuth } from "@/lib/auth";
import { apiRequest } from "@/lib/api";

type QueueReservation = {
  reservation_id: string;
  patient_id: string;
  status: string;
  quantity: number;
  expires_at: string;
  medicine: { id: string; canonical_name: string; strength?: string | null };
};

type InventoryItem = {
  inventory_id: string;
  quantity_available: number;
  quantity_reserved: number;
  state: string;
  confidence_score: number;
  medicine: { id: string; canonical_name: string; strength?: string | null; generic_name: string };
};

export default function PharmacyDashboard() {
  const { hydrated, token, user, login } = useAuth();
  const [tab, setTab] = useState<"reservations" | "inventory">("reservations");
  const [queue, setQueue] = useState<QueueReservation[]>([]);
  const [inventory, setInventory] = useState<InventoryItem[]>([]);
  const [loading, setLoading] = useState(false);
  const [search, setSearch] = useState("");
  const [quantities, setQuantities] = useState<Record<string, number>>({});
  const [message, setMessage] = useState<string | null>(null);

  const loadDashboard = useCallback(async () => {
    if (!token) return;
    setLoading(true);
    const [queueResponse, inventoryResponse] = await Promise.all([
      apiRequest<{ results: QueueReservation[] }>("/api/v1/reservations/pharmacy-queue", { token }),
      apiRequest<{ results: InventoryItem[] }>("/api/v1/inventory/pharmacy-items", { token }),
    ]);
    setQueue(queueResponse.results);
    setInventory(inventoryResponse.results);
    setQuantities(
      Object.fromEntries(inventoryResponse.results.map((item) => [item.inventory_id, item.quantity_available])),
    );
    setLoading(false);
  }, [token]);

  useEffect(() => {
    if (!hydrated || !token || !user?.roles.includes("pharmacist")) {
      return;
    }
    const timer = window.setTimeout(() => {
      void loadDashboard();
    }, 0);
    return () => window.clearTimeout(timer);
  }, [hydrated, token, user, loadDashboard]);

  const filteredInventory = useMemo(() => {
    const term = search.trim().toLowerCase();
    if (!term) return inventory;
    return inventory.filter((item) =>
      `${item.medicine.canonical_name} ${item.medicine.generic_name}`.toLowerCase().includes(term),
    );
  }, [inventory, search]);

  const handleQueueAction = async (reservationId: string, status: "approved" | "cancelled") => {
    if (!token) return;
    await apiRequest(`/api/v1/reservations/${reservationId}`, {
      method: "PATCH",
      token,
      body: { status },
    });
    setMessage(`Reservation ${status}.`);
    await loadDashboard();
  };

  const handleInventoryUpdate = async (item: InventoryItem) => {
    if (!token) return;
    await apiRequest("/api/v1/inventory/verify", {
      method: "POST",
      token,
      body: {
        pharmacy_id: user?.pharmacy_id,
        medicine_id: item.medicine.id,
        action: "set",
        quantity: Number(quantities[item.inventory_id] ?? item.quantity_available),
      },
    });
    setMessage(`Inventory updated for ${item.medicine.canonical_name}.`);
    await loadDashboard();
  };

  if (!hydrated) {
    return <div className="min-h-screen bg-muted/20" />;
  }

  if (!user || !user.roles.includes("pharmacist")) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-muted/20 p-6">
        <div className="max-w-md rounded-3xl border border-border bg-card p-8 shadow-sm">
          <h1 className="text-2xl font-bold">Pharmacist access required</h1>
          <p className="mt-2 text-sm text-muted-foreground">
            This dashboard is connected to pharmacist-only backend routes. Continue as the demo pharmacist to operate real inventory and reservation data.
          </p>
          <button
            onClick={() => void login("pharmacist", "pharmacist-demo")}
            className="mt-5 rounded-xl bg-primary px-5 py-3 text-sm font-semibold text-primary-foreground"
          >
            Continue as pharmacist
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-muted/20 pb-safe">
      <header className="sticky top-0 z-50 bg-primary text-primary-foreground shadow-sm">
        <div className="flex h-16 items-center justify-between px-4">
          <div className="flex items-center gap-2">
            <Store className="h-5 w-5" />
            <h1 className="text-lg font-semibold">{user.pharmacy_name ?? "Pharmacy Dashboard"}</h1>
          </div>
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-1.5 rounded-full border border-emerald-500/30 bg-emerald-500/20 px-2 py-0.5 text-xs font-medium text-emerald-100">
              <span className="h-2 w-2 animate-pulse rounded-full bg-emerald-400" />
              Online
            </div>
            <BellRing className="h-6 w-6" />
          </div>
        </div>

        <div className="flex w-full">
          <button
            onClick={() => setTab("reservations")}
            className={`relative flex-1 py-4 text-sm font-semibold uppercase tracking-wide ${tab === "reservations" ? "text-white" : "text-primary-foreground/60"}`}
          >
            Pending ({queue.filter((item) => item.status === "pending").length})
            {tab === "reservations" ? <div className="absolute bottom-0 left-0 right-0 h-1 rounded-t-sm bg-white" /> : null}
          </button>
          <button
            onClick={() => setTab("inventory")}
            className={`relative flex-1 py-4 text-sm font-semibold uppercase tracking-wide ${tab === "inventory" ? "text-white" : "text-primary-foreground/60"}`}
          >
            Update Stock
            {tab === "inventory" ? <div className="absolute bottom-0 left-0 right-0 h-1 rounded-t-sm bg-white" /> : null}
          </button>
        </div>
      </header>

      <main className="mx-auto max-w-3xl space-y-4 p-4 pt-6">
        {message ? <div className="rounded-2xl border border-emerald-200 bg-emerald-50 p-4 text-sm text-emerald-800">{message}</div> : null}
        {loading ? (
          <div className="rounded-2xl border border-border bg-card p-8 text-center shadow-sm">
            <Loader2 className="mx-auto h-6 w-6 animate-spin text-primary" />
          </div>
        ) : null}

        {!loading && tab === "reservations" ? (
          <div className="space-y-4">
            {queue.length === 0 ? (
              <div className="rounded-2xl border border-border bg-card p-6 shadow-sm">
                <p className="text-sm text-muted-foreground">No reservation requests in the pharmacy queue.</p>
              </div>
            ) : (
              queue.map((reservation) => (
                <div key={reservation.reservation_id} className="rounded-2xl border border-border bg-card p-5 shadow-sm">
                  <div className="mb-4 flex items-start justify-between">
                    <div>
                      <h3 className="text-lg font-bold leading-tight">
                        {reservation.medicine.canonical_name}
                        {reservation.medicine.strength ? ` ${reservation.medicine.strength}` : ""}
                      </h3>
                      <p className="text-sm font-medium text-muted-foreground">
                        {reservation.quantity} requested by {reservation.patient_id}
                      </p>
                    </div>
                    <div className="text-right">
                      <span className="mb-1 inline-block rounded-md bg-orange-100 px-2 py-1 text-xs font-bold text-orange-800">
                        {reservation.status}
                      </span>
                      <p className="text-xs text-muted-foreground">
                        Due {new Date(reservation.expires_at).toLocaleTimeString()}
                      </p>
                    </div>
                  </div>

                  <div className="flex gap-3">
                    <button
                      onClick={() => void handleQueueAction(reservation.reservation_id, "cancelled")}
                      className="flex flex-1 items-center justify-center gap-2 rounded-xl border border-rose-200 bg-rose-50 py-4 font-bold text-rose-700"
                    >
                      <X className="h-5 w-5 stroke-[3]" /> Cancel
                    </button>
                    <button
                      onClick={() => void handleQueueAction(reservation.reservation_id, "approved")}
                      className="flex flex-1 items-center justify-center gap-2 rounded-xl bg-primary py-4 font-bold text-primary-foreground shadow-sm"
                    >
                      <Check className="h-5 w-5 stroke-[3]" /> Approve
                    </button>
                  </div>
                </div>
              ))
            )}
          </div>
        ) : null}

        {!loading && tab === "inventory" ? (
          <div className="space-y-4">
            <div className="relative">
              <Search className="absolute left-4 top-1/2 h-5 w-5 -translate-y-1/2 text-muted-foreground" />
              <input
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                placeholder="Search stock to update..."
                className="w-full rounded-2xl border border-border bg-card py-4 pl-12 pr-4 text-lg shadow-sm focus:border-primary focus:outline-none"
              />
            </div>

            {filteredInventory.map((item) => (
              <div key={item.inventory_id} className="rounded-2xl border border-border bg-card p-4 shadow-sm">
                <div className="mb-3 flex items-center justify-between gap-4">
                  <div>
                    <h4 className="text-lg font-semibold">
                      {item.medicine.canonical_name}
                      {item.medicine.strength ? ` ${item.medicine.strength}` : ""}
                    </h4>
                    <p className="text-sm text-muted-foreground">
                      {item.medicine.generic_name} • state {item.state.replaceAll("_", " ")} • confidence {Math.round(item.confidence_score * 100)}%
                    </p>
                  </div>
                  <span className="rounded-md bg-primary/10 px-3 py-1 text-xs font-semibold text-primary">
                    Reserved {item.quantity_reserved}
                  </span>
                </div>
                <div className="flex flex-col gap-3 sm:flex-row sm:items-center">
                  <input
                    type="number"
                    min={0}
                    value={quantities[item.inventory_id] ?? item.quantity_available}
                    onChange={(e) =>
                      setQuantities((current) => ({
                        ...current,
                        [item.inventory_id]: Number(e.target.value),
                      }))
                    }
                    className="w-full rounded-xl border border-border bg-muted/40 px-4 py-3 outline-none focus:border-primary sm:max-w-[140px]"
                  />
                  <button
                    onClick={() => void handleInventoryUpdate(item)}
                    className="rounded-xl bg-primary px-4 py-3 font-semibold text-primary-foreground"
                  >
                    Confirm quantity
                  </button>
                </div>
              </div>
            ))}
          </div>
        ) : null}
      </main>
    </div>
  );
}
