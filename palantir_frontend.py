import os
import shutil

frontend_app_dir = r"D:\satdat 2026\sec\pantauang-enterprise\frontend\src\app"
frontend_components_dir = r"D:\satdat 2026\sec\pantauang-enterprise\frontend\src\components"

# 1. Delete old directories
for dirname in ["dashboard", "risk-map", "analytics", "anomalies", "procurement", "ml"]:
    path = os.path.join(frontend_app_dir, dirname)
    if os.path.exists(path):
        shutil.rmtree(path)

# 2. Re-create base dirs
for dirname in ["infografis", "peta", "data", "about"]:
    os.makedirs(os.path.join(frontend_app_dir, dirname), exist_ok=True)

# 3. Write layout.tsx (Global Palantir Sidebar Layout)
with open(os.path.join(frontend_app_dir, "layout.tsx"), "w") as f:
    f.write('''import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { Sidebar } from "@/components/layout/Sidebar";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "PantaUang Kita | Intelligence Dashboard",
  description: "Government Intelligence Dashboard for public procurement anomaly detection.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="id" className="dark">
      <body className={`${inter.className} bg-slate-950 text-slate-200 overflow-hidden`}>
        <div className="flex h-screen w-full relative">
          <Sidebar />
          <main className="flex-1 ml-20 md:ml-64 relative overflow-hidden flex flex-col h-full bg-[#0a0f18]">
            {children}
          </main>
        </div>
      </body>
    </html>
  );
}
''')

# 4. Write new Sidebar (components/layout/Sidebar.tsx)
os.makedirs(os.path.join(frontend_components_dir, "layout"), exist_ok=True)
with open(os.path.join(frontend_components_dir, "layout/Sidebar.tsx"), "w") as f:
    f.write('''"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { Home, PieChart, Map, Database, FileText } from "lucide-react";

export function Sidebar() {
  const pathname = usePathname();
  
  const menuItems = [
    { name: "Home", href: "/", icon: Home },
    { name: "Infografis", href: "/infografis", icon: PieChart },
    { name: "Peta", href: "/peta", icon: Map },
    { name: "Data", href: "/data", icon: Database },
    { name: "About", href: "/about", icon: FileText },
  ];

  return (
    <aside className="w-20 md:w-64 h-screen bg-[#070b14] border-r border-slate-800 flex flex-col fixed left-0 top-0 z-50">
      <div className="h-20 flex items-center justify-center md:justify-start md:px-8 border-b border-slate-800">
        <span className="font-extrabold text-2xl tracking-tighter text-white hidden md:block">
          Panta<span className="text-[#0D5CBD]">Uang</span>
        </span>
        <span className="font-extrabold text-2xl text-white md:hidden">P</span>
      </div>
      
      <nav className="flex-1 py-8 px-4">
        <ul className="space-y-3">
          {menuItems.map((item) => {
            const isActive = pathname === item.href;
            return (
              <li key={item.name}>
                <Link 
                  href={item.href} 
                  className={`flex items-center justify-center md:justify-start px-3 py-3 rounded-lg transition-all duration-200 font-medium text-sm group ${
                    isActive 
                    ? "bg-[#0D5CBD]/20 text-white border border-[#0D5CBD]/50 shadow-[0_0_15px_rgba(13,92,189,0.2)]" 
                    : "text-slate-400 hover:bg-slate-900 hover:text-slate-100"
                  }`}
                >
                  <item.icon className={`w-5 h-5 md:mr-3 ${isActive ? "text-[#52C7D8]" : "text-slate-500 group-hover:text-slate-300"}`} />
                  <span className="hidden md:block">{item.name}</span>
                </Link>
              </li>
            );
          })}
        </ul>
      </nav>
      
      <div className="p-4 border-t border-slate-800 text-center md:text-left text-xs font-mono text-slate-600">
        <span className="hidden md:inline">SYSTEM.ONLINE //</span><br className="hidden md:block"/>v2.0.0.941
      </div>
    </aside>
  );
}
''')

# 5. globals.css (Dark Slate Tech Theme)
with open(os.path.join(frontend_app_dir, "globals.css"), "w") as f:
    f.write('''@import "tailwindcss";

@layer base {
  :root {
    --background: #0a0f18; /* Palantir-esque deep slate */
    --foreground: #e2e8f0;
    
    /* Risk Levels */
    --risk-extreme: #ef4444; /* Crimson Red */
    --risk-high: #f97316; /* Orange */
    --risk-medium: #eab308; /* Yellow */
    --risk-low: #22c55e; /* Green */
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

.scrollbar-hide::-webkit-scrollbar {
    display: none;
}
.scrollbar-hide {
    -ms-overflow-style: none;
    scrollbar-width: none;
}

/* Palantir style borders and glows */
.tech-border {
    border: 1px solid rgba(148, 163, 184, 0.1);
    box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5);
    background: rgba(15, 23, 42, 0.6);
    backdrop-filter: blur(12px);
}
''')

