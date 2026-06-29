import type { Metadata } from "next";
import { Playfair_Display, Plus_Jakarta_Sans } from "next/font/google";
import "./globals.css";
import { Navbar } from "@/components/layout/Navbar";
import { Footer } from "@/components/layout/Footer";

const playfair = Playfair_Display({ subsets: ["latin"], variable: "--font-playfair", display: "swap" });
const jakarta = Plus_Jakarta_Sans({ subsets: ["latin"], variable: "--font-jakarta", display: "swap" });

export const metadata: Metadata = {
  title: "PantaUang Kita | Procurement Intelligence Platform",
  description: "Platform intelijen risiko pengadaan pemerintah berbasis machine learning.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="id" className={`${playfair.variable} ${jakarta.variable}`}>
      <body className="font-sans text-slate-800 flex flex-col min-h-screen bg-grid">
        <Navbar />
        <main className="flex-1 w-full pt-16">
          {children}
        </main>
        <Footer />
      </body>
    </html>
  );
}
