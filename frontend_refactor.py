import os

frontend_src_dir = r"D:\satdat 2026\sec\pantauang-enterprise\frontend\src"

# 1. Update globals.css to include custom animations and styles
globals_css = os.path.join(frontend_src_dir, "app/globals.css")
with open(globals_css, "w") as f:
    f.write('''@import "tailwindcss";

@theme {
  --color-brand-blue: #0D5CBD;
  --color-brand-semantic: #F28A6A;
  --color-brand-integration: #52C7D8;
  --color-brand-ml: #8A63E8;
  --color-brand-insight: #FF7A3D;
}

@layer base {
  :root {
    --background: #FDFBF7; /* Sangat elegan, off-white ke arah krem super lembut */
    --foreground: #1D1D1F; /* Apple standard dark text */
  }
  
  html {
    scroll-behavior: smooth;
  }
  
  body {
    background-color: var(--background);
    color: var(--foreground);
    overflow-x: hidden;
  }
}

/* Custom Glassmorphism Utilities */
.glass-panel {
  background: rgba(255, 255, 255, 0.65);
  backdrop-filter: blur(24px);
  -webkit-backdrop-filter: blur(24px);
  border: 1px solid rgba(255, 255, 255, 0.4);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.04);
}

.glass-card {
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid rgba(255, 255, 255, 0.8);
  box-shadow: 0 10px 40px -10px rgba(0,0,0,0.08);
  transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}

.glass-card:hover {
  transform: translateY(-8px) scale(1.01);
  box-shadow: 0 20px 40px -15px rgba(0,0,0,0.15);
  border-color: rgba(13, 92, 189, 0.2);
}

/* Fluid Apple-like text gradient */
.text-gradient {
  background: linear-gradient(135deg, #1D1D1F 0%, #434344 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.text-gradient-brand {
  background: linear-gradient(135deg, #0D5CBD 0%, #8A63E8 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
''')

