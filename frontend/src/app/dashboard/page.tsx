"use client";
import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { RiskDistributionChart, BudgetTrendChart } from "@/components/dashboard/RiskCharts";

export default function DashboardHome() {
  const [metrics, setMetrics] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
    fetch(`${apiUrl}/dashboard/metrics`)
      .then(res => res.json())
      .then(data => {
        setMetrics(data);
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        setLoading(false);
      });
  }, []);

  if (loading) return (
    <div className="h-full flex items-center justify-center">
      <div className="animate-pulse flex flex-col items-center">
        <div className="w-12 h-12 rounded-full border-4 border-t-[#0D5CBD] border-slate-200 animate-spin mb-4"></div>
        <p className="text-slate-500 font-medium">Sinkronisasi Jutaan Data TiDB...</p>
      </div>
    </div>
  );

  return (
    <motion.div 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
      className="space-y-8"
    >
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6">
        <MetricCard delay={0.1} title="Total Anggaran" value={metrics?.total_anggaran ? `Rp ${(metrics.total_anggaran / 1e12).toFixed(2)} Triliun` : "-"} color="bg-[#0D5CBD]" />
        <MetricCard delay={0.2} title="Total Paket" value={metrics?.total_paket?.toLocaleString() || "-"} color="bg-[#52C7D8]" />
        <MetricCard delay={0.3} title="Risiko Tinggi" value={metrics?.risiko_tinggi?.toLocaleString() || "-"} color="bg-[#F28A6A]" />
        <MetricCard delay={0.4} title="Potensi Anomali" value={metrics?.estimasi_potensi_anomali ? `Rp ${(metrics.estimasi_potensi_anomali / 1e9).toFixed(2)} Miliar` : "-"} color="bg-[#FF7A3D]" />
      </div>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <motion.div 
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.6, delay: 0.5 }}
          className="glass-card p-8 rounded-3xl h-[450px] flex items-center justify-center relative overflow-hidden group"
        >
          <div className="absolute top-0 right-0 w-32 h-32 bg-orange-100/50 rounded-full blur-[40px] group-hover:scale-150 transition-transform duration-700"></div>
          <RiskDistributionChart data={metrics?.risk_distribution || []} />
        </motion.div>
        
        <motion.div 
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.6, delay: 0.6 }}
          className="glass-card p-8 rounded-3xl h-[450px] flex items-center justify-center relative overflow-hidden group"
        >
          <div className="absolute top-0 right-0 w-32 h-32 bg-purple-100/50 rounded-full blur-[40px] group-hover:scale-150 transition-transform duration-700"></div>
          <BudgetTrendChart data={metrics?.budget_trend || {months: [], pagu: [], p90: []}} />
        </motion.div>
      </div>
    </motion.div>
  );
}

function MetricCard({ title, value, color, delay }: { title: string, value: string, color: string, delay: number }) {
  return (
    <motion.div 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay }}
      className="glass-card p-6 rounded-3xl flex flex-col justify-between min-h-[160px] relative overflow-hidden group cursor-default"
    >
      <div className={`absolute -right-4 -top-4 w-24 h-24 rounded-full ${color} opacity-[0.03] group-hover:opacity-10 group-hover:scale-150 transition-all duration-700`}></div>
      <p className="text-sm font-semibold text-slate-500 uppercase tracking-wide">{title}</p>
      <h3 className="text-3xl lg:text-4xl font-bold tracking-tight text-slate-800 mt-2">{value}</h3>
    </motion.div>
  );
}
