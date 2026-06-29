"use client";
import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Legend } from "recharts";

export default function InfografisClient({ metricsData }: { metricsData: any }) {
  const pieData = metricsData ? [
    { name: "Extreme Anomaly", value: metricsData.ekstrem, color: "#FF5722" },
    { name: "High Risk", value: metricsData.risiko_tinggi, color: "#FF8A65" },
    { name: "Medium/Low Risk", value: metricsData.total_paket - metricsData.ekstrem - metricsData.risiko_tinggi, color: "#4CAF50" },
  ] : [];

  const featureData = [
    { name: "jenisPengadaan", p10: 0.85, p90: 0.92 },
    { name: "provinsi", p10: 0.76, p90: 0.88 },
    { name: "metode", p10: 0.65, p90: 0.72 },
    { name: "sumberDana", p10: 0.45, p90: 0.51 },
    { name: "Distil-IndoBERT", p10: 0.95, p90: 0.98 },
  ];

  if (!metricsData) return <div className="p-12 text-slate-500 font-mono">NO METRICS DATA AVAILABLE.</div>;

  return (
    <div className="h-full overflow-auto flex flex-col md:flex-row">
      {/* Left Pane: Narrative */}
      <div className="w-full md:w-1/3 bg-white p-8 md:p-12 border-r border-slate-200 flex flex-col justify-center shadow-sm z-10">
        <h1 className="text-4xl font-black uppercase text-slate-800 mb-8 tracking-tighter leading-tight">
          Systematic <br/><span className="text-[#FF5722]">Deviation</span> <br/>Detected.
        </h1>
        <div className="space-y-6 text-slate-600 text-lg leading-relaxed font-serif">
          <p>
            Dari <span className="text-slate-800 font-bold">{metricsData.total_data_exact.toLocaleString()}</span> paket pengadaan, sistem mengidentifikasi bahwa <span className="text-[#FF5722] font-bold">{metricsData.anomaly_ratio}%</span> menyimpang secara sistematis dari model historis.
          </p>
          <p>
            Analisis *Information Gain* membuktikan bahwa variabel semantik dari <span className="text-[#FF8A65] font-bold font-mono">Distil-IndoBERT</span> mendominasi akurasi prediksi, disusul oleh fitur regional (<span className="text-slate-800 font-mono text-sm">provinsi</span>) dan tipe (<span className="text-slate-800 font-mono text-sm">jenisPengadaan</span>).
          </p>
        </div>
      </div>

      {/* Right Pane: Charts */}
      <div className="w-full md:w-2/3 p-8 md:p-12 space-y-12 bg-slate-50">
        <div className="tech-border rounded-xl p-8">
          <h3 className="text-xs font-bold text-[#FF5722] mb-6 uppercase tracking-widest">Risk Category Proportion</h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie data={pieData} innerRadius={60} outerRadius={100} paddingAngle={5} dataKey="value">
                  {pieData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip contentStyle={{ backgroundColor: '#ffffff', borderColor: '#e2e8f0', color: '#1e293b' }} />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="tech-border rounded-xl p-8">
          <h3 className="text-xs font-bold text-[#7E57C2] mb-6 uppercase tracking-widest">Feature Importance (Information Gain)</h3>
          <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={featureData} layout="vertical" margin={{ top: 5, right: 30, left: 40, bottom: 5 }}>
                <XAxis type="number" stroke="#94a3b8" />
                <YAxis dataKey="name" type="category" stroke="#64748b" width={120} tick={{ fontSize: 11 }} />
                <Tooltip contentStyle={{ backgroundColor: '#ffffff', borderColor: '#e2e8f0', color: '#1e293b' }} />
                <Legend />
                <Bar dataKey="p10" name="Lower Bound (P10)" fill="#1E88E5" radius={[0, 4, 4, 0]} />
                <Bar dataKey="p90" name="Upper Bound (P90)" fill="#7E57C2" radius={[0, 4, 4, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
}
