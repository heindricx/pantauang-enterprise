import os

frontend_app_dir = r"D:\satdat 2026\sec\pantauang-enterprise\frontend\src\app"

ssr_helper = '''
async function fetchSSR(endpoint: string) {
  try {
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";
    const res = await fetch(`${apiUrl}${endpoint}`, { cache: 'no-store' });
    if (!res.ok) return null;
    return await res.json();
  } catch (e) {
    return null;
  }
}
'''

# 6. Infografis (page.tsx + InfografisClient.tsx)
with open(os.path.join(frontend_app_dir, "infografis/page.tsx"), "w") as f:
    f.write(ssr_helper + '''
import InfografisClient from "./InfografisClient";

export default async function InfografisPage() {
  const metrics = await fetchSSR("/dashboard/metrics") || null;
  return <InfografisClient metricsData={metrics} />;
}
''')

with open(os.path.join(frontend_app_dir, "infografis/InfografisClient.tsx"), "w") as f:
    f.write('''"use client";
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
''')

# 7. Peta (page.tsx + PetaClient.tsx)
with open(os.path.join(frontend_app_dir, "peta/page.tsx"), "w") as f:
    f.write(ssr_helper + '''
import PetaClient from "./PetaClient";

export default async function PetaPage() {
  const regions = await fetchSSR("/api/map-regions") || [];
  return <PetaClient initialRegions={regions} />;
}
''')

with open(os.path.join(frontend_app_dir, "peta/PetaClient.tsx"), "w") as f:
    f.write('''"use client";
import Map, { NavigationControl, Marker } from "react-map-gl/maplibre";
import "maplibre-gl/dist/maplibre-gl.css";
import { MapPin } from "lucide-react";

export default function PetaClient({ initialRegions }: { initialRegions: any[] }) {
  // Mock coordinates for regions for visual purpose
  const coords: any = {
    "Jawa Barat": { lat: -6.9, lng: 107.6 },
    "Jawa Timur": { lat: -7.2, lng: 112.7 },
    "DKI Jakarta": { lat: -6.2, lng: 106.8 },
    "Jawa Tengah": { lat: -7.0, lng: 110.4 },
    "Sumatera Utara": { lat: 3.5, lng: 98.6 }
  };

  return (
    <div className="h-full w-full flex relative">
      <div className="w-80 h-full bg-white/95 backdrop-blur-xl border-r border-slate-200 flex flex-col absolute left-0 top-0 z-10 shadow-lg">
        <header className="p-6 border-b border-slate-100">
          <h2 className="text-xl font-bold uppercase tracking-widest text-slate-800">Spatial Risk</h2>
          <p className="text-xs font-mono text-[#26C6DA] mt-1 font-bold">Top 5 Endangered Regions</p>
        </header>
        <div className="flex-1 overflow-auto p-4 space-y-4">
          {initialRegions.slice(0, 5).map((r: any, idx) => (
            <div key={idx} className="bg-slate-50 border border-slate-200 rounded-lg p-4 cursor-pointer hover:bg-white hover:shadow-md transition-all group">
              <div className="flex items-center justify-between mb-2">
                <h3 className="font-bold text-slate-700 group-hover:text-[#1E88E5] transition-colors flex items-center gap-2">
                  <span className="text-xs bg-[#FF5722] text-white px-1.5 py-0.5 rounded font-mono">#{idx+1}</span>
                  {r.provinsi}
                </h3>
                <MapPin className="w-4 h-4 text-slate-400 group-hover:text-[#1E88E5]" />
              </div>
              <div className="flex justify-between items-end mt-4 font-mono text-xs text-slate-500">
                <div>
                  <div className="uppercase text-[10px] text-slate-400">Incidents</div>
                  <div className="text-[#FF5722] font-bold">{r.incident_count} Flags</div>
                </div>
                <div className="text-right">
                  <div className="uppercase text-[10px] text-slate-400">Budget at Risk</div>
                  <div className="text-slate-800 font-bold">Rp {(r.total_budget / 1e12).toFixed(1)}T</div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="flex-1 w-full h-full bg-slate-100">
        <Map
          initialViewState={{ longitude: 118, latitude: -2.5, zoom: 4.5 }}
          mapStyle="https://basemaps.cartocdn.com/gl/positron-gl-style/style.json"
        >
          <NavigationControl position="bottom-right" />
          {initialRegions.map((r, i) => {
            const loc = coords[r.provinsi];
            if (!loc) return null;
            return (
              <Marker key={i} longitude={loc.lng} latitude={loc.lat}>
                <div className="bg-[#FF5722]/20 p-2 rounded-full animate-pulse">
                  <div className="bg-[#FF5722] w-4 h-4 rounded-full shadow-lg border-2 border-white"></div>
                </div>
              </Marker>
            );
          })}
        </Map>
      </div>
    </div>
  );
}
''')

