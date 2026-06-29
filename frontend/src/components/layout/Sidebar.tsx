"use client";
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
