"use client";

import { useState } from "react";
import { Navbar } from "@/components/navbar";
import { Search, MapPin, Activity, ShieldCheck, Clock, ArrowRight, CornerRightDown, Users } from "lucide-react";
import Link from 'next/link';

export default function Home() {
  const [query, setQuery] = useState("");

  return (
    <div className="min-h-screen flex flex-col bg-background selection:bg-primary/20 pb-20 md:pb-0">
      <Navbar />

      <main className="flex-1 flex flex-col items-center px-4 md:px-8 mt-8 md:mt-24">
        {/* Hero Section */}
        <div className="w-full max-w-3xl space-y-8 flex flex-col items-center text-center">

          <div className="space-y-4">
            <h1 className="text-4xl md:text-6xl font-semibold tracking-tight text-foreground leading-[1.1]">
              Find life-saving medicine. <br /> <span className="text-primary italic font-serif opacity-90">Instantly.</span>
            </h1>
            <p className="text-lg md:text-xl text-muted-foreground max-w-xl mx-auto font-light leading-relaxed">
              We verify real-time inventory across trusted pharmacies in Ethiopia, so you never travel in vain.
            </p>
          </div>

          {/* Search Bar Component */}
          <div className="w-full max-w-2xl relative group mt-8">
            <div className="absolute inset-0 bg-primary/5 rounded-2xl blur-xl group-hover:bg-primary/10 transition-colors pointer-events-none" />
            <div className="relative bg-card border border-border/80 shadow-sm hover:shadow-md transition-shadow rounded-2xl p-2 pl-4 flex items-center">
              <div className="text-primary/60 flex-shrink-0">
                <Search className="w-6 h-6" />
              </div>
              <input
                type="text"
                className="w-full text-lg bg-transparent outline-none placeholder:text-muted-foreground/50 p-3 ml-2 font-medium"
                placeholder="Search medication, generic, symptom..."
                value={query}
                autoFocus
                onChange={(e) => setQuery(e.target.value)}
              />
              <Link href={query ? `/search?q=${encodeURIComponent(query)}` : '#'} className="flex-shrink-0 bg-primary hover:bg-primary-800 text-primary-foreground px-6 py-3.5 rounded-xl font-medium transition-colors flex items-center gap-2 shadow-sm">
                Search
                <ArrowRight className="w-4 h-4 hidden sm:block" />
              </Link>
            </div>

            {/* Smart Suggestions Dropdown */}
            {query.length > 0 && (
              <div className="absolute top-[calc(100%+8px)] left-0 right-0 bg-card border border-border/50 rounded-xl shadow-lg overflow-hidden z-20 animate-in fade-in slide-in-from-top-2 duration-200">
                <div className="p-2 border-b border-border/30 bg-muted/20">
                  <span className="text-xs font-semibold text-muted-foreground uppercase tracking-wider pl-2">Medical Intelligence</span>
                </div>

                {[1, 2].map((idx) => (
                  <Link href={`/search?q=${query}`} key={idx} className="p-3 hover:bg-muted/40 cursor-pointer flex items-center gap-4 transition-colors">
                    <div className="w-10 h-10 rounded-full bg-primary/10 flex items-center justify-center flex-shrink-0">
                      <Activity className="w-5 h-5 text-primary" />
                    </div>
                    <div className="flex-1 text-left">
                      <h4 className="font-semibold text-foreground text-sm md:text-base capitalize">{query}{idx === 1 ? ' 500mg' : ' generic variant'}</h4>
                      <div className="flex items-center gap-1.5 mt-0.5">
                        <ShieldCheck className="w-3.5 h-3.5 text-primary/70" />
                        <p className="text-xs text-muted-foreground">{idx === 1 ? '45 pharmacies nearby' : 'Available at trusted hubs'}</p>
                      </div>
                    </div>
                    <CornerRightDown className="w-5 h-5 text-muted-foreground/30 mr-2" />
                  </Link>
                ))}
              </div>
            )}

            <div className="mt-3 flex items-center justify-center gap-2 text-sm text-muted-foreground font-medium">
              <span className="text-primary/70">Or</span>
              <Link href="/prescriptions/upload" className="text-primary hover:underline underline-offset-4 font-semibold text-sm">
                Scan your prescription
              </Link>
            </div>
          </div>

          {/* Quick Stats / Trust Indicators */}
          <div className="pt-16 pb-8 grid grid-cols-2 lg:grid-cols-4 gap-4 md:gap-8 w-full text-left">
            {[
              { icon: ShieldCheck, title: "1,240+", subtitle: "Verified Pharmacies" },
              { icon: Clock, title: "Real-Time", subtitle: "Stock Reliability" },
              { icon: MapPin, title: "Addis Ababa", subtitle: "& Regional coverage" },
              { icon: Users, title: "Community", subtitle: "Crowdsourced reports" }
            ].map((stat, i) => (
              <div key={i} className="flex flex-col items-center md:items-start text-center md:text-left gap-1.5 p-4 rounded-2xl bg-card border border-border/30 shadow-sm">
                <div className="w-10 h-10 bg-primary/5 rounded-full flex items-center justify-center mb-2">
                  <stat.icon className="w-5 h-5 text-primary" />
                </div>
                <p className="text-lg md:text-xl font-bold text-foreground">{stat.title}</p>
                <p className="text-xs text-muted-foreground font-medium">{stat.subtitle}</p>
              </div>
            ))}
          </div>

        </div>
      </main>
    </div>
  );
}
