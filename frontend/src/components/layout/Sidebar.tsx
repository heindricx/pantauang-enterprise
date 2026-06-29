"use client";
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