# 6. Page 1: Home (Mission Control)
with open(os.path.join(frontend_app_dir, "page.tsx"), "w") as f:
    f.write('''"use client";
import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { Activity, Database, AlertOctagon, TrendingUp, Cpu, GitMerge } from "lucide-react";

export default function Home() {
  const [ticker, setTicker] = useState([]);
  const [metrics, setMetrics] = useState<any>(null);

  useEffect(() => {
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
    // Fetch Ticker
    fetch(`${apiUrl}/api/ticker`).then(res => res.json()).then(setTicker).catch(console.error);
    // Fetch Metrics
    fetch(`${apiUrl}/dashboard/metrics`).then(res => res.json()).then(setMetrics).catch(console.error);
  }, []);

  return (
    <div className="h-full overflow-auto flex flex-col">
      {/* 1. Ticker Banner */}
      <div className="h-10 bg-black/80 border-b border-red-900/50 flex items-center overflow-hidden">
        <div className="flex px-4 items-center bg-red-950/80 h-full border-r border-red-900/50 z-10 font-bold text-xs text-red-500 uppercase tracking-widest whitespace-nowrap shadow-[0_0_10px_rgba(239,68,68,0.2)]">
          <Activity className="w-4 h-4 mr-2 animate-pulse" /> Live Extreme Anomalies
        </div>
        <div className="flex-1 overflow-hidden relative">
          <div className="animate-[marquee_20s_linear_infinite] whitespace-nowrap flex gap-10 absolute">
            {ticker.length > 0 ? ticker.map((t: any, i) => (
              <span key={i} className="text-red-400 font-mono text-xs">
                [{t.score.toFixed(2)}] {t.agenda} - Rp {(t.pagu/1e9).toFixed(2)}M
              </span>
            )) : <span className="text-slate-600 font-mono text-xs">AWAITING TELEMETRY...</span>}
          </div>
        </div>
      </div>

      {/* 2. Hero Mission Control */}
      <div className="flex-1 p-8 md:p-12 relative flex flex-col justify-center">
        {/* Abstract Network Background */}
        <div className="absolute inset-0 z-0 opacity-20 pointer-events-none" 
             style={{ backgroundImage: 'radial-gradient(circle at 50% 50%, #0D5CBD 1px, transparent 1px)', backgroundSize: '40px 40px' }} />
        
        <div className="z-10 w-full max-w-7xl mx-auto">
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="mb-12">
            <h1 className="text-5xl md:text-7xl font-black tracking-tighter text-white mb-4 uppercase">
              Intelligence <span className="text-transparent bg-clip-text bg-gradient-to-r from-[#0D5CBD] to-[#52C7D8]">Node.</span>
            </h1>
            <p className="text-slate-400 font-mono text-sm md:text-base max-w-2xl border-l-2 border-[#0D5CBD] pl-4">
              PantaUang Kita Enterprise Architecture. Powered by Distil-IndoBERT and Quantile Regression LightGBM (QRLGBM) for public procurement anomaly detection.
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-16">
            <div className="tech-border p-6 rounded-lg border-l-4 border-l-[#0D5CBD]">
              <div className="flex items-center gap-3 mb-2 text-slate-400 font-mono text-xs uppercase"><Database className="w-4 h-4" /> Data Latih & Uji</div>
              <div className="text-4xl font-black font-mono text-white">{metrics?.total_data_exact?.toLocaleString() || "..."}</div>
            </div>
            <div className="tech-border p-6 rounded-lg border-l-4 border-l-[#52C7D8]">
              <div className="flex items-center gap-3 mb-2 text-slate-400 font-mono text-xs uppercase"><TrendingUp className="w-4 h-4" /> Total Budget Evaluated</div>
              <div className="text-4xl font-black font-mono text-white">Rp {metrics?.total_anggaran ? (metrics.total_anggaran / 1e12).toFixed(2) : "..."} T</div>
            </div>
            <div className="tech-border p-6 rounded-lg border-l-4 border-l-red-500 shadow-[0_0_20px_rgba(239,68,68,0.1)]">
              <div className="flex items-center gap-3 mb-2 text-red-400 font-mono text-xs uppercase"><AlertOctagon className="w-4 h-4" /> Extreme Anomaly Ratio</div>
              <div className="text-4xl font-black font-mono text-red-500">{metrics?.anomaly_ratio ? metrics.anomaly_ratio + "%" : "..."}</div>
            </div>
          </div>

          {/* Stepper */}
          <div className="mt-8">
            <h3 className="text-xs font-mono text-slate-500 mb-6 uppercase tracking-widest">Scientific Methodology Pipeline</h3>
            <div className="flex flex-col md:flex-row gap-4 items-center w-full">
              {[
                { icon: Database, label: "Data RUP Input" },
                { icon: Cpu, label: "Distil-IndoBERT + PCA" },
                { icon: GitMerge, label: "Integrasi Fitur" },
                { icon: Activity, label: "QRLGBM Modeling" },
                { icon: AlertOctagon, label: "Risk Categorization" }
              ].map((step, idx, arr) => (
                <div key={idx} className="flex items-center w-full md:w-auto flex-1">
                  <div className="tech-border px-4 py-3 rounded text-center flex-1 min-w-max flex flex-col items-center gap-2">
                    <step.icon className="w-5 h-5 text-slate-400" />
                    <span className="text-[10px] font-mono text-slate-300 uppercase">{step.label}</span>
                  </div>
                  {idx < arr.length - 1 && <div className="h-8 w-px md:h-px md:w-8 bg-slate-700 mx-2"></div>}
                </div>
              ))}
            </div>
          </div>

        </div>
      </div>
      <style dangerouslySetInnerHTML={{__html: `
        @keyframes marquee { 0% { transform: translateX(100vw); } 100% { transform: translateX(-100%); } }
      `}} />
    </div>
  );
}
''')

