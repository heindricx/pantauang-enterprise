import os

FRONTEND_APP = r"D:\satdat 2026\sec\pantauang-enterprise\frontend\src\app"
FRONTEND_COMPONENTS = r"D:\satdat 2026\sec\pantauang-enterprise\frontend\src\components"

# ─── 2. globals.css ───
with open(os.path.join(FRONTEND_APP, "globals.css"), "w") as f:
    f.write('''@import "tailwindcss";

@layer base {
  :root {
    --background: #f8fafc;
    --foreground: #1e293b;
    --cp-blue: #1E88E5;
    --cp-coral: #FF8A65;
    --cp-purple: #7E57C2;
    --cp-orange: #FF5722;
    --cp-cyan: #26C6DA;
  }
  html { scroll-behavior: smooth; }
  body {
    background-color: #f8fafc;
    color: #1e293b;
    overflow-x: hidden;
  }
}

.font-sans { font-family: var(--font-jakarta), "Segoe UI", sans-serif; }
.font-serif { font-family: var(--font-playfair), Georgia, serif; }

/* === GEOMETRIC GRID BACKGROUND === */
.bg-grid {
  background-color: #f8fafc;
  background-image:
    linear-gradient(rgba(148, 163, 184, 0.15) 1px, transparent 1px),
    linear-gradient(90deg, rgba(148, 163, 184, 0.15) 1px, transparent 1px);
  background-size: 40px 40px;
}

/* === DOT GRID for dark sections === */
.bg-dot-dark {
  background-color: #0f172a;
  background-image: radial-gradient(rgba(255,255,255,0.08) 1px, transparent 1px);
  background-size: 32px 32px;
}

/* === GLASS CARD === */
.glass {
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid rgba(255,255,255,0.5);
}

.glass-dark {
  background: rgba(15, 23, 42, 0.75);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid rgba(255,255,255,0.08);
}

/* === TECH BORDER === */
.tech-border {
  border: 1px solid rgba(148, 163, 184, 0.25);
  box-shadow: 0 4px 24px -4px rgba(0, 0, 0, 0.06);
  background: #ffffff;
}

/* === HOVER LIFT === */
.hover-lift {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.hover-lift:hover {
  transform: translateY(-4px) scale(1.005);
  box-shadow: 0 12px 40px -8px rgba(0, 0, 0, 0.12);
}

/* === TICKER === */
@keyframes marquee { 0% { transform: translateX(100vw); } 100% { transform: translateX(-100%); } }

/* === SCROLLBAR HIDE === */
.scrollbar-hide::-webkit-scrollbar { display: none; }
.scrollbar-hide { -ms-overflow-style: none; scrollbar-width: none; }
''')

# ─── 3. layout.tsx ───
with open(os.path.join(FRONTEND_APP, "layout.tsx"), "w") as f:
    f.write('''import type { Metadata } from "next";
import { Playfair_Display, Plus_Jakarta_Sans } from "next/font/google";
import "./globals.css";
import { Navbar } from "@/components/layout/Navbar";
import { Footer } from "@/components/layout/Footer";

const playfair = Playfair_Display({ subsets: ["latin"], variable: "--font-playfair", display: "swap" });
const jakarta = Plus_Jakarta_Sans({ subsets: ["latin"], variable: "--font-jakarta", display: "swap" });

export const metadata: Metadata = {
  title: "PantaUang Kita | Procurement Intelligence Platform",
  description: "Platform intelijen risiko pengadaan pemerintah berbasis machine learning.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="id" className={`${playfair.variable} ${jakarta.variable}`}>
      <body className="font-sans text-slate-800 flex flex-col min-h-screen bg-grid">
        <Navbar />
        <main className="flex-1 w-full pt-16">
          {children}
        </main>
        <Footer />
      </body>
    </html>
  );
}
''')

# ─── 4. Navbar.tsx ───
os.makedirs(os.path.join(FRONTEND_COMPONENTS, "layout"), exist_ok=True)
with open(os.path.join(FRONTEND_COMPONENTS, "layout/Navbar.tsx"), "w") as f:
    f.write('''"use client";
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
''')

# ─── 5. Footer.tsx ───
with open(os.path.join(FRONTEND_COMPONENTS, "layout/Footer.tsx"), "w") as f:
    f.write('''import Link from "next/link";

export function Footer() {
  return (
    <footer className="w-full bg-slate-900 text-slate-400 border-t border-slate-800 font-sans">
      <div className="max-w-7xl mx-auto px-6 py-10 grid grid-cols-1 md:grid-cols-3 gap-8">
        <div>
          <span className="font-serif font-black text-2xl tracking-tight text-white block mb-3">
            Panta<span className="text-[#1E88E5]">Uang</span>
          </span>
          <p className="text-xs leading-relaxed text-slate-500 max-w-xs">
            Platform intelijen pengadaan publik berbasis machine learning untuk deteksi anomali secara sistematis dan transparan.
          </p>
        </div>
        <div>
          <h4 className="text-slate-300 font-bold text-xs uppercase tracking-wider mb-4">Sumber Data</h4>
          <ul className="space-y-2 text-xs text-slate-500">
            <li><a href="https://inaproc.id" target="_blank" rel="noopener noreferrer" className="hover:text-slate-200 transition-colors">Inaproc — Sistem Pengadaan Nasional</a></li>
            <li><a href="https://e-rencana.lkpp.go.id" target="_blank" rel="noopener noreferrer" className="hover:text-slate-200 transition-colors">Sistem Informasi RUP — LKPP</a></li>
            <li><span className="text-slate-600">Data periode 2023–2024</span></li>
          </ul>
        </div>
        <div>
          <h4 className="text-slate-300 font-bold text-xs uppercase tracking-wider mb-4">Model & Teknologi</h4>
          <ul className="space-y-2 text-xs text-slate-500">
            <li>Distil-IndoBERT NLP Pipeline</li>
            <li>Quantile Regression LightGBM (QRLGBM)</li>
            <li>Optuna Hyperparameter Optimization</li>
          </ul>
        </div>
      </div>
      <div className="border-t border-slate-800 px-6 py-4 text-center text-xs text-slate-600">
        &copy; {new Date().getFullYear()} PantaUang Kita · Satria Data Enterprise 2026 · All rights reserved.
      </div>
    </footer>
  );
}
''')

print("Step 1: globals, layout, navbar, footer done")
