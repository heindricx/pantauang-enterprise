import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { Sidebar } from "@/components/layout/Sidebar";

const inter = Inter({ subsets: ["latin"] });

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
    <html lang="id" className="light">
      <body className={`${inter.className} bg-slate-50 text-slate-800 overflow-hidden`}>
        <div className="flex h-screen w-full relative">
          <Sidebar />
          <main className="flex-1 ml-20 md:ml-64 relative overflow-hidden flex flex-col h-full bg-slate-50">
            {children}
          </main>
        </div>
      </body>
    </html>
  );
}
