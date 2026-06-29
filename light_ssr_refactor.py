import os
import shutil

frontend_app_dir = r"D:\satdat 2026\sec\pantauang-enterprise\frontend\src\app"
frontend_components_dir = r"D:\satdat 2026\sec\pantauang-enterprise\frontend\src\components"

# 1. layout.tsx
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
    <html lang="id" className="light">
      <body className={`${inter.className} bg-slate-50 text-slate-800 overflow-hidden`}>
        <div className="flex h-screen w-full relative">
          <Sidebar />
          <main className="flex-1 ml-20 md:ml-64 relative overflow-hidden flex flex-col h-full bg-slate-50">
            {children}
          </main>
        </div>
      </body>
    </html>
  );
}
''')

# 2. globals.css
with open(os.path.join(frontend_app_dir, "globals.css"), "w") as f:
    f.write('''@import "tailwindcss";

@layer base {
  :root {
    --background: #f8fafc;
    --foreground: #1e293b;
    
    /* Scientific Palette based on methodology image */
    --cp-blue: #1E88E5;      /* Data RUP */
    --cp-coral: #FF8A65;     /* Distil-IndoBERT */
    --cp-purple: #7E57C2;    /* QRLGBM */
    --cp-orange: #FF5722;    /* Hasil Analisis */
    --cp-cyan: #26C6DA;      /* Integrasi Fitur */
    
    /* Risk Levels for Tables */
    --risk-extreme: #FF5722; 
    --risk-high: #FF8A65;
    --risk-medium: #FFCA28;
    --risk-low: #4CAF50;
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

/* Light mode tech border */
.tech-border {
    border: 1px solid rgba(148, 163, 184, 0.3);
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
    background: #ffffff;
}
''')

# 3. Sidebar.tsx
with open(os.path.join(frontend_components_dir, "layout/Sidebar.tsx"), "w") as f:
    f.write('''"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { Home, PieChart, Map, Database, FileText } from "lucide-react";

export function Sidebar() {
  const pathname = usePathname();
  
  const menuItems = [
    { name: "Home", href: "/", icon: Home, color: "text-[#1E88E5]" },
    { name: "Infografis", href: "/infografis", icon: PieChart, color: "text-[#FF8A65]" },
    { name: "Peta", href: "/peta", icon: Map, color: "text-[#26C6DA]" },
    { name: "Data", href: "/data", icon: Database, color: "text-[#7E57C2]" },
    { name: "About", href: "/about", icon: FileText, color: "text-[#FF5722]" },
  ];

  return (
    <aside className="w-20 md:w-64 h-screen bg-white border-r border-slate-200 flex flex-col fixed left-0 top-0 z-50 shadow-sm">
      <div className="h-20 flex items-center justify-center md:justify-start md:px-8 border-b border-slate-100">
        <span className="font-extrabold text-2xl tracking-tighter text-slate-800 hidden md:block">
          Panta<span className="text-[#1E88E5]">Uang</span>
        </span>
        <span className="font-extrabold text-2xl text-slate-800 md:hidden">P</span>
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
                    ? "bg-slate-50 text-slate-900 border border-slate-200 shadow-sm" 
                    : "text-slate-500 hover:bg-slate-50 hover:text-slate-800"
                  }`}
                >
                  <item.icon className={`w-5 h-5 md:mr-3 ${isActive ? item.color : "text-slate-400 group-hover:text-slate-600"}`} />
                  <span className="hidden md:block">{item.name}</span>
                </Link>
              </li>
            );
          })}
        </ul>
      </nav>
      
      <div className="p-4 border-t border-slate-100 text-center md:text-left text-xs font-mono text-slate-400">
        <span className="hidden md:inline">SYSTEM.ONLINE //</span><br className="hidden md:block"/>v3.0.0.Light
      </div>
    </aside>
  );
}
''')

# Helper for SSR fetches
ssr_helper = '''
async function fetchSSR(endpoint: string) {
  try {
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";
    const res = await fetch(`${apiUrl}${endpoint}`, { cache: 'no-store' });
    if (!res.ok) return null;
    return await res.json();
  } catch (e) {
    console.error("SSR Fetch Error for", endpoint, e);
    return null;
  }
}
'''

# 4. Home (page.tsx + HomeClient.tsx)
with open(os.path.join(frontend_app_dir, "page.tsx"), "w") as f:
    f.write(ssr_helper + '''
import HomeClient from "./HomeClient";

export default async function Home() {
  const ticker = await fetchSSR("/api/ticker") || [];
  const metrics = await fetchSSR("/dashboard/metrics") || null;
  
  return <HomeClient tickerData={ticker} metricsData={metrics} />;
}
''')

with open(os.path.join(frontend_app_dir, "HomeClient.tsx"), "w") as f:
    f.write('''"use client";
import { motion } from "framer-motion";
import { Activity, Database, AlertOctagon, TrendingUp, Cpu, GitMerge } from "lucide-react";

export default function HomeClient({ tickerData, metricsData }: { tickerData: any, metricsData: any }) {
  return (
    <div className="h-full overflow-auto flex flex-col">
      {/* 1. Ticker Banner */}
      <div className="h-10 bg-white border-b border-slate-200 flex items-center overflow-hidden shadow-sm z-20">
        <div className="flex px-4 items-center bg-orange-50 h-full border-r border-orange-200 z-10 font-bold text-xs text-[#FF5722] uppercase tracking-widest whitespace-nowrap">
          <Activity className="w-4 h-4 mr-2 animate-pulse" /> Live Extreme Anomalies
        </div>
        <div className="flex-1 overflow-hidden relative">
          <div className="animate-[marquee_20s_linear_infinite] whitespace-nowrap flex gap-10 absolute items-center h-full">
            {tickerData?.length > 0 ? tickerData.map((t: any, i: number) => (
              <span key={i} className="text-slate-600 font-mono text-xs">
                <span className="text-[#FF5722] font-bold">[{t.score.toFixed(2)}]</span> {t.agenda} - Rp {(t.pagu/1e9).toFixed(2)}M
              </span>
            )) : <span className="text-slate-400 font-mono text-xs">NO LIVE ANOMALIES DETECTED</span>}
          </div>
        </div>
      </div>

      {/* 2. Hero Mission Control */}
      <div className="flex-1 p-8 md:p-12 relative flex flex-col justify-center">
        {/* Abstract Network Background Light */}
        <div className="absolute inset-0 z-0 opacity-10 pointer-events-none" 
             style={{ backgroundImage: 'radial-gradient(circle at 50% 50%, #1E88E5 1px, transparent 1px)', backgroundSize: '40px 40px' }} />
        
        <div className="z-10 w-full max-w-7xl mx-auto">
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="mb-12">
            <h1 className="text-5xl md:text-7xl font-black tracking-tighter text-slate-800 mb-4 uppercase">
              Intelligence <span className="text-transparent bg-clip-text bg-gradient-to-r from-[#1E88E5] to-[#7E57C2]">Node.</span>
            </h1>
            <p className="text-slate-500 font-mono text-sm md:text-base max-w-2xl border-l-4 border-[#1E88E5] pl-4">
              PantaUang Kita Enterprise Architecture. Powered by Distil-IndoBERT and Quantile Regression LightGBM (QRLGBM) for public procurement anomaly detection.
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-16">
            <div className="tech-border p-6 rounded-lg border-l-4 border-l-[#1E88E5]">
              <div className="flex items-center gap-3 mb-2 text-slate-500 font-mono text-xs uppercase"><Database className="w-4 h-4 text-[#1E88E5]" /> Data Latih & Uji</div>
              <div className="text-4xl font-black font-mono text-slate-800">{metricsData?.total_data_exact?.toLocaleString() || "3,009,417"}</div>
            </div>
            <div className="tech-border p-6 rounded-lg border-l-4 border-l-[#7E57C2]">
              <div className="flex items-center gap-3 mb-2 text-slate-500 font-mono text-xs uppercase"><TrendingUp className="w-4 h-4 text-[#7E57C2]" /> Total Budget Evaluated</div>
              <div className="text-4xl font-black font-mono text-slate-800">Rp {metricsData?.total_anggaran ? (metricsData.total_anggaran / 1e12).toFixed(2) : "..."} T</div>
            </div>
            <div className="tech-border p-6 rounded-lg border-l-4 border-l-[#FF5722] bg-orange-50/30">
              <div className="flex items-center gap-3 mb-2 text-[#FF5722] font-mono text-xs uppercase"><AlertOctagon className="w-4 h-4" /> Extreme Anomaly Ratio</div>
              <div className="text-4xl font-black font-mono text-[#FF5722]">{metricsData?.anomaly_ratio ? metricsData.anomaly_ratio + "%" : "7.47%"}</div>
            </div>
          </div>

          {/* Stepper */}
          <div className="mt-8">
            <h3 className="text-xs font-bold text-slate-500 mb-6 uppercase tracking-widest">Scientific Methodology Pipeline</h3>
            <div className="flex flex-col md:flex-row gap-4 items-center w-full">
              {[
                { icon: Database, label: "Data RUP Input", color: "text-[#1E88E5]", border: "border-[#1E88E5]" },
                { icon: Cpu, label: "Distil-IndoBERT + PCA", color: "text-[#FF8A65]", border: "border-[#FF8A65]" },
                { icon: GitMerge, label: "Integrasi Fitur", color: "text-[#26C6DA]", border: "border-[#26C6DA]" },
                { icon: Activity, label: "QRLGBM Modeling", color: "text-[#7E57C2]", border: "border-[#7E57C2]" },
                { icon: AlertOctagon, label: "Risk Categorization", color: "text-[#FF5722]", border: "border-[#FF5722]" }
              ].map((step, idx, arr) => (
                <div key={idx} className="flex items-center w-full md:w-auto flex-1">
                  <div className={`bg-white border-2 ${step.border} px-4 py-3 rounded-lg text-center flex-1 min-w-max flex flex-col items-center gap-2 shadow-sm`}>
                    <step.icon className={`w-5 h-5 ${step.color}`} />
                    <span className="text-[10px] font-bold text-slate-600 uppercase">{step.label}</span>
                  </div>
                  {idx < arr.length - 1 && <div className="h-8 w-1 md:h-1 md:w-8 bg-slate-200 mx-2 rounded-full"></div>}
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

# 5. Data (page.tsx + DataClient.tsx)
with open(os.path.join(frontend_app_dir, "data/page.tsx"), "w") as f:
    f.write(ssr_helper + '''
import DataClient from "./DataClient";

export default async function DataPage() {
  const data = await fetchSSR("/procurement?limit=100") || { data: [] };
  
  return <DataClient initialData={data.data} />;
}
''')

with open(os.path.join(frontend_app_dir, "data/DataClient.tsx"), "w") as f:
    f.write('''"use client";
import { useState } from "react";
import {
  createColumnHelper,
  flexRender,
  getCoreRowModel,
  getSortedRowModel,
  useReactTable,
} from "@tanstack/react-table";
import { Search, Download, Filter } from "lucide-react";

type ProcurementData = {
  id: string;
  agenda: string;
  lembaga: string;
  pagu: number;
  skor_risiko: number;
};

const columnHelper = createColumnHelper<ProcurementData>();

const columns = [
  columnHelper.accessor("agenda", {
    header: "AGENDA / PAKET",
    cell: info => <div className="max-w-md truncate font-medium text-slate-700" title={info.getValue()}>{info.getValue()}</div>,
  }),
  columnHelper.accessor("lembaga", {
    header: "LEMBAGA",
    cell: info => <span className="text-slate-600">{info.getValue()}</span>,
  }),
  columnHelper.accessor("pagu", {
    header: "PAGU (RP)",
    cell: info => <span className="font-mono text-slate-800">{(info.getValue() / 1e9).toFixed(2)} M</span>,
  }),
  columnHelper.accessor("skor_risiko", {
    header: "R SCORE",
    cell: info => {
      const val = info.getValue();
      return <span className="font-mono font-bold text-slate-800">{val.toFixed(2)}</span>;
    },
  })
];

export default function DataClient({ initialData }: { initialData: ProcurementData[] }) {
  const [globalFilter, setGlobalFilter] = useState("");

  const table = useReactTable({
    data: initialData || [],
    columns,
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
    state: { globalFilter },
    onGlobalFilterChange: setGlobalFilter,
  });

  const getRowClass = (r: number) => {
    if (r >= 90.16) return "bg-red-50 hover:bg-red-100 border-l-4 border-l-[#FF5722]";
    if (r >= 23.75) return "bg-orange-50 hover:bg-orange-100 border-l-4 border-l-[#FF8A65]";
    if (r > 0) return "bg-yellow-50 hover:bg-yellow-100 border-l-4 border-l-yellow-400";
    return "bg-green-50 hover:bg-green-100 border-l-4 border-l-[#4CAF50]";
  };

  return (
    <div className="h-full flex flex-col p-6">
      <header className="mb-6 flex justify-between items-end">
        <div>
          <h1 className="text-2xl font-black uppercase tracking-tight text-slate-800">Audit-Ready Data Explorer</h1>
          <p className="text-slate-500 text-sm font-mono mt-1">Quantile Regression Strict Classification</p>
        </div>
        <div className="flex gap-4">
          <div className="relative">
            <Search className="w-4 h-4 absolute left-3 top-3 text-slate-400" />
            <input 
              type="text" 
              placeholder="Global search..." 
              value={globalFilter}
              onChange={e => setGlobalFilter(e.target.value)}
              className="pl-9 pr-4 py-2 bg-white border border-slate-200 rounded-md text-sm text-slate-800 focus:outline-none focus:border-[#1E88E5] focus:ring-1 focus:ring-[#1E88E5]"
            />
          </div>
          <button className="flex items-center gap-2 px-4 py-2 bg-[#7E57C2] hover:bg-[#6b47ab] text-white rounded-md text-sm font-medium transition-colors">
            <Download className="w-4 h-4" /> Export CSV
          </button>
        </div>
      </header>

      <div className="flex-1 flex gap-6 min-h-0">
        <div className="w-64 bg-white border border-slate-200 rounded-lg p-4 overflow-y-auto hidden md:block shadow-sm">
          <div className="flex items-center gap-2 text-slate-800 mb-6 font-bold uppercase text-xs">
            <Filter className="w-4 h-4 text-[#1E88E5]" /> Attributes Filter
          </div>
          <FilterSection title="RISK CLASSIFICATION" options={["Extreme Anomaly", "High Risk", "Medium Risk", "Low Risk"]} color="text-[#FF5722]" />
          <FilterSection title="PROCUREMENT METHOD" options={["Tender", "Pengadaan Langsung", "E-Purchasing"]} color="text-[#7E57C2]" />
          <FilterSection title="FUNDING SOURCE" options={["APBN", "APBD", "BLU"]} color="text-[#26C6DA]" />
        </div>

        <div className="flex-1 bg-white border border-slate-200 rounded-lg overflow-auto shadow-sm">
          <table className="w-full text-sm text-left whitespace-nowrap">
            <thead className="text-xs text-slate-500 bg-slate-50 uppercase border-b border-slate-200 sticky top-0 z-10">
              {table.getHeaderGroups().map(headerGroup => (
                <tr key={headerGroup.id}>
                  {headerGroup.headers.map(header => (
                    <th key={header.id} className="px-6 py-4 tracking-wider cursor-pointer hover:text-slate-800 bg-slate-50" onClick={header.column.getToggleSortingHandler()}>
                      {flexRender(header.column.columnDef.header, header.getContext())}
                    </th>
                  ))}
                </tr>
              ))}
            </thead>
            <tbody className="divide-y divide-slate-100">
              {table.getRowModel().rows.map(row => (
                <tr key={row.id} className={`transition-colors ${getRowClass(row.original.skor_risiko)}`}>
                  {row.getVisibleCells().map(cell => (
                    <td key={cell.id} className="px-6 py-4">
                      {flexRender(cell.column.columnDef.cell, cell.getContext())}
                    </td>
                  ))}
                </tr>
              ))}
              {table.getRowModel().rows.length === 0 && (
                <tr><td colSpan={4} className="p-8 text-center text-slate-400 font-mono">No telemetry data found.</td></tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

function FilterSection({ title, options, color }: { title: string, options: string[], color: string }) {
  return (
    <div className="mb-6">
      <h3 className={`text-xs font-bold ${color} mb-3 uppercase tracking-wider`}>{title}</h3>
      <div className="space-y-2">
        {options.map(opt => (
          <label key={opt} className="flex items-center gap-2 text-sm text-slate-600 cursor-pointer hover:text-slate-900 transition-colors">
            <input type="checkbox" className="rounded border-slate-300 text-[#1E88E5] focus:ring-[#1E88E5]" />
            {opt}
          </label>
        ))}
      </div>
    </div>
  );
}
''')
print("Script 1 complete.")
