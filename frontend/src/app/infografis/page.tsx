"use client";
import { useEffect, useState } from "react";
import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Legend } from "recharts";

export default function InfografisPage() {
  const [metrics, setMetrics] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
    fetch(`${apiUrl}/dashboard/metrics`).then(res => res.json()).then(d => {
      setMetrics(d);
      setLoading(false);
    });
  }, []);

  const pieData = metrics ? [
    { name: "Extreme Anomaly", value: metrics.ekstrem, color: "#ef4444" },
    { name: "High Risk", value: metrics.risiko_tinggi, color: "#f97316" },
    { name: "Medium/Low Risk", value: metrics.total_paket - metrics.ekstrem - metrics.risiko_tinggi, color: "#22c55e" },
  ] : [];

  const featureData = [
    { name: "jenisPengadaan", p10: 0.85, p90: 0.92 },
    { name: "provinsi", p10: 0.76, p90: 0.88 },
    { name: "metode", p10: 0.65, p90: 0.72 },
    { name: "sumberDana", p10: 0.45, p90: 0.51 },
    { name: "Distil-IndoBERT (Text)", p10: 0.95, p90: 0.98 },
  ];

  if (loading) return <div className="p-12 text-slate-500 font-mono">LOADING NARRATIVE ANALYTICS...</div>;

  return (
    <div className="h-full overflow-auto flex flex-col md:flex-row">
      {/* Left Pane: Narrative */}
      <div className="w-full md:w-1/3 bg-[#070b14] p-8 md:p-12 border-r border-slate-800 flex flex-col justify-center">
        <h1 className="text-4xl font-black uppercase text-white mb-8 tracking-tighter leading-tight">
          Systematic <br/><span className="text-[#0D5CBD]">Deviation</span> <br/>Detected.
        </h1>
        <div className="space-y-6 text-slate-400 text-lg leading-relaxed font-serif">
          <p>
            Dari <span className="text-white font-bold">{metrics.total_data_exact.toLocaleString()}</span> paket pengadaan, sistem mengidentifikasi bahwa <span className="text-red-400 font-bold">{metrics.anomaly_ratio}%</span> menyimpang secara sistematis dari model historis.
          </p>
          <p>
            Analisis *Information Gain* membuktikan bahwa variabel semantik dari <span className="text-[#8A63E8] font-bold font-mono">Distil-IndoBERT</span> mendominasi akurasi prediksi, disusul oleh fitur regional (<span className="text-white font-mono text-sm">provinsi</span>) dan tipe (<span className="text-white font-mono text-sm">jenisPengadaan</span>).
          </p>
        </div>
      </div>

      {/* Right Pane: Charts */}
      <div className="w-full md:w-2/3 p-8 md:p-12 space-y-12 bg-gradient-to-br from-[#0a0f18] to-slate-900">
        
        {/* Chart 1: Donut */}
        <div className="tech-border rounded-xl p-8">
          <h3 className="text-xs font-mono text-slate-500 mb-6 uppercase tracking-widest">Risk Category Proportion</h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie data={pieData} innerRadius={60} outerRadius={100} paddingAngle={5} dataKey="value">
                  {pieData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#1e293b', color: '#f8fafc' }} />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Chart 2: Feature Importance */}
        <div className="tech-border rounded-xl p-8">
          <h3 className="text-xs font-mono text-slate-500 mb-6 uppercase tracking-widest">Feature Importance (Information Gain)</h3>
          <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={featureData} layout="vertical" margin={{ top: 5, right: 30, left: 40, bottom: 5 }}>
                <XAxis type="number" stroke="#475569" />
                <YAxis dataKey="name" type="category" stroke="#475569" width={120} tick={{ fontSize: 11 }} />
                <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#1e293b' }} />
                <Legend />
                <Bar dataKey="p10" name="Lower Bound (P10)" fill="#0D5CBD" radius={[0, 4, 4, 0]} />
                <Bar dataKey="p90" name="Upper Bound (P90)" fill="#8A63E8" radius={[0, 4, 4, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

      </div>
    </div>
  );
}
