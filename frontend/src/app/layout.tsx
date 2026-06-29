import type { Metadata } from "next";
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
