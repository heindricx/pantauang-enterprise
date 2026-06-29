import Link from "next/link";
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
