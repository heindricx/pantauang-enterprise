"use client";
import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { Activity, Database, AlertOctagon, TrendingUp, Cpu, GitMerge } from "lucide-react";

export default function Home() {
  const [ticker, setTicker] = useState([]);
  const [metrics, setMetrics] = useState<any>(null);

  useEffect(() => {
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
    // Fetch Ticker
    fetch(`${apiUrl}/api/ticker`).then(res => res.json()).then(setTicker).catch(console.error);
    // Fetch Metrics
    fetch(`${apiUrl}/dashboard/metrics`).then(res => res.json()).then(setMetrics).catch(console.error);
  }, []);

  return (
    <div className="h-full overflow-auto flex flex-col">
      {/* 1. Ticker Banner */}
      <div className="h-10 bg-black/80 border-b border-red-900/50 flex items-center overflow-hidden">
        <div className="flex px-4 items-center bg-red-950/80 h-full border-r border-red-900/50 z-10 font-bold text-xs text-red-500 uppercase tracking-widest whitespace-nowrap shadow-[0_0_10px_rgba(239,68,68,0.2)]">
          <Activity className="w-4 h-4 mr-2 animate-pulse" /> Live Extreme Anomalies
        </div>
        <div className="flex-1 overflow-hidden relative">
          <div className="animate-[marquee_20s_linear_infinite] whitespace-nowrap flex gap-10 absolute">
            {ticker.length > 0 ? ticker.map((t: any, i) => (
              <span key={i} className="text-red-400 font-mono text-xs">
                [{t.score.toFixed(2)}] {t.agenda} - Rp {(t.pagu/1e9).toFixed(2)}M
              </span>
            )) : <span className="text-slate-600 font-mono text-xs">AWAITING TELEMETRY...</span>}
          </div>
        </div>
      </div>

      {/* 2. Hero Mission Control */}
      <div className="flex-1 p-8 md:p-12 relative flex flex-col justify-center">
        {/* Abstract Network Background */}
        <div className="absolute inset-0 z-0 opacity-20 pointer-events-none" 
             style={{ backgroundImage: 'radial-gradient(circle at 50% 50%, #0D5CBD 1px, transparent 1px)', backgroundSize: '40px 40px' }} />
        
        <div className="z-10 w-full max-w-7xl mx-auto">
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="mb-12">
            <h1 className="text-5xl md:text-7xl font-black tracking-tighter text-white mb-4 uppercase">
              Intelligence <span className="text-transparent bg-clip-text bg-gradient-to-r from-[#0D5CBD] to-[#52C7D8]">Node.</span>
            </h1>
            <p className="text-slate-400 font-mono text-sm md:text-base max-w-2xl border-l-2 border-[#0D5CBD] pl-4">
              PantaUang Kita Enterprise Architecture. Powered by Distil-IndoBERT and Quantile Regression LightGBM (QRLGBM) for public procurement anomaly detection.
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-16">
            <div className="tech-border p-6 rounded-lg border-l-4 border-l-[#0D5CBD]">
              <div className="flex items-center gap-3 mb-2 text-slate-400 font-mono text-xs uppercase"><Database className="w-4 h-4" /> Data Latih & Uji</div>
              <div className="text-4xl font-black font-mono text-white">{metrics?.total_data_exact?.toLocaleString() || "..."}</div>
            </div>
            <div className="tech-border p-6 rounded-lg border-l-4 border-l-[#52C7D8]">
              <div className="flex items-center gap-3 mb-2 text-slate-400 font-mono text-xs uppercase"><TrendingUp className="w-4 h-4" /> Total Budget Evaluated</div>
              <div className="text-4xl font-black font-mono text-white">Rp {metrics?.total_anggaran ? (metrics.total_anggaran / 1e12).toFixed(2) : "..."} T</div>
            </div>
            <div className="tech-border p-6 rounded-lg border-l-4 border-l-red-500 shadow-[0_0_20px_rgba(239,68,68,0.1)]">
              <div className="flex items-center gap-3 mb-2 text-red-400 font-mono text-xs uppercase"><AlertOctagon className="w-4 h-4" /> Extreme Anomaly Ratio</div>
              <div className="text-4xl font-black font-mono text-red-500">{metrics?.anomaly_ratio ? metrics.anomaly_ratio + "%" : "..."}</div>
            </div>
          </div>

          {/* Stepper */}
          <div className="mt-8">
            <h3 className="text-xs font-mono text-slate-500 mb-6 uppercase tracking-widest">Scientific Methodology Pipeline</h3>
            <div className="flex flex-col md:flex-row gap-4 items-center w-full">
              {[
                { icon: Database, label: "Data RUP Input" },
                { icon: Cpu, label: "Distil-IndoBERT + PCA" },
                { icon: GitMerge, label: "Integrasi Fitur" },
                { icon: Activity, label: "QRLGBM Modeling" },
                { icon: AlertOctagon, label: "Risk Categorization" }
              ].map((step, idx, arr) => (
                <div key={idx} className="flex items-center w-full md:w-auto flex-1">
                  <div className="tech-border px-4 py-3 rounded text-center flex-1 min-w-max flex flex-col items-center gap-2">
                    <step.icon className="w-5 h-5 text-slate-400" />
                    <span className="text-[10px] font-mono text-slate-300 uppercase">{step.label}</span>
                  </div>
                  {idx < arr.length - 1 && <div className="h-8 w-px md:h-px md:w-8 bg-slate-700 mx-2"></div>}
                </div>
              ))}
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