# 7. Page 5: About (Technical Trust)
with open(os.path.join(frontend_app_dir, "about/page.tsx"), "w") as f:
    f.write('''"use client";
import { useEffect, useState } from "react";
import { ShieldCheck, Server, Key, Target } from "lucide-react";

export default function AboutPage() {
  const [stats, setStats] = useState<any>(null);

  useEffect(() => {
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
    fetch(`${apiUrl}/api/methodology-stats`).then(res => res.json()).then(setStats).catch(console.error);
  }, []);

  return (
    <div className="h-full overflow-auto p-8 md:p-12">
      <div className="max-w-5xl mx-auto space-y-12">
        <header>
          <h1 className="text-3xl font-black uppercase tracking-tight mb-2">Technical Model Card</h1>
          <p className="text-slate-400 font-mono text-sm">Satria Data 2026 / 16_NOCturnal_SEC Documentation</p>
        </header>

        <section className="tech-border rounded-xl p-8">
          <div className="flex items-center gap-2 text-[#52C7D8] mb-6">
            <Target className="w-5 h-5" />
            <h2 className="text-lg font-bold uppercase tracking-wider">Model Evaluation Matrix</h2>
          </div>
          
          <div className="overflow-x-auto">
            <table className="w-full text-left font-mono text-sm">
              <thead className="text-xs uppercase bg-slate-900 text-slate-400">
                <tr>
                  <th className="px-6 py-4">Metric</th>
                  <th className="px-6 py-4">Train</th>
                  <th className="px-6 py-4">Test</th>
                  <th className="px-6 py-4">Notes</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800">
                {stats?.evaluation_matrix && Object.entries(stats.evaluation_matrix).map(([key, val]: any) => (
                  <tr key={key} className="hover:bg-slate-800/50 transition-colors">
                    <td className="px-6 py-4 font-bold text-white">{key}</td>
                    <td className="px-6 py-4 text-green-400">{val.train}</td>
                    <td className="px-6 py-4 text-green-400">{val.test}</td>
                    <td className="px-6 py-4 text-slate-500 text-xs">{val.note}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>

        <section className="tech-border rounded-xl p-8">
          <div className="flex items-center gap-2 text-[#8A63E8] mb-6">
            <Server className="w-5 h-5" />
            <h2 className="text-lg font-bold uppercase tracking-wider">Hyperparameter Transparency (TPE Optuna)</h2>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {stats?.optuna_hyperparameters && Object.entries(stats.optuna_hyperparameters).map(([model, params]: any) => (
              <div key={model} className="bg-slate-900/50 p-6 rounded-lg border border-slate-800">
                <h3 className="text-md font-bold mb-4 font-mono text-white">{model}</h3>
                <ul className="space-y-3 font-mono text-xs">
                  {Object.entries(params).map(([p, v]: any) => (
                    <li key={p} className="flex justify-between items-center border-b border-slate-800 pb-2">
                      <span className="text-slate-400">{p}</span>
                      <span className="text-[#0D5CBD] font-bold bg-blue-950 px-2 py-1 rounded">{v}</span>
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </section>
      </div>
    </div>
  );
}
''')

print("Palantir Layout, Home, and About pages built successfully!")
