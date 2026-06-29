import type { Metadata } from "next";
import { Inter } from "next/font/google"; // Using Inter as fallback for Mona Sans if local font fails
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "PantaUang Kita | Intelijen Pengadaan Nasional",
  description: "Platform intelijen pengadaan nasional berbasis AI.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="id">
      <body className={`${inter.className} bg-slate-50 text-slate-800 antialiased`}>
        {children}
      </body>
    </html>
  );
}