# 2. Update page.tsx (The massive scrolling landing page)
page_tsx = os.path.join(frontend_src_dir, "app/page.tsx")
with open(page_tsx, "w") as f:
    f.write('''"use client";
import Link from 'next/link';
import { motion, useScroll, useTransform } from 'framer-motion';
import { useRef } from 'react';
import { ArrowRight, Activity, ShieldAlert, Cpu, BarChart3, Database } from 'lucide-react';

export default function LandingPage() {
  const containerRef = useRef(null);
  const { scrollYProgress } = useScroll({ target: containerRef });
  
  // Parallax effects
  const heroY = useTransform(scrollYProgress, [0, 0.2], [0, 150]);
  const heroOpacity = useTransform(scrollYProgress, [0, 0.15], [1, 0]);

  return (
    <div ref={containerRef} className="relative min-h-screen selection:bg-blue-200">
      
      {/* Animated Subtle Ambient Background (Not Plain White) */}
      <div className="fixed inset-0 -z-10 overflow-hidden pointer-events-none">
        <div className="absolute top-[-20%] left-[-10%] w-[50vw] h-[50vw] rounded-full bg-gradient-to-tr from-[#eef2f3] to-[#8e9eab] opacity-30 blur-[120px] mix-blend-multiply animate-pulse" style={{ animationDuration: '8s' }}></div>
        <div className="absolute top-[20%] right-[-10%] w-[40vw] h-[40vw] rounded-full bg-gradient-to-tr from-[#52C7D8]/20 to-[#0D5CBD]/10 opacity-40 blur-[120px] mix-blend-multiply animate-pulse" style={{ animationDuration: '12s', animationDelay: '2s' }}></div>
        <div className="absolute bottom-[-10%] left-[20%] w-[60vw] h-[60vw] rounded-full bg-gradient-to-tr from-[#F28A6A]/10 to-[#FF7A3D]/10 opacity-40 blur-[120px] mix-blend-multiply animate-pulse" style={{ animationDuration: '10s', animationDelay: '4s' }}></div>
      </div>

      {/* Navbar Glass */}
      <nav className="fixed top-0 w-full z-50 glass-panel border-b-0 border-x-0 border-t-0 bg-white/40 transition-all duration-300">
        <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
          <span className="font-bold text-xl tracking-tight text-slate-800">PantaUang<span className="text-[#0D5CBD]">.</span></span>
          <div className="flex gap-4">
            <Link href="/dashboard" className="px-5 py-2 text-sm font-medium text-slate-800 hover:text-[#0D5CBD] transition-colors">Dasbor</Link>
            <Link href="/dashboard" className="px-5 py-2 text-sm font-medium bg-[#1D1D1F] hover:bg-black text-white rounded-full transition-all shadow-md hover:shadow-lg transform hover:-translate-y-0.5">Mulai Eksplorasi</Link>
          </div>
        </div>
      </nav>

      {/* 1. HERO SECTION */}
      <motion.section 
        style={{ y: heroY, opacity: heroOpacity }}
        className="relative pt-40 pb-32 px-6 flex flex-col items-center justify-center text-center min-h-[90vh]"
      >
        <motion.div 
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, ease: [0.16, 1, 0.3, 1] }}
          className="max-w-4xl"
        >
          <span className="inline-block py-1 px-3 rounded-full bg-blue-50 border border-blue-100 text-[#0D5CBD] text-sm font-semibold mb-6 tracking-wide uppercase">
            Platform Generasi Baru 2026
          </span>
          <h1 className="text-6xl md:text-8xl font-bold tracking-tighter leading-tight mb-8 text-gradient">
            Intelijen Pengadaan.<br/>Sangat Presisi.
          </h1>
          <p className="text-xl md:text-2xl font-medium text-slate-500 mb-12 max-w-2xl mx-auto leading-relaxed">
            Menyelami 3 Juta data lelang nasional menggunakan model AI Distil-IndoBERT. Mengendus potensi risiko hingga ke akar dengan estetika tanpa kompromi.
          </p>
          
          <div className="flex flex-col sm:flex-row gap-5 justify-center items-center">
            <Link href="/dashboard" className="group flex items-center gap-2 px-8 py-4 bg-[#1D1D1F] hover:bg-black text-white rounded-full font-semibold text-lg transition-all shadow-xl hover:shadow-2xl transform hover:scale-105">
              Masuk ke Dasbor
              <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
            </Link>
            <Link href="#features" className="px-8 py-4 bg-white/50 backdrop-blur-md border border-slate-200 hover:border-slate-300 hover:bg-white text-slate-700 rounded-full font-semibold text-lg transition-all shadow-sm hover:shadow-md">
              Pelajari Lebih Lanjut
            </Link>
          </div>
        </motion.div>
      </motion.section>

      {/* 2. STATS SHOWCASE */}
      <section className="py-24 px-6 relative z-10">
        <div className="max-w-7xl mx-auto">
          <motion.div 
            initial={{ opacity: 0, y: 40 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, margin: "-100px" }}
            transition={{ duration: 0.8 }}
            className="glass-panel rounded-3xl p-10 md:p-16 flex flex-col md:flex-row justify-between items-center gap-10"
          >
            <div className="text-center md:text-left">
              <h2 className="text-4xl md:text-5xl font-bold tracking-tight mb-2 text-gradient-brand">3.000.000+</h2>
              <p className="text-lg text-slate-500 font-medium">Baris Data Dianalisis</p>
            </div>
            <div className="w-px h-16 bg-slate-200 hidden md:block"></div>
            <div className="text-center md:text-left">
              <h2 className="text-4xl md:text-5xl font-bold tracking-tight mb-2 text-gradient-brand">&lt; 10 ms</h2>
              <p className="text-lg text-slate-500 font-medium">Waktu Respons Agregasi</p>
            </div>
            <div className="w-px h-16 bg-slate-200 hidden md:block"></div>
            <div className="text-center md:text-left">
              <h2 className="text-4xl md:text-5xl font-bold tracking-tight mb-2 text-gradient-brand">99.9%</h2>
              <p className="text-lg text-slate-500 font-medium">Uptime Serverless</p>
            </div>
          </motion.div>
        </div>
      </section>

      {/* 3. FEATURES SECTION */}
      <section id="features" className="py-32 px-6 relative z-10">
        <div className="max-w-7xl mx-auto">
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-20"
          >
            <h2 className="text-5xl font-bold tracking-tight mb-6">Kemampuan Luar Biasa.<br/>Dalam Balutan Kesederhanaan.</h2>
            <p className="text-xl text-slate-500 max-w-3xl mx-auto">Semua teknologi mutakhir disembunyikan di balik antarmuka yang sangat bersih dan intuitif, dirancang khusus untuk pengambil keputusan.</p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            <FeatureCard 
              icon={<ShieldAlert className="w-8 h-8 text-[#F28A6A]" />}
              title="Deteksi Risiko P90"
              desc="Model QRLGBM secara otomatis memprediksi batas kewajaran harga P90 dan mendeteksi anomali mark-up."
              delay={0.1}
            />
            <FeatureCard 
              icon={<Cpu className="w-8 h-8 text-[#8A63E8]" />}
              title="AI Semantic Analysis"
              desc="Distil-IndoBERT membaca dokumen pengadaan bagaikan manusia untuk memahami konteks dan risiko tersembunyi."
              delay={0.2}
            />
            <FeatureCard 
              icon={<Database className="w-8 h-8 text-[#0D5CBD]" />}
              title="TiDB HTAP Engine"
              desc="Mengakses jutaan baris data historis secara instan berkat infrastruktur TiDB Serverless."
              delay={0.3}
            />
          </div>
        </div>
      </section>

      {/* 4. LARGE PREVIEW SECTION */}
      <section className="py-24 px-6 relative z-10 overflow-hidden">
        <div className="max-w-7xl mx-auto">
          <motion.div 
            initial={{ opacity: 0, scale: 0.95 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
            transition={{ duration: 1, ease: "easeOut" }}
            className="relative rounded-[2.5rem] overflow-hidden glass-card p-4 md:p-8 border border-slate-200/50"
          >
            {/* Mockup Window */}
            <div className="w-full rounded-2xl bg-white/80 border border-slate-100 shadow-2xl overflow-hidden aspect-[16/9] md:aspect-[21/9] flex flex-col">
              <div className="h-10 bg-slate-100/50 border-b border-slate-200 flex items-center px-4 gap-2">
                <div className="w-3 h-3 rounded-full bg-red-400"></div>
                <div className="w-3 h-3 rounded-full bg-amber-400"></div>
                <div className="w-3 h-3 rounded-full bg-green-400"></div>
              </div>
              <div className="flex-1 p-8 flex items-center justify-center bg-slate-50/50">
                <BarChart3 className="w-32 h-32 text-slate-300 opacity-50" />
              </div>
            </div>
          </motion.div>
        </div>
      </section>

      {/* 5. CTA SECTION */}
      <section className="py-40 px-6 relative z-10">
        <motion.div 
          initial={{ opacity: 0, y: 50 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8 }}
          className="max-w-4xl mx-auto text-center"
        >
          <h2 className="text-5xl md:text-7xl font-bold tracking-tight mb-8">Siap Mengambil Kendali?</h2>
          <Link href="/dashboard" className="inline-block px-12 py-5 bg-[#1D1D1F] hover:bg-black text-white rounded-full font-bold text-xl transition-all shadow-2xl hover:shadow-[0_20px_50px_rgba(0,0,0,0.3)] transform hover:scale-105">
            Buka PantaUang Dashboard
          </Link>
        </motion.div>
      </section>

    </div>
  );
}

function FeatureCard({ icon, title, desc, delay }: { icon: React.ReactNode, title: string, desc: string, delay: number }) {
  return (
    <motion.div 
      initial={{ opacity: 0, y: 30 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "-50px" }}
      transition={{ duration: 0.6, delay }}
      className="glass-card p-10 rounded-3xl flex flex-col h-full"
    >
      <div className="w-16 h-16 rounded-2xl bg-white border border-slate-100 flex items-center justify-center mb-6 shadow-sm">
        {icon}
      </div>
      <h3 className="text-2xl font-bold mb-4 text-slate-800">{title}</h3>
      <p className="text-slate-500 font-medium leading-relaxed">{desc}</p>
    </motion.div>
  );
}
''')

