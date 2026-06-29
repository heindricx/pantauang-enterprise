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
    <html lang="id" className="dark">
      <body className={`${inter.className} bg-slate-950 text-slate-200 overflow-hidden`}>
        <div className="flex h-screen w-full relative">
          <Sidebar />
          <main className="flex-1 ml-20 md:ml-64 relative overflow-hidden flex flex-col h-full bg-[#0a0f18]">
            {children}
          </main>
        </div>
      </body>
    </html>
  );
}
