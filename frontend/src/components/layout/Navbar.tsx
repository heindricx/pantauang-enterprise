"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { Menu, X, BarChart2, Map, Database, BookOpen, Home } from "lucide-react";
import { useState } from "react";

const NAV_ITEMS = [
  { name: "Beranda", href: "/", icon: Home },
  { name: "Infografis", href: "/infografis", icon: BarChart2 },
  { name: "Peta Risiko", href: "/peta", icon: Map },
  { name: "Data Explorer", href: "/data", icon: Database },
  { name: "Metodologi", href: "/about", icon: BookOpen },
];

export function Navbar() {
  const pathname = usePathname();
  const [open, setOpen] = useState(false);

  return (
    <>
      <header className="fixed top-0 left-0 right-0 z-50 h-16 glass border-b border-white/30 shadow-sm">
        <div className="max-w-7xl mx-auto h-full px-4 sm:px-6 flex items-center justify-between">
          {/* Logo */}
          <Link href="/" className="flex items-center gap-2 shrink-0">
            <span className="font-serif font-black text-xl tracking-tight text-slate-900">
              Panta<span className="text-[#1E88E5]">Uang</span>
            </span>
            <span className="hidden sm:inline-flex items-center px-2 py-0.5 text-[10px] font-bold bg-[#1E88E5]/10 text-[#1E88E5] rounded-full border border-[#1E88E5]/20 font-sans">
              ENTERPRISE
            </span>
          </Link>

          {/* Desktop nav */}
          <nav className="hidden md:flex items-center gap-1">
            {NAV_ITEMS.map((item) => {
              const active = item.href === "/" ? pathname === "/" : pathname.startsWith(item.href);
              return (
                <Link
                  key={item.href}
                  href={item.href}
                  className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-sm font-bold font-sans transition-all duration-200 ${
                    active
                      ? "bg-slate-900 text-white shadow-sm"
                      : "text-slate-600 hover:bg-slate-100 hover:text-slate-900"
                  }`}
                >
                  <item.icon className="w-3.5 h-3.5" />
                  {item.name}
                </Link>
              );
            })}
          </nav>

          {/* Mobile hamburger */}
          <button
            className="md:hidden p-2 rounded-lg text-slate-600 hover:bg-slate-100"
            onClick={() => setOpen(!open)}
          >
            {open ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
          </button>
        </div>
      </header>

      {/* Mobile drawer */}
      <div
        className={`fixed inset-0 z-40 transition-all duration-300 md:hidden ${open ? "pointer-events-auto" : "pointer-events-none"}`}
      >
        <div className={`absolute inset-0 bg-slate-900/40 transition-opacity duration-300 ${open ? "opacity-100" : "opacity-0"}`} onClick={() => setOpen(false)} />
        <div className={`absolute top-16 left-0 right-0 glass border-b border-white/30 shadow-xl transition-transform duration-300 ${open ? "translate-y-0" : "-translate-y-4 opacity-0"}`}>
          <nav className="flex flex-col p-4 gap-1">
            {NAV_ITEMS.map((item) => {
              const active = item.href === "/" ? pathname === "/" : pathname.startsWith(item.href);
              return (
                <Link
                  key={item.href}
                  href={item.href}
                  onClick={() => setOpen(false)}
                  className={`flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-bold font-sans transition-all ${
                    active ? "bg-slate-900 text-white" : "text-slate-700 hover:bg-slate-100"
                  }`}
                >
                  <item.icon className="w-4 h-4" />
                  {item.name}
                </Link>
              );
            })}
          </nav>
        </div>
      </div>
    </>
  );
}