# 3. Sidebar.tsx (Dashboard UI Refactor)
sidebar_tsx = os.path.join(frontend_src_dir, "components/layout/Sidebar.tsx")
with open(sidebar_tsx, "w") as f:
    f.write('''"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { LayoutDashboard, Database, Map, BarChart2, AlertTriangle, Cpu, FileText, Settings, LogOut } from "lucide-react";

export function Sidebar() {
  const pathname = usePathname();
  
  const menuItems = [
    { name: "Dashboard", href: "/dashboard", icon: LayoutDashboard },
    { name: "Data Pengadaan", href: "/procurement", icon: Database },
    { name: "Peta Risiko", href: "/risk-map", icon: Map },
    { name: "Analitik", href: "/analytics", icon: BarChart2 },
    { name: "Anomali", href: "/anomalies", icon: AlertTriangle },
    { name: "Model AI", href: "/ml", icon: Cpu },
  ];

  return (
    <aside className="w-72 h-screen p-4 flex flex-col fixed left-0 top-0 z-40">
      <div className="w-full h-full glass-panel rounded-3xl overflow-hidden flex flex-col shadow-lg">
        
        <div className="h-24 flex flex-col justify-center px-8 border-b border-white/20">
          <span className="font-extrabold text-2xl tracking-tight text-slate-800">
            PantaUang<span className="text-[#0D5CBD]">.</span>
          </span>
          <span className="text-xs font-semibold text-slate-500 uppercase tracking-widest mt-1">Enterprise</span>
        </div>
        
        <nav className="flex-1 py-6 overflow-y-auto px-4 custom-scrollbar">
          <ul className="space-y-2">
            {menuItems.map((item) => {
              const isActive = pathname === item.href;
              return (
                <li key={item.name}>
                  <Link 
                    href={item.href} 
                    className={`flex items-center px-4 py-3.5 rounded-2xl transition-all duration-300 font-medium text-sm group ${
                      isActive 
                      ? "bg-white/80 text-[#0D5CBD] shadow-sm border border-white" 
                      : "text-slate-600 hover:bg-white/40 hover:text-slate-900"
                    }`}
                  >
                    <item.icon className={`w-5 h-5 mr-3 transition-colors ${isActive ? "text-[#0D5CBD]" : "text-slate-400 group-hover:text-slate-700"}`} />
                    {item.name}
                  </Link>
                </li>
              );
            })}
          </ul>
        </nav>
        
        <div className="p-4 border-t border-white/20">
          <Link href="/" className="flex items-center justify-center w-full px-4 py-3 rounded-2xl bg-white/50 text-slate-600 font-medium text-sm hover:bg-white transition-all shadow-sm">
            <LogOut className="w-4 h-4 mr-2" /> Keluar
          </Link>
        </div>

      </div>
    </aside>
  );
}
''')

