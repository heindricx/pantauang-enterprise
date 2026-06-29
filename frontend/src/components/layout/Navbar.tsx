"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { Home, PieChart, Map as MapIcon, Database, FileText, Menu, X } from "lucide-react";
import { useState, useEffect } from "react";

export function Navbar() {
  const pathname = usePathname();
  const [isOpen, setIsOpen] = useState(false);
  const [activeSection, setActiveSection] = useState("home");
  const isHomePage = pathname === "/";

  useEffect(() => {
    if (!isHomePage) return;
    
    const sections = ["home", "infografis", "peta", "data", "about"];
    
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          setActiveSection(entry.target.id);
        }
      });
    }, { threshold: 0.5 });

    sections.forEach(id => {
      const el = document.getElementById(id);
      if (el) observer.observe(el);
    });

    return () => observer.disconnect();
  }, [isHomePage]);

  const menuItems = [
    { name: "Home", href: "/#home", id: "home", icon: Home, color: "text-[#1E88E5]" },
    { name: "Infografis", href: "/#infografis", id: "infografis", icon: PieChart, color: "text-[#FF8A65]" },
    { name: "Peta", href: "/#peta", id: "peta", icon: MapIcon, color: "text-[#26C6DA]" },
    { name: "Data", href: "/#data", id: "data", icon: Database, color: "text-[#7E57C2]" },
    { name: "About", href: "/#about", id: "about", icon: FileText, color: "text-[#FF5722]" },
  ];

  return (
    <>
      <header className="fixed top-0 left-0 w-full h-16 bg-white/70 backdrop-blur-md flex items-center justify-between px-6 z-50 shrink-0 border-0 shadow-[0_1px_3px_rgba(0,0,0,0.02)] transition-all">
        <div className="flex items-center">
          <Link href="/#home" className="font-serif font-black text-2xl tracking-tighter text-slate-800">
            Panta<span className="text-[#1E88E5]">Uang</span>
          </Link>
        </div>
        
        {/* Desktop Nav */}
        <nav className="hidden md:flex gap-4">
          {menuItems.map((item) => {
            const isActive = isHomePage ? activeSection === item.id : pathname.includes(item.id);
            return (
              <Link 
                key={item.name}
                href={item.href} 
                className={`flex items-center px-2 py-2 transition-all duration-300 font-sans font-bold text-sm border-b-2 ${
                  isActive 
                  ? "text-slate-900 border-slate-900" 
                  : "text-slate-500 border-transparent hover:text-slate-800"
                }`}
              >
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
        <div className="md:hidden fixed top-16 left-0 w-full bg-white/90 backdrop-blur-lg border-b border-slate-100 shadow-lg z-40 flex flex-col p-4">
          {menuItems.map((item) => {
            const isActive = isHomePage ? activeSection === item.id : pathname.includes(item.id);
            return (
              <Link 
                key={item.name}
                href={item.href} 
                onClick={() => setIsOpen(false)}
                className={`flex items-center px-4 py-4 rounded-md transition-all duration-200 font-sans font-bold text-base mb-2 ${
                  isActive 
                  ? "bg-slate-50/80 text-slate-900 shadow-sm" 
                  : "text-slate-500 hover:bg-slate-50/80 hover:text-slate-800"
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
