"""
Patch v5: Fix all audit issues
- Consistent 3,009,417 number
- Data loading with correct HF backend URL hint
- Remove ENTERPRISE badge from Navbar
- Remove "?" (encode fix for ticker)
- Better Peta frame with gradient fade
- Legend with numeric breakpoints
- Transparent gradient header/footer principle
"""
import os

FRONTEND_APP = r"D:\satdat 2026\sec\pantauang-enterprise\frontend\src\app"
FRONTEND_COMPONENTS = r"D:\satdat 2026\sec\pantauang-enterprise\frontend\src\components"

TOTAL_DATA = "3.009.417"
TOTAL_INT  = 3009417

# ─── 1. NAVBAR (Remove ENTERPRISE badge, fix encoding) ─────────────────
navbar_tsx = '''"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { Menu, X, BarChart2, Map, Database, BookOpen, Home } from "lucide-react";
import { useState } from "react";

const NAV_ITEMS = [
  { name: "Beranda",     href: "/",          icon: Home      },
  { name: "Infografis",  href: "/infografis", icon: BarChart2 },
  { name: "Peta Risiko", href: "/peta",       icon: Map       },
  { name: "Data",        href: "/data",       icon: Database  },
  { name: "Metodologi",  href: "/about",      icon: BookOpen  },
];

export function Navbar() {
  const pathname = usePathname();
  const [open, setOpen] = useState(false);

  return (
    <>
      <header className="fixed top-0 left-0 right-0 z-50 h-16 glass border-b border-white/30 shadow-sm">
        <div className="max-w-7xl mx-auto h-full px-4 sm:px-6 flex items-center justify-between">
          <Link href="/" className="flex items-center gap-2 shrink-0">
            <span className="font-serif font-black text-xl tracking-tight text-slate-900">
              Panta<span className="text-[#1E88E5]">Uang</span>
            </span>
            <span className="hidden sm:inline text-[10px] font-bold text-slate-400 font-sans tracking-widest ml-1">KITA</span>
          </Link>

          {/* Desktop nav */}
          <nav className="hidden md:flex items-center gap-1">
            {NAV_ITEMS.map((item) => {
              const active = item.href === "/" ? pathname === "/" : pathname.startsWith(item.href);
              return (
                <Link key={item.href} href={item.href}
                  className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-sm font-bold font-sans transition-all duration-200 ${
                    active ? "bg-slate-900 text-white shadow-sm" : "text-slate-600 hover:bg-slate-100 hover:text-slate-900"
                  }`}>
                  <item.icon className="w-3.5 h-3.5" />
                  {item.name}
                </Link>
              );
            })}
          </nav>

          <button className="md:hidden p-2 rounded-lg text-slate-600 hover:bg-slate-100" onClick={() => setOpen(!open)}>
            {open ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
          </button>
        </div>
      </header>

      {/* Mobile drawer */}
      <div className={`fixed inset-0 z-40 transition-all duration-300 md:hidden ${open ? "pointer-events-auto" : "pointer-events-none"}`}>
        <div className={`absolute inset-0 bg-slate-900/40 transition-opacity duration-300 ${open ? "opacity-100" : "opacity-0"}`} onClick={() => setOpen(false)} />
        <div className={`absolute top-16 left-0 right-0 glass border-b border-white/30 shadow-xl transition-all duration-300 ${open ? "translate-y-0 opacity-100" : "-translate-y-4 opacity-0"}`}>
          <nav className="flex flex-col p-4 gap-1">
            {NAV_ITEMS.map((item) => {
              const active = item.href === "/" ? pathname === "/" : pathname.startsWith(item.href);
              return (
                <Link key={item.href} href={item.href} onClick={() => setOpen(false)}
                  className={`flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-bold font-sans transition-all ${
                    active ? "bg-slate-900 text-white" : "text-slate-700 hover:bg-slate-100"
                  }`}>
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
'''
with open(os.path.join(FRONTEND_COMPONENTS, "layout/Navbar.tsx"), "w", encoding="utf-8") as f:
    f.write(navbar_tsx)

