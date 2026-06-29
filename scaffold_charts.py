import os

frontend_src_dir = r"D:\satdat 2026\sec\pantauang-enterprise\frontend\src"

# 1. ECharts Components
echarts_comp = os.path.join(frontend_src_dir, "components/dashboard/RiskCharts.tsx")
with open(echarts_comp, "w") as f:
    f.write('''"use client";
import ReactECharts from "echarts-for-react";

export function RiskDistributionChart() {
  const options = {
    title: { text: "Distribusi Kategori Risiko", left: "center" },
    tooltip: { trigger: "item" },
    legend: { bottom: "0%" },
    series: [
      {
        name: "Risiko",
        type: "pie",
        radius: ["40%", "70%"],
        data: [
          { value: 1048, name: "Tinggi", itemStyle: { color: "#F28A6A" } },
          { value: 735, name: "Sedang", itemStyle: { color: "#FF7A3D" } },
          { value: 580, name: "Rendah", itemStyle: { color: "#52C7D8" } },
        ]
      }
    ]
  };
  return <ReactECharts option={options} style={{ height: "100%", width: "100%" }} />;
}

export function BudgetTrendChart() {
  const options = {
    title: { text: "Tren Pagu vs Prediksi Wajar P90", left: "center" },
    tooltip: { trigger: "axis" },
    xAxis: { type: "category", data: ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun"] },
    yAxis: { type: "value" },
    series: [
      { data: [820, 932, 901, 934, 1290, 1330], type: "line", name: "Pagu Asli", smooth: true, itemStyle: { color: "#0D5CBD" } },
      { data: [800, 900, 850, 900, 1100, 1200], type: "line", name: "P90 (Wajar)", smooth: true, itemStyle: { color: "#8A63E8" }, lineStyle: { type: "dashed" } },
    ]
  };
  return <ReactECharts option={options} style={{ height: "100%", width: "100%" }} />;
}
''')

# Update dashboard to use actual charts
dashboard_page = os.path.join(frontend_src_dir, "app/dashboard/page.tsx")
with open(dashboard_page, "w") as f:
    f.write('''"use client";
import { useEffect, useState } from "react";
import { RiskDistributionChart, BudgetTrendChart } from "@/components/dashboard/RiskCharts";

export default function DashboardHome() {
  const [metrics, setMetrics] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("http://localhost:8000/dashboard/metrics")
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
''')

# 3. Virtualized Table Component
procurement_page = os.path.join(frontend_src_dir, "app/procurement/page.tsx")
with open(procurement_page, "w") as f:
    f.write('''"use client";
import { Sidebar } from "@/components/layout/Sidebar";
import { useEffect, useState } from "react";

export default function ProcurementPage() {
  const [data, setData] = useState([]);
  
  useEffect(() => {
    fetch("http://localhost:8000/procurement?limit=100")
      .then(res => res.json())
      .then(d => setData(d.data || []));
  }, []);

  return (
    <div className="flex h-screen bg-slate-50 overflow-hidden">
      <Sidebar />
      <div className="flex-1 flex flex-col ml-64">
        <header className="h-16 bg-white border-b border-slate-200 flex items-center px-8 shadow-sm z-10">
          <h2 className="text-lg font-semibold text-slate-800">Eksplorasi Data Pengadaan</h2>
        </header>
        <main className="flex-1 p-6 relative overflow-auto">
          <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full text-sm text-left">
                <thead className="text-xs text-slate-500 bg-slate-50 uppercase sticky top-0">
                  <tr>
                    <th className="px-6 py-4">Agenda / Paket</th>
                    <th className="px-6 py-4">Lembaga</th>
                    <th className="px-6 py-4">Pagu (Rp)</th>
                    <th className="px-6 py-4">P90 (Wajar)</th>
                    <th className="px-6 py-4">Skor Risiko</th>
                    <th className="px-6 py-4">Status</th>
                  </tr>
                </thead>
                <tbody>
                  {data.map((row: any) => (
                    <tr key={row.id} className="border-b border-slate-100 hover:bg-slate-50">
                      <td className="px-6 py-4 font-medium text-slate-900 line-clamp-2" title={row.agenda}>{row.agenda.substring(0, 50)}...</td>
                      <td className="px-6 py-4">{row.lembaga}</td>
                      <td className="px-6 py-4">{row.pagu?.toLocaleString()}</td>
                      <td className="px-6 py-4">{row.p90?.toLocaleString()}</td>
                      <td className="px-6 py-4">{row.skor_risiko?.toFixed(2)}</td>
                      <td className="px-6 py-4">
                        <span className={`px-2 py-1 rounded-full text-xs font-semibold ${row.kategori_risiko === 'Tinggi' ? 'bg-red-100 text-red-700' : 'bg-green-100 text-green-700'}`}>
                          {row.kategori_risiko}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
''')

# Create page for anomalies, analytics, etc
for page in ["anomalies", "analytics", "ml", "reports", "settings"]:
    d = os.path.join(frontend_src_dir, f"app/{page}")
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "page.tsx"), "w") as f:
        f.write(f'''import {{ Sidebar }} from "@/components/layout/Sidebar";
export default function {page.capitalize()}Page() {{
  return (
    <div className="flex h-screen bg-slate-50 overflow-hidden">
      <Sidebar />
      <div className="flex-1 flex flex-col ml-64">
        <header className="h-16 bg-white border-b border-slate-200 flex items-center px-8 shadow-sm z-10">
          <h2 className="text-lg font-semibold text-slate-800">{page.capitalize()}</h2>
        </header>
        <main className="flex-1 p-6 relative">
          <div className="bg-white p-8 rounded-xl border border-slate-200 shadow-sm text-center">
            <h3 className="text-xl font-medium text-slate-600">Modul {page} sedang dalam tahap integrasi...</h3>
          </div>
        </main>
      </div>
    </div>
  );
}}
''')

print("Charts, Table and remaining pages scaffolded successfully!")
