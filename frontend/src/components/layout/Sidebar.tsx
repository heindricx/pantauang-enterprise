"use client";
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
