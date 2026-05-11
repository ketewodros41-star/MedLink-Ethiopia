"use client";

import { Calendar, FileText, LogIn, Search, Store, Truck, User, Users } from "lucide-react";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";

import { useAuth } from "@/lib/auth";
import { cn } from "@/lib/utils";

const NAV_ITEMS = [
  { name: "Search", href: "/", icon: Search },
  { name: "Prescriptions", href: "/prescriptions/upload", icon: FileText },
  { name: "Pharmacies", href: "/pharmacies", icon: Store },
  { name: "Reservations", href: "/reservations", icon: Calendar },
  { name: "Community", href: "/community", icon: Users },
  { name: "Deliveries", href: "/deliveries", icon: Truck },
];

export function Navbar() {
  const pathname = usePathname();
  const router = useRouter();
  const { user, logout } = useAuth();

  const handleAccountClick = () => {
    if (!user) {
      router.push("/auth");
      return;
    }
    if (user.roles.includes("pharmacist")) {
      router.push("/pharmacy");
      return;
    }
    router.push("/reservations");
  };

  return (
    <nav className="sticky top-0 z-50 w-full border-b border-border/40 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container mx-auto flex h-16 items-center justify-between px-4 md:px-8">
        <Link href="/" className="flex items-center space-x-2">
          <span className="text-xl font-semibold tracking-tight text-primary">MedLink</span>
          <span className="hidden text-xl font-light tracking-tight text-primary/80 sm:inline-block">Ethiopia</span>
        </Link>

        <div className="hidden flex-1 items-center justify-center space-x-6 text-sm font-medium md:flex">
          {NAV_ITEMS.map((item) => {
            const isActive = item.href === "/" ? pathname === "/" : pathname.startsWith(item.href);
            return (
              <Link
                key={item.name}
                href={item.href}
                className={cn(
                  "flex items-center gap-2 transition-colors hover:text-primary",
                  isActive ? "text-primary font-semibold" : "text-foreground/60",
                )}
              >
                <item.icon className="h-4 w-4" />
                {item.name}
              </Link>
            );
          })}
          <Link
            href="/auth/pharmacist"
            className={cn(
              "transition-colors hover:text-primary",
              pathname.startsWith("/auth/pharmacist") || pathname.startsWith("/pharmacy")
                ? "text-primary font-semibold"
                : "text-foreground/60",
            )}
          >
            Pharmacy Portal
          </Link>
        </div>

        <div className="flex items-center gap-3">
          {user ? (
            <div className="hidden rounded-full bg-primary/5 px-3 py-1 text-xs font-semibold text-primary sm:block">
              {user.roles[0]}: {user.sub}
            </div>
          ) : null}
          <button
            onClick={handleAccountClick}
            className="flex items-center justify-center rounded-full bg-secondary p-2 transition-colors hover:bg-secondary/80"
          >
            {user ? <User className="h-5 w-5 text-secondary-foreground" /> : <LogIn className="h-5 w-5 text-secondary-foreground" />}
          </button>
          {user ? (
            <button onClick={logout} className="hidden text-sm font-medium text-muted-foreground hover:text-foreground sm:block">
              Logout
            </button>
          ) : null}
        </div>
      </div>

      <div className="fixed bottom-0 left-0 right-0 z-50 flex h-[72px] items-center justify-around border-t bg-background pb-2 pt-1 shadow-[0_-4px_10px_rgba(0,0,0,0.05)] md:hidden">
        {NAV_ITEMS.slice(0, 5).map((item) => {
          const isActive = item.href === "/" ? pathname === "/" : pathname.startsWith(item.href);
          return (
            <Link
              key={item.name}
              href={item.href}
              className={cn(
                "flex h-full w-full flex-col items-center justify-center space-y-1 transition-colors hover:text-primary",
                isActive ? "text-primary" : "text-foreground/50",
              )}
            >
              <item.icon className="mb-1 h-6 w-6" />
              <span className="text-[10px] font-medium tracking-wide">{item.name}</span>
            </Link>
          );
        })}
      </div>
    </nav>
  );
}
