"use client";
import { motion } from "framer-motion";
import { Activity, Database, AlertOctagon, TrendingUp, ArrowRight, ExternalLink, Map as MapIcon } from "lucide-react";
import Link from "next/link";
import { PieChart, Pie, Cell, ResponsiveContainer } from "recharts";

export default function HomeClient({ tickerData, metricsData }: { tickerData: any, metricsData: any }) {
  
  const pieData = metricsData ? [
    { name: "Anomali", value: metricsData.ekstrem, color: "#FF5722" },
    { name: "Tinggi", value: metricsData.risiko_tinggi, color: "#FF8A65" },
    { name: "Sedang", value: Math.floor(metricsData.total_paket * 0.15), color: "#FFCA28" },
    { name: "Rendah", value: metricsData.total_paket - metricsData.ekstrem - metricsData.risiko_tinggi - Math.floor(metricsData.total_paket * 0.15), color: "#4CAF50" },
  ] : [];

  return (
    <div className="w-full flex flex-col font-sans">
      
      {/* 1. Ticker Banner */}
      <div className="h-10 bg-white border-b border-slate-100 flex items-center overflow-hidden z-20 shrink-0 sticky top-16">
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

      {/* --- SECTION: HOME / HERO --- */}
      <section id="home" className="min-h-[85vh] p-6 md:p-12 relative flex flex-col justify-center items-center text-center">
        <div className="absolute inset-0 z-0 opacity-[0.03] pointer-events-none" 
             style={{ backgroundImage: 'radial-gradient(circle at 50% 50%, #1E88E5 1px, transparent 1px)', backgroundSize: '40px 40px' }} />
        
        <div className="z-10 w-full max-w-5xl mx-auto flex flex-col items-center">
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="mb-12 flex flex-col items-center">
            <h1 className="font-serif capitalize text-[clamp(3rem,6vw,5.5rem)] font-black tracking-tighter text-slate-800 mb-6 leading-[1.1]">
              Intelligence <span className="text-transparent bg-clip-text bg-gradient-to-r from-[#1E88E5] to-[#7E57C2]">Node.</span>
            </h1>
            <p className="text-slate-500 font-sans text-[clamp(1.125rem,1.5vw,1.25rem)] max-w-3xl mb-10 leading-relaxed">
              Platform PantaUang Kita menyediakan analisis risiko pengadaan barang dan jasa pemerintah menggunakan *machine learning* mutakhir Distil-IndoBERT dan QRLGBM.
            </p>
            <div className="flex flex-col sm:flex-row gap-4">
              <Link href="#infografis" className="flex items-center justify-center gap-2 px-8 py-4 bg-slate-900 hover:bg-slate-800 text-white rounded-full font-bold transition-all shadow-xl hover:shadow-2xl hover:-translate-y-1">
                Mulai Eksplorasi <ArrowRight className="w-5 h-5" />
              </Link>
            </div>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 w-full max-w-4xl">
            <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-100 flex flex-col items-center text-center">
              <Database className="w-6 h-6 text-[#1E88E5] mb-4" />
              <div className="text-3xl md:text-4xl font-black font-sans text-slate-800 mb-1">{metricsData?.total_data_exact?.toLocaleString() || "3,009,417"}</div>
              <div className="text-slate-500 font-sans font-bold text-xs capitalize">Data Analisis</div>
            </div>
            <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-100 flex flex-col items-center text-center">
              <TrendingUp className="w-6 h-6 text-[#7E57C2] mb-4" />
              <div className="text-3xl md:text-4xl font-black font-sans text-slate-800 mb-1">{metricsData?.total_anggaran ? (metricsData.total_anggaran / 1e12).toFixed(1) : "..."} T</div>
              <div className="text-slate-500 font-sans font-bold text-xs capitalize">Total Anggaran Evaluasi</div>
            </div>
            <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-100 flex flex-col items-center text-center">
              <AlertOctagon className="w-6 h-6 text-[#FF5722] mb-4" />
              <div className="text-3xl md:text-4xl font-black font-sans text-[#FF5722] mb-1">{metricsData?.anomaly_ratio ? metricsData.anomaly_ratio + "%" : "7.47%"}</div>
              <div className="text-[#FF5722] font-sans font-bold text-xs capitalize">Rasio Anomali Ekstrem</div>
            </div>
          </div>
        </div>
      </section>

      {/* --- SECTION: INFOGRAFIS PREVIEW --- */}
      <section id="infografis" className="min-h-screen p-6 md:p-12 relative flex flex-col justify-center bg-white border-t border-slate-100">
        <div className="max-w-6xl mx-auto w-full flex flex-col md:flex-row items-center gap-12">
          <div className="w-full md:w-1/2">
            <h2 className="font-serif capitalize text-[clamp(2.5rem,4vw,3.5rem)] font-black text-slate-800 mb-6 leading-tight">
              Systematic <span className="text-[#FF5722]">Deviation</span> Analytics.
            </h2>
            <p className="text-slate-500 font-sans text-[clamp(1rem,1.2vw,1.125rem)] mb-8 leading-relaxed">
              Algoritma QRLGBM kami memilah jutaan baris pengadaan menjadi matriks anomali yang tajam. Analisis struktural ini memberikan visibilitas mutlak terhadap titik buta korupsi dan inefisiensi anggaran secara instan.
            </p>
            <Link href="/infografis" className="inline-flex items-center gap-2 px-6 py-3 bg-slate-50 border border-slate-200 text-slate-700 hover:bg-slate-100 rounded-full font-bold transition-all text-sm">
              Lihat Selengkapnya <ExternalLink className="w-4 h-4" />
            </Link>
          </div>
          <div className="w-full md:w-1/2 bg-slate-50 rounded-3xl p-8 border border-slate-100 flex items-center justify-center">
             <div className="w-full h-[300px]">
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie data={pieData} innerRadius={80} outerRadius={120} paddingAngle={2} dataKey="value">
                      {pieData.map((entry, index) => <Cell key={`cell-${index}`} fill={entry.color} />)}
                    </Pie>
                  </PieChart>
                </ResponsiveContainer>
             </div>
          </div>
        </div>
      </section>

      {/* --- SECTION: PETA PREVIEW --- */}
      <section id="peta" className="min-h-screen p-6 md:p-12 relative flex flex-col justify-center bg-slate-900 text-white">
        <div className="absolute inset-0 z-0 opacity-10" style={{ backgroundImage: 'radial-gradient(circle at 50% 50%, #ffffff 1px, transparent 1px)', backgroundSize: '40px 40px' }} />
        <div className="max-w-6xl mx-auto w-full z-10 flex flex-col items-center text-center">
            <h2 className="font-serif capitalize text-[clamp(2.5rem,4vw,3.5rem)] font-black text-white mb-6 leading-tight">
              Geospatial <span className="text-[#26C6DA]">Risk Mapping.</span>
            </h2>
            <p className="text-slate-400 font-sans text-[clamp(1rem,1.2vw,1.125rem)] mb-10 max-w-2xl leading-relaxed">
              Lanskap risiko pengadaan tidak merata. Eksplorasi pemetaan koroplet kami untuk mengungkap konsentrasi anomali struktural di 38 Provinsi Indonesia. Navigasi secara spasial, temukan pola wilayah tersembunyi.
            </p>
            <div className="w-full h-[400px] bg-slate-800 rounded-3xl mb-8 border border-slate-700 shadow-2xl overflow-hidden relative flex items-center justify-center">
                <MapIcon className="w-24 h-24 text-slate-600 opacity-50" />
                <div className="absolute inset-0 flex items-center justify-center bg-gradient-to-t from-slate-900/80 to-transparent"></div>
            </div>
            <Link href="/peta" className="inline-flex items-center gap-2 px-8 py-4 bg-[#26C6DA] hover:bg-[#00BCD4] text-slate-900 rounded-full font-black transition-all shadow-lg hover:shadow-cyan-500/20">
              Eksplorasi Peta Interaktif <ExternalLink className="w-5 h-5" />
            </Link>
        </div>
      </section>

      {/* --- SECTION: DATA PREVIEW --- */}
      <section id="data" className="min-h-screen p-6 md:p-12 relative flex flex-col justify-center bg-white border-t border-slate-100">
        <div className="max-w-6xl mx-auto w-full flex flex-col md:flex-row-reverse items-center gap-12">
          <div className="w-full md:w-1/2 text-left md:text-right">
            <h2 className="font-serif capitalize text-[clamp(2.5rem,4vw,3.5rem)] font-black text-slate-800 mb-6 leading-tight">
              Audit-Ready <span className="text-[#7E57C2]">Telemetry.</span>
            </h2>
            <p className="text-slate-500 font-sans text-[clamp(1rem,1.2vw,1.125rem)] mb-8 leading-relaxed ml-auto">
              Tidak ada data yang disembunyikan. Tabel audit cerdas kami memungkinkan Anda melakukan filter multi-atribut, ekspansi baris detail (*accordion*), dan penyortiran matematis pada seluruh arsip anomali secara *real-time*.
            </p>
            <Link href="/data" className="inline-flex items-center gap-2 px-6 py-3 bg-slate-50 border border-slate-200 text-slate-700 hover:bg-slate-100 rounded-full font-bold transition-all text-sm">
              Akses Master Data <ExternalLink className="w-4 h-4" />
            </Link>
          </div>
          <div className="w-full md:w-1/2">
             <div className="w-full bg-white rounded-3xl shadow-xl border border-slate-100 overflow-hidden transform -rotate-1 hover:rotate-0 transition-transform duration-500">
                <div className="h-10 bg-slate-50 border-b border-slate-100 flex items-center px-4 gap-2">
                   <div className="w-3 h-3 rounded-full bg-red-400"></div>
                   <div className="w-3 h-3 rounded-full bg-amber-400"></div>
                   <div className="w-3 h-3 rounded-full bg-green-400"></div>
                </div>
                <div className="p-4 space-y-3">
                   {[1,2,3,4].map(i => (
                     <div key={i} className="h-12 bg-slate-50 rounded border border-slate-100 flex items-center px-4 justify-between">
                        <div className="w-2/3 h-3 bg-slate-200 rounded"></div>
                        <div className="w-16 h-4 bg-[#FF5722]/20 rounded-full"></div>
                     </div>
                   ))}
                </div>
             </div>
          </div>
        </div>
      </section>

      {/* --- SECTION: ABOUT PREVIEW --- */}
      <section id="about" className="min-h-[60vh] p-6 md:p-12 relative flex flex-col justify-center items-center text-center bg-slate-50 border-t border-slate-200">
        <div className="max-w-4xl mx-auto w-full">
            <h2 className="font-serif capitalize text-[clamp(2rem,3vw,3rem)] font-black text-slate-800 mb-6 leading-tight">
              Metodologi Saintifik & <span className="text-[#1E88E5]">Transparansi.</span>
            </h2>
            <p className="text-slate-500 font-sans text-[clamp(1rem,1.2vw,1.125rem)] mb-10 leading-relaxed max-w-2xl mx-auto">
              Dibangun khusus untuk Kompetisi Satria Data 2026. Kami percaya pada transparansi arsitektural. Telusuri bagaimana metrik evaluasi model, hiperparameter Optuna, dan arsitektur pipa data kami direkayasa.
            </p>
            <Link href="/about" className="inline-flex items-center gap-2 px-8 py-4 bg-slate-900 hover:bg-slate-800 text-white rounded-full font-bold transition-all shadow-lg">
              Baca Dokumentasi Teknis <ExternalLink className="w-5 h-5" />
            </Link>
        </div>
      </section>

      <style dangerouslySetInnerHTML={{__html: `
        @keyframes marquee { 0% { transform: translateX(100vw); } 100% { transform: translateX(-100%); } }
      `}} />
    </div>
  );
}