# 4. dashboard/layout.tsx Refactor to fit the new floating sidebar
dashboard_layout = os.path.join(frontend_src_dir, "app/dashboard/layout.tsx")
with open(dashboard_layout, "w") as f:
    f.write('''import { Sidebar } from "@/components/layout/Sidebar";

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex h-screen bg-[#FDFBF7] overflow-hidden relative">
      {/* Subtle background element for dashboard */}
      <div className="absolute top-0 right-0 w-[800px] h-[800px] bg-gradient-to-bl from-blue-100/40 to-transparent rounded-full blur-[100px] -z-10 pointer-events-none" />
      
      <Sidebar />
      
      <div className="flex-1 flex flex-col ml-72">
        <header className="h-24 flex items-end pb-4 px-10 z-10">
          <h2 className="text-3xl font-bold tracking-tight text-slate-800">Ringkasan Eksekutif</h2>
        </header>
        <main className="flex-1 overflow-auto p-10 pt-4 pb-24">
          {children}
        </main>
      </div>
    </div>
  );
}
''')

# 5. Fix dashboard/page.tsx MetricCards to use framer-motion and glassmorphism
dashboard_page = os.path.join(frontend_src_dir, "app/dashboard/page.tsx")
with open(dashboard_page, "w") as f:
    f.write('''"use client";
import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { RiskDistributionChart, BudgetTrendChart } from "@/components/dashboard/RiskCharts";

export default function DashboardHome() {
  const [metrics, setMetrics] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
    fetch(`${apiUrl}/dashboard/metrics`)
      .then(res => res.json())
      .then(data => {
        setMetrics(data);
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        setLoading(false);
      });
  }, []);

  if (loading) return (
    <div className="h-full flex items-center justify-center">
      <div className="animate-pulse flex flex-col items-center">
        <div className="w-12 h-12 rounded-full border-4 border-t-[#0D5CBD] border-slate-200 animate-spin mb-4"></div>
        <p className="text-slate-500 font-medium">Sinkronisasi Jutaan Data TiDB...</p>
      </div>
    </div>
  );

  return (
    <motion.div 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
      className="space-y-8"
    >
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6">
        <MetricCard delay={0.1} title="Total Anggaran" value={metrics?.total_anggaran ? `Rp ${(metrics.total_anggaran / 1e12).toFixed(2)} Triliun` : "-"} color="bg-[#0D5CBD]" />
        <MetricCard delay={0.2} title="Total Paket" value={metrics?.total_paket?.toLocaleString() || "-"} color="bg-[#52C7D8]" />
        <MetricCard delay={0.3} title="Risiko Tinggi" value={metrics?.risiko_tinggi?.toLocaleString() || "-"} color="bg-[#F28A6A]" />
        <MetricCard delay={0.4} title="Potensi Anomali" value={metrics?.estimasi_potensi_anomali ? `Rp ${(metrics.estimasi_potensi_anomali / 1e9).toFixed(2)} Miliar` : "-"} color="bg-[#FF7A3D]" />
      </div>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <motion.div 
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.6, delay: 0.5 }}
          className="glass-card p-8 rounded-3xl h-[450px] flex items-center justify-center relative overflow-hidden group"
        >
          <div className="absolute top-0 right-0 w-32 h-32 bg-orange-100/50 rounded-full blur-[40px] group-hover:scale-150 transition-transform duration-700"></div>
          <RiskDistributionChart data={metrics?.risk_distribution || []} />
        </motion.div>
        
        <motion.div 
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.6, delay: 0.6 }}
          className="glass-card p-8 rounded-3xl h-[450px] flex items-center justify-center relative overflow-hidden group"
        >
          <div className="absolute top-0 right-0 w-32 h-32 bg-purple-100/50 rounded-full blur-[40px] group-hover:scale-150 transition-transform duration-700"></div>
          <BudgetTrendChart data={metrics?.budget_trend || {months: [], pagu: [], p90: []}} />
        </motion.div>
      </div>
    </motion.div>
  );
}

function MetricCard({ title, value, color, delay }: { title: string, value: string, color: string, delay: number }) {
  return (
    <motion.div 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay }}
      className="glass-card p-6 rounded-3xl flex flex-col justify-between min-h-[160px] relative overflow-hidden group cursor-default"
    >
      <div className={`absolute -right-4 -top-4 w-24 h-24 rounded-full ${color} opacity-[0.03] group-hover:opacity-10 group-hover:scale-150 transition-all duration-700`}></div>
      <p className="text-sm font-semibold text-slate-500 uppercase tracking-wide">{title}</p>
      <h3 className="text-3xl lg:text-4xl font-bold tracking-tight text-slate-800 mt-2">{value}</h3>
    </motion.div>
  );
}
''')

print("UI/UX Refactor Applied!")