# 8. About (page.tsx + AboutClient.tsx)
with open(os.path.join(frontend_app_dir, "about/page.tsx"), "w") as f:
    f.write(ssr_helper + '''
import AboutClient from "./AboutClient";

export default async function AboutPage() {
  const stats = await fetchSSR("/api/methodology-stats") || null;
  return <AboutClient stats={stats} />;
}
''')

with open(os.path.join(frontend_app_dir, "about/AboutClient.tsx"), "w") as f:
    f.write('''"use client";
import { Server, Target } from "lucide-react";

export default function AboutClient({ stats }: { stats: any }) {
  return (
    <div className="h-full overflow-auto p-8 md:p-12 bg-white">
      <div className="max-w-5xl mx-auto space-y-12">
        <header>
          <h1 className="text-3xl font-black uppercase tracking-tight mb-2 text-slate-800">Technical Model Card</h1>
          <p className="text-[#1E88E5] font-mono text-sm font-bold">Satria Data 2026 / 16_NOCturnal_SEC Documentation</p>
        </header>

        <section className="tech-border rounded-xl p-8">
          <div className="flex items-center gap-2 text-[#7E57C2] mb-6">
            <Target className="w-5 h-5" />
            <h2 className="text-lg font-bold uppercase tracking-wider">Model Evaluation Matrix</h2>
          </div>
          
          <div className="overflow-x-auto">
            <table className="w-full text-left font-mono text-sm">
              <thead className="text-xs uppercase bg-slate-50 text-slate-500">
                <tr>
                  <th className="px-6 py-4">Metric</th>
                  <th className="px-6 py-4">Train</th>
                  <th className="px-6 py-4">Test</th>
                  <th className="px-6 py-4">Notes</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {stats?.evaluation_matrix && Object.entries(stats.evaluation_matrix).map(([key, val]: any) => (
                  <tr key={key} className="hover:bg-slate-50 transition-colors">
                    <td className="px-6 py-4 font-bold text-slate-700">{key}</td>
                    <td className="px-6 py-4 text-[#4CAF50] font-bold">{val.train}</td>
                    <td className="px-6 py-4 text-[#4CAF50] font-bold">{val.test}</td>
                    <td className="px-6 py-4 text-slate-400 text-xs">{val.note}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>

        <section className="tech-border rounded-xl p-8">
          <div className="flex items-center gap-2 text-[#FF8A65] mb-6">
            <Server className="w-5 h-5" />
            <h2 className="text-lg font-bold uppercase tracking-wider">Hyperparameter Transparency (TPE Optuna)</h2>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {stats?.optuna_hyperparameters && Object.entries(stats.optuna_hyperparameters).map(([model, params]: any) => (
              <div key={model} className="bg-slate-50 p-6 rounded-lg border border-slate-200 shadow-sm">
                <h3 className="text-md font-bold mb-4 font-mono text-slate-700">{model}</h3>
                <ul className="space-y-3 font-mono text-xs">
                  {Object.entries(params).map(([p, v]: any) => (
                    <li key={p} className="flex justify-between items-center border-b border-slate-200 pb-2">
                      <span className="text-slate-500">{p}</span>
                      <span className="text-white font-bold bg-[#1E88E5] px-2 py-1 rounded">{v}</span>
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </section>
      </div>
    </div>
  );
}
''')

print("Script 2 complete.")
