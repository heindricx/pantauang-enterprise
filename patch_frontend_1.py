import os

frontend_app_dir = r"D:\satdat 2026\sec\pantauang-enterprise\frontend\src\app"
frontend_components_dir = r"D:\satdat 2026\sec\pantauang-enterprise\frontend\src\components"

# 1. layout.tsx
with open(os.path.join(frontend_app_dir, "layout.tsx"), "w") as f:
    f.write('''import type { Metadata } from "next";
import { Playfair_Display, Plus_Jakarta_Sans } from "next/font/google";
import "./globals.css";
import { Navbar } from "@/components/layout/Navbar";

const playfair = Playfair_Display({ subsets: ["latin"], variable: "--font-playfair" });
const jakarta = Plus_Jakarta_Sans({ subsets: ["latin"], variable: "--font-jakarta" });

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
    <html lang="id" className={`light ${playfair.variable} ${jakarta.variable}`}>
      <body className="font-sans bg-slate-50 text-slate-800 overflow-hidden flex flex-col h-screen">
        <Navbar />
        <main className="flex-1 relative overflow-auto bg-slate-50 w-full">
          {children}
        </main>
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
    
    --cp-blue: #1E88E5;      
    --cp-coral: #FF8A65;     
    --cp-purple: #7E57C2;    
    --cp-orange: #FF5722;    
    --cp-cyan: #26C6DA;      
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

.font-sans {
  font-family: var(--font-jakarta), sans-serif;
}

.font-serif {
  font-family: var(--font-playfair), serif;
}

.scrollbar-hide::-webkit-scrollbar {
    display: none;
}
.scrollbar-hide {
    -ms-overflow-style: none;
    scrollbar-width: none;
}

.tech-border {
    border: 1px solid rgba(148, 163, 184, 0.3);
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
    background: #ffffff;
}
''')

# 3. Navbar.tsx
os.makedirs(os.path.join(frontend_components_dir, "layout"), exist_ok=True)
with open(os.path.join(frontend_components_dir, "layout/Navbar.tsx"), "w") as f:
    f.write('''"use client";
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
''')

print("Step 1 done")
