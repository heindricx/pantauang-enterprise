"use client";
import { useEffect, useState } from "react";
import { RiskDistributionChart, BudgetTrendChart } from "@/components/dashboard/RiskCharts";

export default function DashboardHome() {
  const [metrics, setMetrics] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("https://heindricx-pantauang-backend.hf.space")
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

  if (loading) return <div>Memuat metrik intelijen...</div>;

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-slate-900">Dashboard Eksekutif</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <MetricCard title="Total Anggaran" value={metrics?.total_anggaran ? `Rp ${(metrics.total_anggaran / 1e12).toFixed(2)} Triliun` : "-"} color="bg-[#0D5CBD]" />
        <MetricCard title="Total Paket" value={metrics?.total_paket?.toLocaleString() || "-"} color="bg-[#52C7D8]" />
        <MetricCard title="Risiko Tinggi" value={metrics?.risiko_tinggi?.toLocaleString() || "-"} color="bg-[#F28A6A]" />
        <MetricCard title="Estimasi Potensi Anomali" value={metrics?.estimasi_potensi_anomali ? `Rp ${(metrics.estimasi_potensi_anomali / 1e9).toFixed(2)} Miliar` : "-"} color="bg-[#FF7A3D]" />
      </div>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-8">
        <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm h-96 flex items-center justify-center">
          <RiskDistributionChart />
        </div>
        <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm h-96 flex items-center justify-center">
          <BudgetTrendChart />
        </div>
      </div>
    </div>
  );
}

function MetricCard({ title, value, color }: { title: string, value: string, color: string }) {
  return (
    <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm flex items-start space-x-4">
      <div className={`w-12 h-12 rounded-lg ${color} bg-opacity-10 flex items-center justify-center shrink-0`}>
        <div className={`w-4 h-4 rounded-full ${color}`}></div>
      </div>
      <div>
        <p className="text-sm font-medium text-slate-500 mb-1">{title}</p>
        <h3 className="text-2xl font-bold text-slate-900">{value}</h3>
      </div>
    </div>
  );
}
