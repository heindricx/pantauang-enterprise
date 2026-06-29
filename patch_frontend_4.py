import os

frontend_app_dir = r"D:\satdat 2026\sec\pantauang-enterprise\frontend\src\app"

with open(os.path.join(frontend_app_dir, "HomeClient.tsx"), "w") as f:
    f.write('''"use client";
import { motion } from "framer-motion";
import { Activity, Database, AlertOctagon, TrendingUp, Cpu, GitMerge, ArrowRight } from "lucide-react";
import Link from "next/link";

export default function HomeClient({ tickerData, metricsData }: { tickerData: any, metricsData: any }) {
  return (
    <div className="h-full overflow-auto flex flex-col">
      {/* 1. Ticker Banner */}
      <div className="h-10 bg-white border-b border-slate-200 flex items-center overflow-hidden shadow-sm z-20 shrink-0">
        <div className="flex px-4 items-center bg-orange-50 h-full border-r border-orange-200 z-10 font-bold text-xs text-[#FF5722] uppercase tracking-widest whitespace-nowrap">
          <Activity className="w-4 h-4 mr-2 animate-pulse" /> Live Extreme Anomalies
        </div>
        <div className="flex-1 overflow-hidden relative h-full">
          <div className="animate-[marquee_20s_linear_infinite] whitespace-nowrap flex gap-10 absolute items-center h-full">
            {tickerData?.length > 0 ? tickerData.map((t: any, i: number) => (
              <span key={i} className="text-slate-600 font-sans text-xs">
                <span className="text-[#FF5722] font-bold">[{t.score.toFixed(2)}]</span> {t.agenda} - Rp {(t.pagu/1e9).toFixed(2)}M
              </span>
            )) : <span className="text-slate-400 font-sans text-xs">NO LIVE ANOMALIES DETECTED</span>}
          </div>
        </div>
      </div>

      {/* 2. Hero Mission Control */}
      <div className="flex-1 p-6 md:p-12 relative flex flex-col justify-center">
        <div className="absolute inset-0 z-0 opacity-10 pointer-events-none" 
             style={{ backgroundImage: 'radial-gradient(circle at 50% 50%, #1E88E5 1px, transparent 1px)', backgroundSize: '40px 40px' }} />
        
        <div className="z-10 w-full max-w-7xl mx-auto">
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="mb-12">
            <h1 className="font-serif text-[clamp(2.5rem,6vw,5rem)] font-black tracking-tighter text-slate-800 mb-4 uppercase leading-[1.1]">
              Intelligence <span className="text-transparent bg-clip-text bg-gradient-to-r from-[#1E88E5] to-[#7E57C2]">Node.</span>
            </h1>
            <p className="text-slate-500 font-sans text-[clamp(1rem,1.5vw,1.125rem)] max-w-2xl border-l-4 border-[#1E88E5] pl-4 mb-8">
              Platform PantaUang Kita menyediakan analisis risiko pengadaan barang dan jasa pemerintah menggunakan machine learning mutakhir Distil-IndoBERT dan QRLGBM.
            </p>
            <div className="flex flex-col sm:flex-row gap-4">
              <Link href="/data" className="flex items-center justify-center gap-2 px-8 py-4 bg-slate-900 hover:bg-slate-800 text-white rounded-lg font-bold transition-all shadow-md">
                Mulai Eksplorasi <ArrowRight className="w-5 h-5" />
              </Link>
              <Link href="/peta" className="flex items-center justify-center gap-2 px-8 py-4 bg-white border border-slate-200 hover:bg-slate-50 text-slate-700 rounded-lg font-bold transition-all shadow-sm">
                Lihat Peta Risiko
              </Link>
            </div>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
            <div className="tech-border p-6 rounded-lg border-l-4 border-l-[#1E88E5]">
              <div className="flex items-center gap-3 mb-2 text-slate-500 font-sans font-bold text-xs uppercase"><Database className="w-4 h-4 text-[#1E88E5]" /> Data Analisis</div>
              <div className="text-3xl md:text-4xl font-black font-sans text-slate-800">{metricsData?.total_data_exact?.toLocaleString() || "3,009,417"}</div>
            </div>
            <div className="tech-border p-6 rounded-lg border-l-4 border-l-[#7E57C2]">
              <div className="flex items-center gap-3 mb-2 text-slate-500 font-sans font-bold text-xs uppercase"><TrendingUp className="w-4 h-4 text-[#7E57C2]" /> Total Anggaran Evaluasi</div>
              <div className="text-3xl md:text-4xl font-black font-sans text-slate-800">Rp {metricsData?.total_anggaran ? (metricsData.total_anggaran / 1e12).toFixed(2) : "..."} T</div>
            </div>
            <div className="tech-border p-6 rounded-lg border-l-4 border-l-[#FF5722] bg-orange-50/30">
              <div className="flex items-center gap-3 mb-2 text-[#FF5722] font-sans font-bold text-xs uppercase"><AlertOctagon className="w-4 h-4" /> Rasio Anomali Ekstrem</div>
              <div className="text-3xl md:text-4xl font-black font-sans text-[#FF5722]">{metricsData?.anomaly_ratio ? metricsData.anomaly_ratio + "%" : "7.47%"}</div>
            </div>
          </div>

        </div>
      </div>
      <style dangerouslySetInnerHTML={{__html: `
        @keyframes marquee { 0% { transform: translateX(100vw); } 100% { transform: translateX(-100%); } }
      `}} />
    </div>
  );
}
''')

print("Home CTA updated")
