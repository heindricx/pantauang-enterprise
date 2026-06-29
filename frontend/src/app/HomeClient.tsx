"use client";
import { motion } from "framer-motion";
import { Activity, Database, AlertOctagon, TrendingUp, Cpu, GitMerge } from "lucide-react";

export default function HomeClient({ tickerData, metricsData }: { tickerData: any, metricsData: any }) {
  return (
    <div className="h-full overflow-auto flex flex-col">
      {/* 1. Ticker Banner */}
      <div className="h-10 bg-white border-b border-slate-200 flex items-center overflow-hidden shadow-sm z-20">
        <div className="flex px-4 items-center bg-orange-50 h-full border-r border-orange-200 z-10 font-bold text-xs text-[#FF5722] uppercase tracking-widest whitespace-nowrap">
          <Activity className="w-4 h-4 mr-2 animate-pulse" /> Live Extreme Anomalies
        </div>
        <div className="flex-1 overflow-hidden relative">
          <div className="animate-[marquee_20s_linear_infinite] whitespace-nowrap flex gap-10 absolute items-center h-full">
            {tickerData?.length > 0 ? tickerData.map((t: any, i: number) => (
              <span key={i} className="text-slate-600 font-mono text-xs">
                <span className="text-[#FF5722] font-bold">[{t.score.toFixed(2)}]</span> {t.agenda} - Rp {(t.pagu/1e9).toFixed(2)}M
              </span>
            )) : <span className="text-slate-400 font-mono text-xs">NO LIVE ANOMALIES DETECTED</span>}
          </div>
        </div>
      </div>

      {/* 2. Hero Mission Control */}
      <div className="flex-1 p-8 md:p-12 relative flex flex-col justify-center">
        {/* Abstract Network Background Light */}
        <div className="absolute inset-0 z-0 opacity-10 pointer-events-none" 
             style={{ backgroundImage: 'radial-gradient(circle at 50% 50%, #1E88E5 1px, transparent 1px)', backgroundSize: '40px 40px' }} />
        
        <div className="z-10 w-full max-w-7xl mx-auto">
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="mb-12">
            <h1 className="text-5xl md:text-7xl font-black tracking-tighter text-slate-800 mb-4 uppercase">
              Intelligence <span className="text-transparent bg-clip-text bg-gradient-to-r from-[#1E88E5] to-[#7E57C2]">Node.</span>
            </h1>
            <p className="text-slate-500 font-mono text-sm md:text-base max-w-2xl border-l-4 border-[#1E88E5] pl-4">
              PantaUang Kita Enterprise Architecture. Powered by Distil-IndoBERT and Quantile Regression LightGBM (QRLGBM) for public procurement anomaly detection.
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-16">
            <div className="tech-border p-6 rounded-lg border-l-4 border-l-[#1E88E5]">
              <div className="flex items-center gap-3 mb-2 text-slate-500 font-mono text-xs uppercase"><Database className="w-4 h-4 text-[#1E88E5]" /> Data Latih & Uji</div>
              <div className="text-4xl font-black font-mono text-slate-800">{metricsData?.total_data_exact?.toLocaleString() || "3,009,417"}</div>
            </div>
            <div className="tech-border p-6 rounded-lg border-l-4 border-l-[#7E57C2]">
              <div className="flex items-center gap-3 mb-2 text-slate-500 font-mono text-xs uppercase"><TrendingUp className="w-4 h-4 text-[#7E57C2]" /> Total Budget Evaluated</div>
              <div className="text-4xl font-black font-mono text-slate-800">Rp {metricsData?.total_anggaran ? (metricsData.total_anggaran / 1e12).toFixed(2) : "..."} T</div>
            </div>
            <div className="tech-border p-6 rounded-lg border-l-4 border-l-[#FF5722] bg-orange-50/30">
              <div className="flex items-center gap-3 mb-2 text-[#FF5722] font-mono text-xs uppercase"><AlertOctagon className="w-4 h-4" /> Extreme Anomaly Ratio</div>
              <div className="text-4xl font-black font-mono text-[#FF5722]">{metricsData?.anomaly_ratio ? metricsData.anomaly_ratio + "%" : "7.47%"}</div>
            </div>
          </div>

          {/* Stepper */}
          <div className="mt-8">
            <h3 className="text-xs font-bold text-slate-500 mb-6 uppercase tracking-widest">Scientific Methodology Pipeline</h3>
            <div className="flex flex-col md:flex-row gap-4 items-center w-full">
              {[
                { icon: Database, label: "Data RUP Input", color: "text-[#1E88E5]", border: "border-[#1E88E5]" },
                { icon: Cpu, label: "Distil-IndoBERT + PCA", color: "text-[#FF8A65]", border: "border-[#FF8A65]" },
                { icon: GitMerge, label: "Integrasi Fitur", color: "text-[#26C6DA]", border: "border-[#26C6DA]" },
                { icon: Activity, label: "QRLGBM Modeling", color: "text-[#7E57C2]", border: "border-[#7E57C2]" },
                { icon: AlertOctagon, label: "Risk Categorization", color: "text-[#FF5722]", border: "border-[#FF5722]" }
              ].map((step, idx, arr) => (
                <div key={idx} className="flex items-center w-full md:w-auto flex-1">
                  <div className={`bg-white border-2 ${step.border} px-4 py-3 rounded-lg text-center flex-1 min-w-max flex flex-col items-center gap-2 shadow-sm`}>
                    <step.icon className={`w-5 h-5 ${step.color}`} />
                    <span className="text-[10px] font-bold text-slate-600 uppercase">{step.label}</span>
                  </div>
                  {idx < arr.length - 1 && <div className="h-8 w-1 md:h-1 md:w-8 bg-slate-200 mx-2 rounded-full"></div>}
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
