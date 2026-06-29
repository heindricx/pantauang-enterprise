import os

frontend_src_dir = r"D:\satdat 2026\sec\pantauang-enterprise\frontend\src"

dirs = [
    "components/ui",
    "components/layout",
    "components/dashboard",
    "components/map",
    "lib",
    "hooks",
    "store",
    "app/dashboard",
    "app/procurement",
    "app/risk-map"
]

for d in dirs:
    os.makedirs(os.path.join(frontend_src_dir, d), exist_ok=True)

layout_tsx = os.path.join(frontend_src_dir, "app/layout.tsx")
with open(layout_tsx, "w") as f:
    f.write('''import type { Metadata } from "next";
import { Inter } from "next/font/google"; // Using Inter as fallback for Mona Sans if local font fails
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "PantaUang Kita | Intelijen Pengadaan Nasional",
  description: "Platform intelijen pengadaan nasional berbasis AI.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="id">
      <body className={`${inter.className} bg-slate-50 text-slate-800 antialiased`}>
        {children}
      </body>
    </html>
  );
}
''')

page_tsx = os.path.join(frontend_src_dir, "app/page.tsx")
with open(page_tsx, "w") as f:
    f.write('''import Link from 'next/link';

export default function LandingPage() {
  return (
    <div className="relative min-h-screen overflow-hidden bg-slate-50">
      {/* Animated background gradient mesh simulation */}
      <div className="absolute top-0 left-0 w-full h-full overflow-hidden -z-10">
        <div className="absolute -top-40 -left-40 w-96 h-96 bg-blue-400 rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-blob"></div>
        <div className="absolute top-0 -right-40 w-96 h-96 bg-purple-400 rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-blob animation-delay-2000"></div>
        <div className="absolute -bottom-40 left-20 w-96 h-96 bg-orange-400 rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-blob animation-delay-4000"></div>
      </div>

      <main className="flex flex-col items-center justify-center min-h-screen px-4 text-center">
        <h1 className="text-6xl md:text-8xl font-extrabold tracking-tight text-slate-900 mb-6 drop-shadow-sm">
          PantaUang Kita
        </h1>
        <p className="text-xl md:text-2xl font-medium text-slate-600 mb-10 max-w-3xl">
          Platform Intelijen Risiko Pengadaan Nasional Berbasis AI
        </p>
        
        <div className="flex flex-col sm:flex-row gap-4">
          <Link href="/dashboard" className="px-8 py-4 bg-[#0D5CBD] hover:bg-blue-700 text-white rounded-lg font-semibold text-lg transition-all shadow-lg hover:shadow-xl hover:-translate-y-1">
            Eksplor Data
          </Link>
          <Link href="/dashboard" className="px-8 py-4 bg-white border-2 border-slate-200 hover:border-slate-300 text-slate-700 rounded-lg font-semibold text-lg transition-all shadow-sm hover:shadow-md hover:-translate-y-1">
            Lihat Analisis
          </Link>
        </div>
      </main>
    </div>
  );
}
''')

sidebar_tsx = os.path.join(frontend_src_dir, "components/layout/Sidebar.tsx")
with open(sidebar_tsx, "w") as f:
    f.write('''import Link from "next/link";
import { LayoutDashboard, Database, Map, BarChart2, AlertTriangle, Cpu, FileText, Settings } from "lucide-react";

export function Sidebar() {
  const menuItems = [
    { name: "Dashboard", href: "/dashboard", icon: LayoutDashboard },
    { name: "Data Pengadaan", href: "/procurement", icon: Database },
    { name: "Peta Risiko", href: "/risk-map", icon: Map },
    { name: "Analitik", href: "/analytics", icon: BarChart2 },
    { name: "Anomali", href: "/anomalies", icon: AlertTriangle },
    { name: "Model AI", href: "/ml", icon: Cpu },
    { name: "Laporan", href: "/reports", icon: FileText },
    { name: "Pengaturan", href: "/settings", icon: Settings },
  ];

  return (
    <aside className="w-64 h-screen bg-[#1E293B] text-slate-300 flex flex-col fixed left-0 top-0">
      <div className="h-16 flex items-center px-6 font-bold text-white text-xl border-b border-slate-700/50">
        PantaUang Kita
      </div>
      <nav className="flex-1 py-4 overflow-y-auto">
        <ul className="space-y-1 px-3">
          {menuItems.map((item) => (
            <li key={item.name}>
              <Link href={item.href} className="flex items-center px-3 py-2.5 rounded-md hover:bg-slate-800 hover:text-white transition-colors">
                <item.icon className="w-5 h-5 mr-3" />
                <span className="font-medium text-sm">{item.name}</span>
              </Link>
            </li>
          ))}
        </ul>
      </nav>
    </aside>
  );
}
''')

dashboard_layout = os.path.join(frontend_src_dir, "app/dashboard/layout.tsx")
with open(dashboard_layout, "w") as f:
    f.write('''import { Sidebar } from "@/components/layout/Sidebar";

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex h-screen bg-slate-50 overflow-hidden">
      <Sidebar />
      <div className="flex-1 flex flex-col ml-64">
        <header className="h-16 bg-white border-b border-slate-200 flex items-center px-8 shadow-sm z-10">
          <h2 className="text-lg font-semibold text-slate-800">Overview</h2>
        </header>
        <main className="flex-1 overflow-auto p-8">
          {children}
        </main>
      </div>
    </div>
  );
}
''')

dashboard_page = os.path.join(frontend_src_dir, "app/dashboard/page.tsx")
with open(dashboard_page, "w") as f:
    f.write('''"use client";
import { useEffect, useState } from "react";

export default function DashboardHome() {
  const [metrics, setMetrics] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("http://localhost:8000/dashboard/metrics")
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

  if (loading) return <div>Memuat metrik intelijen...</div>;

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-slate-900">Dashboard Eksekutif</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <MetricCard title="Total Anggaran" value={metrics?.total_anggaran ? `Rp ${(metrics.total_anggaran / 1e12).toFixed(2)} Triliun` : "-"} color="bg-[#0D5CBD]" />
        <MetricCard title="Total Paket" value={metrics?.total_paket?.toLocaleString() || "-"} color="bg-[#52C7D8]" />
        <MetricCard title="Risiko Tinggi" value={metrics?.risiko_tinggi?.toLocaleString() || "-"} color="bg-[#F28A6A]" />
        <MetricCard title="Estimasi Potensi Anomali" value={metrics?.estimasi_potensi_anomali ? `Rp ${(metrics.estimasi_potensi_anomali / 1e9).toFixed(2)} Miliar` : "-"} color="bg-[#FF7A3D]" />
      </div>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-8">
        <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm h-96 flex items-center justify-center">
          <p className="text-slate-400 font-medium">Distribusi Risiko (ECharts Akan Dimuat)</p>
        </div>
        <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm h-96 flex items-center justify-center">
          <p className="text-slate-400 font-medium">Tren Anggaran (ECharts Akan Dimuat)</p>
        </div>
      </div>
    </div>
  );
}

function MetricCard({ title, value, color }: { title: str, value: string, color: string }) {
  return (
    <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm flex items-start space-x-4">
      <div className={`w-12 h-12 rounded-lg ${color} bg-opacity-10 flex items-center justify-center shrink-0`}>
        <div className={`w-4 h-4 rounded-full ${color}`}></div>
      </div>
      <div>
        <p className="text-sm font-medium text-slate-500 mb-1">{title}</p>
        <h3 className="text-2xl font-bold text-slate-900">{value}</h3>
      </div>
    </div>
  );
}
''')

print("Frontend pages scaffolded successfully!")
