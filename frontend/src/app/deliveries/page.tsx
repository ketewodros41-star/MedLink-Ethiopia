"use client";

import { Navbar } from "@/components/navbar";
import { Truck } from "lucide-react";

export default function DeliveriesPage() {
    return (
        <div className="min-h-screen flex flex-col bg-background">
            <Navbar />
            <main className="flex-1 flex flex-col items-center justify-center px-4 text-center">
                <div className="flex flex-col items-center space-y-4 max-w-sm mx-auto opacity-70">
                    <div className="w-16 h-16 bg-primary/10 text-primary rounded-full flex items-center justify-center">
                        <Truck className="w-8 h-8" />
                    </div>
                    <h2 className="text-2xl font-bold">Deliveries</h2>
                    <p className="text-muted-foreground text-center">
                        Delivery tracking and dispatch coordination will appear here. Coming soon in phase 2.
                    </p>
                </div>
            </main>
        </div>
    );
}