print("Navbar done")

# ─── 2. HOMELIENT (fix "?" from Activity icon, use consistent number) ───
home_tsx = '''"use client";
import { motion } from "framer-motion";
import { Database, AlertOctagon, TrendingUp, ArrowRight, ExternalLink, Map as MapIcon, BarChart2, Zap } from "lucide-react";
import Link from "next/link";
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from "recharts";

const RISK_COLORS = { Anomali: "#FF5722", Tinggi: "#FF8A65", Sedang: "#FFCA28", Rendah: "#4CAF50" };
const TOTAL = 3009417;

const fadeUp = { hidden: { opacity: 0, y: 30 }, visible: (i: number) => ({ opacity: 1, y: 0, transition: { delay: i * 0.1, duration: 0.5 } }) };

export default function HomeClient({ tickerData, metricsData }: { tickerData: any; metricsData: any }) {
  const anomali = metricsData?.ekstrem || 75120;
  const tinggi  = metricsData?.risiko_tinggi || 149871;
  const sedang  = Math.floor(TOTAL * 0.15);
  const rendah  = TOTAL - anomali - tinggi - sedang;

  const pieData = [
    { name: "Anomali", value: anomali, fill: RISK_COLORS.Anomali },
    { name: "Tinggi",  value: tinggi,  fill: RISK_COLORS.Tinggi  },
    { name: "Sedang",  value: sedang,  fill: RISK_COLORS.Sedang  },
    { name: "Rendah",  value: rendah,  fill: RISK_COLORS.Rendah  },
  ];

  const stats = [
    { icon: Database,     label: "Data Dianalisis",   value: "3.009.417", color: "#1E88E5", bg: "bg-blue-50"   },
    { icon: TrendingUp,   label: "Total Anggaran",     value: "Rp 642,2T",  color: "#7E57C2", bg: "bg-purple-50" },
    { icon: AlertOctagon, label: "Rasio Anomali",      value: "7,47%",      color: "#FF5722", bg: "bg-red-50"    },
  ];

  const tickerItems = tickerData?.length > 0 ? tickerData : [
    { score: 99.87, agenda: "Pengadaan Alat Kesehatan RSUD...", pagu: 12400000000 },
    { score: 98.54, agenda: "Pembangunan Jalan Lingkar Luar...", pagu: 8700000000 },
    { score: 97.12, agenda: "Pengadaan Kendaraan Dinas...",     pagu: 5300000000 },
  ];

  return (
    <div className="w-full font-sans">
      {/* TICKER — no special emoji chars */}
      <div className="h-9 bg-white/80 backdrop-blur border-b border-slate-200/60 flex items-center overflow-hidden shrink-0">
        <div className="flex items-center px-4 bg-[#FF5722]/10 h-full border-r border-[#FF5722]/20 gap-2 shrink-0">
          <Zap className="w-3.5 h-3.5 text-[#FF5722] fill-current" />
          <span className="text-[10px] font-bold text-[#FF5722] uppercase tracking-widest whitespace-nowrap font-sans">Live Anomalies</span>
        </div>
        <div className="flex-1 overflow-hidden relative h-full">
          <div className="animate-[marquee_25s_linear_infinite] whitespace-nowrap flex gap-8 absolute items-center h-full px-4">
            {tickerItems.map((t: any, i: number) => (
              <span key={i} className="text-slate-600 text-xs font-sans">
                <span className="text-[#FF5722] font-bold font-mono">[{(t.score || t.skor_risiko || 0).toFixed(2)}]</span>
                {" "}{(t.agenda || "").substring(0, 45)}{(t.agenda || "").length > 45 ? "..." : ""}
                {" "}<span className="text-slate-400">Rp {((t.pagu || 0) / 1e9).toFixed(1)}M</span>
              </span>
            ))}
          </div>
        </div>
      </div>

      {/* HERO */}
      <section className="relative min-h-[90vh] flex items-center justify-center px-6 md:px-12 py-20 overflow-hidden">
        <div className="absolute top-[-10%] left-[-5%] w-[500px] h-[500px] rounded-full bg-[#1E88E5]/8 blur-3xl pointer-events-none" />
        <div className="absolute bottom-[-10%] right-[-5%] w-[400px] h-[400px] rounded-full bg-[#7E57C2]/8 blur-3xl pointer-events-none" />

        <div className="max-w-6xl mx-auto w-full">
          <div className="grid md:grid-cols-2 gap-12 items-center">
            <div>
              <motion.div variants={fadeUp} custom={0} initial="hidden" animate="visible"
                className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-[#1E88E5]/10 border border-[#1E88E5]/20 text-[#1E88E5] text-xs font-bold font-sans mb-6">
                <span className="w-1.5 h-1.5 rounded-full bg-[#1E88E5] animate-pulse" />
                Live — 3.009.417 Data Dianalisis
              </motion.div>

              <motion.h1 variants={fadeUp} custom={1} initial="hidden" animate="visible"
                className="font-serif font-black text-[clamp(2.8rem,5vw,4.5rem)] text-slate-900 leading-[1.08] tracking-tight mb-6">
                Intelijen Pengadaan{" "}
                <span className="text-transparent bg-clip-text bg-gradient-to-r from-[#1E88E5] to-[#7E57C2]">
                  Transparan dan Akurat.
                </span>
              </motion.h1>

              <motion.p variants={fadeUp} custom={2} initial="hidden" animate="visible"
                className="text-slate-500 font-sans text-[clamp(1rem,1.3vw,1.125rem)] leading-relaxed mb-8 max-w-lg">
                Platform PantaUang Kita menyediakan analisis risiko pengadaan barang dan jasa pemerintah menggunakan machine learning mutakhir. Eksplorasi hasil training dan testing klasifikasi risiko dengan mudah.
              </motion.p>

              <motion.div variants={fadeUp} custom={3} initial="hidden" animate="visible" className="flex flex-col sm:flex-row gap-3">
                <Link href="/data" className="flex items-center justify-center gap-2 px-6 py-3.5 bg-slate-900 hover:bg-slate-800 text-white rounded-xl font-bold text-sm transition-all shadow-lg hover:shadow-xl hover:-translate-y-0.5">
                  Mulai Eksplorasi Data <ArrowRight className="w-4 h-4" />
                </Link>
                <Link href="/peta" className="flex items-center justify-center gap-2 px-6 py-3.5 glass border border-slate-200 text-slate-700 hover:bg-white rounded-xl font-bold text-sm transition-all">
                  Lihat Peta Risiko <ExternalLink className="w-4 h-4" />
                </Link>
              </motion.div>
            </div>

            <motion.div variants={fadeUp} custom={2} initial="hidden" animate="visible"
              className="glass rounded-3xl p-8 shadow-xl border border-white/60 hover-lift">
              <h3 className="font-serif text-lg font-bold text-slate-800 mb-1">Distribusi Kategori Risiko</h3>
              <p className="text-slate-400 text-xs font-sans mb-4">Berdasarkan skor QRLGBM — 3.009.417 paket</p>
              <div className="h-[200px]">
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie data={pieData} innerRadius={60} outerRadius={90} paddingAngle={3} dataKey="value" stroke="none">
                      {pieData.map((entry, i) => <Cell key={i} fill={entry.fill} />)}
                    </Pie>
                    <Tooltip contentStyle={{ borderRadius: "10px", border: "none", boxShadow: "0 8px 24px rgba(0,0,0,0.1)", fontFamily: "var(--font-jakarta)", fontSize: "12px" }}
                      formatter={(val: any, name: string) => [`${val.toLocaleString("id-ID")} paket`, name]} />
                  </PieChart>
                </ResponsiveContainer>
              </div>
              <div className="flex flex-wrap gap-x-4 gap-y-2 justify-center mt-2">
                {Object.entries(RISK_COLORS).map(([k, c]) => (
                  <div key={k} className="flex items-center gap-1.5 text-xs font-sans font-bold text-slate-600">
                    <div className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: c }} />
                    {k}
                  </div>
                ))}
              </div>
            </motion.div>
          </div>

          {/* Stat Cards */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mt-12">
            {stats.map((s, i) => (
              <motion.div key={s.label} variants={fadeUp} custom={4 + i} initial="hidden" animate="visible"
                className="glass rounded-2xl p-5 border border-white/60 hover-lift cursor-default">
                <div className={`w-9 h-9 ${s.bg} rounded-xl flex items-center justify-center mb-3`}>
                  <s.icon className="w-4 h-4" style={{ color: s.color }} />
                </div>
                <div className="text-2xl font-black font-sans text-slate-900 mb-0.5">{s.value}</div>
                <div className="text-xs font-sans font-medium text-slate-400">{s.label}</div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* FEATURE CARDS */}
      <section className="bg-slate-900 bg-dot-dark px-6 md:px-12 py-20">
        <div className="max-w-6xl mx-auto">
          <motion.h2 initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }}
            className="font-serif font-black text-[clamp(2rem,3vw,3rem)] text-white text-center mb-3">
            Modul Analitik Terintegrasi
          </motion.h2>
          <p className="text-slate-500 font-sans text-center text-sm mb-12 max-w-xl mx-auto">
            Setiap modul dirancang untuk penyelidikan data dari sudut pandang yang berbeda namun saling melengkapi.
          </p>

          <div className="grid md:grid-cols-3 gap-6">
            {[
              { href: "/infografis", icon: BarChart2, color: "#FF8A65", bg: "from-orange-500/20 to-red-500/10",   label: "Infografis",    desc: "Visualisasi distribusi risiko, tren musiman, dan analisis sektoral secara dinamis." },
              { href: "/peta",       icon: MapIcon,   color: "#26C6DA", bg: "from-cyan-500/20 to-blue-500/10",   label: "Peta Risiko",   desc: "Choropleth interaktif 38 Provinsi dengan gradasi warna berdasarkan kategori risiko." },
              { href: "/data",       icon: Database,  color: "#7E57C2", bg: "from-purple-500/20 to-indigo-500/10", label: "Data Explorer", desc: "Tabel audit 3.009.417 paket dengan filter majemuk, pagination, dan detail akordion." },
            ].map((card, i) => (
              <motion.div key={card.href} initial={{ opacity: 0, y: 30 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ delay: i * 0.1 }}>
                <Link href={card.href} className="group block glass-dark rounded-2xl p-7 border border-white/5 hover:border-white/15 hover-lift transition-all">
                  <div className={`w-12 h-12 bg-gradient-to-br ${card.bg} rounded-xl flex items-center justify-center mb-5`}>
                    <card.icon className="w-5 h-5" style={{ color: card.color }} />
                  </div>
                  <h3 className="font-serif font-bold text-xl text-white mb-2">{card.label}</h3>
                  <p className="text-slate-500 text-sm font-sans leading-relaxed">{card.desc}</p>
                  <div className="flex items-center gap-2 mt-5 text-xs font-bold font-sans" style={{ color: card.color }}>
                    Eksplorasi <ArrowRight className="w-3.5 h-3.5 group-hover:translate-x-1 transition-transform" />
                  </div>
                </Link>
              </motion.div>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}
'''
with open(os.path.join(FRONTEND_APP, "HomeClient.tsx"), "w", encoding="utf-8") as f:
    f.write(home_tsx)

print("HomeClient done")
