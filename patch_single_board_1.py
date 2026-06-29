import os

frontend_app_dir = r"D:\satdat 2026\sec\pantauang-enterprise\frontend\src\app"
frontend_components_dir = r"D:\satdat 2026\sec\pantauang-enterprise\frontend\src\components"

# 1. layout.tsx (Typography setup)
with open(os.path.join(frontend_app_dir, "layout.tsx"), "w") as f:
    f.write('''import type { Metadata } from "next";
import { Playfair_Display, Plus_Jakarta_Sans } from "next/font/google";
import "./globals.css";
import { Navbar } from "@/components/layout/Navbar";
import { Footer } from "@/components/layout/Footer";

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
      <body className="font-sans bg-slate-50 text-slate-800 flex flex-col min-h-screen">
        <Navbar />
        <main className="flex-1 relative w-full pt-16">
          {children}
        </main>
        <Footer />
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

# 3. Footer.tsx
os.makedirs(os.path.join(frontend_components_dir, "layout"), exist_ok=True)
with open(os.path.join(frontend_components_dir, "layout/Footer.tsx"), "w") as f:
    f.write('''export function Footer() {
  return (
    <footer className="w-full bg-slate-900 text-slate-400 py-8 px-6 mt-12 font-sans shrink-0 border-t border-slate-800">
      <div className="max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-center gap-4">
        <div>
          <span className="font-serif font-black text-xl tracking-tighter text-white">
            Panta<span className="text-[#1E88E5]">Uang</span>
          </span>
          <p className="text-xs mt-2 max-w-sm leading-relaxed">
            Platform intelijen pengadaan barang dan jasa menggunakan machine learning untuk mendeteksi anomali secara sistematis dan transparan.
          </p>
        </div>
        <div className="text-left md:text-right text-xs space-y-1">
          <p className="text-slate-300 font-bold">Data Attribution & Methodology</p>
          <p>Sumber Data: Inaproc & Sistem Informasi RUP LKPP</p>
          <p>Model Baseline: Distil-IndoBERT + QRLGBM</p>
          <p className="mt-4 text-slate-600">&copy; {new Date().getFullYear()} Satria Data Enterprise. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
}
''')

print("Step 1 done")
