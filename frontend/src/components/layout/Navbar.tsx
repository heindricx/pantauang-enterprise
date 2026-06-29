"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { Home, PieChart, Map as MapIcon, Database, FileText, Menu, X } from "lucide-react";
import { useState } from "react";

export function Navbar() {
  const pathname = usePathname();
  const [isOpen, setIsOpen] = useState(false);
  
  const menuItems = [
    { name: "Home", href: "/", icon: Home, color: "text-[#1E88E5]" },
    { name: "Infografis", href: "/infografis", icon: PieChart, color: "text-[#FF8A65]" },
    { name: "Peta", href: "/peta", icon: MapIcon, color: "text-[#26C6DA]" },
    { name: "Data", href: "/data", icon: Database, color: "text-[#7E57C2]" },
    { name: "About", href: "/about", icon: FileText, color: "text-[#FF5722]" },
  ];

  return (
    <>
      <header className="h-16 w-full bg-white border-b border-slate-200 flex items-center justify-between px-6 z-50 shadow-sm shrink-0 relative">
        <div className="flex items-center">
          <span className="font-serif font-black text-2xl tracking-tighter text-slate-800">
            Panta<span className="text-[#1E88E5]">Uang</span>
          </span>
        </div>
        
        {/* Desktop Nav */}
        <nav className="hidden md:flex gap-1">
          {menuItems.map((item) => {
            const isActive = pathname === item.href;
            return (
              <Link 
                key={item.name}
                href={item.href} 
                className={`flex items-center px-4 py-2 rounded-md transition-all duration-200 font-bold text-sm ${
                  isActive 
                  ? "bg-slate-50 text-slate-900 border border-slate-200 shadow-sm" 
                  : "text-slate-500 hover:bg-slate-50 hover:text-slate-800"
                }`}
              >
                <item.icon className={`w-4 h-4 mr-2 ${isActive ? item.color : "text-slate-400"}`} />
                {item.name}
              </Link>
            );
          })}
        </nav>

        {/* Mobile Hamburger */}
        <button className="md:hidden p-2 text-slate-600 hover:text-slate-900" onClick={() => setIsOpen(!isOpen)}>
          {isOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
        </button>
      </header>

      {/* Mobile Drawer */}
      {isOpen && (
        <div className="md:hidden absolute top-16 left-0 w-full bg-white border-b border-slate-200 shadow-lg z-40 flex flex-col p-4 animate-in slide-in-from-top-2">
          {menuItems.map((item) => {
            const isActive = pathname === item.href;
            return (
              <Link 
                key={item.name}
                href={item.href} 
                onClick={() => setIsOpen(false)}
                className={`flex items-center px-4 py-4 rounded-md transition-all duration-200 font-bold text-base mb-2 ${
                  isActive 
                  ? "bg-slate-50 text-slate-900 border border-slate-200 shadow-sm" 
                  : "text-slate-500 hover:bg-slate-50 hover:text-slate-800"
                }`}
              >
                <item.icon className={`w-5 h-5 mr-3 ${isActive ? item.color : "text-slate-400"}`} />
                {item.name}
              </Link>
            );
          })}
        </div>
      )}
    </>
  );
}
