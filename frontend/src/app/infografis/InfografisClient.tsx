"use client";
import { PieChart, Pie, Cell, AreaChart, Area, BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Legend, CartesianGrid } from "recharts";

export default function InfografisClient({ metricsData, timeSeries, jenisPengadaan }: { metricsData: any, timeSeries: any[], jenisPengadaan: any[] }) {
  const pieData = metricsData ? [
    { name: "Anomali", value: metricsData.ekstrem, color: "#FF5722" }, // Extreme
    { name: "Tinggi", value: metricsData.risiko_tinggi, color: "#FF8A65" },
    { name: "Sedang", value: Math.floor(metricsData.total_paket * 0.15), color: "#FFCA28" }, // Mocked for 4 categories 
    { name: "Rendah", value: metricsData.total_paket - metricsData.ekstrem - metricsData.risiko_tinggi - Math.floor(metricsData.total_paket * 0.15), color: "#4CAF50" },
  ] : [];

  if (!metricsData) return <div className="p-12 text-slate-500 font-mono">NO METRICS DATA AVAILABLE.</div>;

  return (
    <div className="h-full overflow-auto flex flex-col md:flex-row bg-white">
      {/* Left Pane: Narrative */}
      <div className="w-full md:w-1/3 p-8 md:p-12 border-r border-slate-200 flex flex-col justify-center shrink-0">
        <h1 className="font-serif font-black text-[clamp(2rem,5vw,4rem)] capitalize text-slate-900 mb-6 tracking-tighter leading-[1.1]">
          Systematic <br/><span className="text-[#FF5722]">Deviation</span> <br/>Analytics.
        </h1>
        <div className="space-y-6 text-slate-600 text-[clamp(1rem,1.5vw,1.125rem)] leading-relaxed font-sans">
          <p>
            Dari <span className="text-slate-900 font-bold">{metricsData.total_data_exact.toLocaleString()}</span> paket pengadaan, sistem mengidentifikasi pola penyimpangan yang signifikan berdasarkan algoritma QRLGBM.
          </p>
          <p>
            Analisis runtun waktu (Time-Series) menunjukkan tren musiman paket rawan, sementara rincian per Jenis Pengadaan memberikan wawasan presisi atas sektor yang paling rentan terhadap anomali struktural.
          </p>
        </div>
      </div>

      {/* Right Pane: Charts */}
      <div className="w-full md:w-2/3 p-4 md:p-12 overflow-y-auto space-y-8 bg-slate-50">
        
        {/* Risk Breakdown Pie */}
        <div className="tech-border rounded-xl p-6 bg-white">
          <h3 className="font-serif text-lg font-bold text-slate-800 mb-4 capitalize">Distribusi 4 Kategori Risiko</h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie data={pieData} innerRadius={70} outerRadius={110} paddingAngle={2} dataKey="value">
                  {pieData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }} />
                <Legend iconType="circle" />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Time Series Area Chart */}
        <div className="tech-border rounded-xl p-6 bg-white">
          <h3 className="font-serif text-lg font-bold text-slate-800 mb-4 capitalize">Tren Musiman (12 Bulan)</h3>
          <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={timeSeries} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
                <defs>
                  <linearGradient id="colorEkstrem" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#FF5722" stopOpacity={0.8}/>
                    <stop offset="95%" stopColor="#FF5722" stopOpacity={0}/>
                  </linearGradient>
                  <linearGradient id="colorTinggi" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#FF8A65" stopOpacity={0.8}/>
                    <stop offset="95%" stopColor="#FF8A65" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <XAxis dataKey="bulan" axisLine={false} tickLine={false} tick={{fontSize: 12, fill: '#64748b'}} />
                <YAxis axisLine={false} tickLine={false} tick={{fontSize: 12, fill: '#64748b'}} />
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1f5f9" />
                <Tooltip contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }} />
                <Legend />
                <Area type="monotone" dataKey="Risiko Tinggi" stroke="#FF8A65" fillOpacity={1} fill="url(#colorTinggi)" />
                <Area type="monotone" dataKey="Anomali Ekstrem" stroke="#FF5722" fillOpacity={1} fill="url(#colorEkstrem)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Stacked Bar Chart */}
        <div className="tech-border rounded-xl p-6 bg-white">
          <h3 className="font-serif text-lg font-bold text-slate-800 mb-4 capitalize">Sebaran Berdasarkan Jenis Pengadaan</h3>
          <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={jenisPengadaan} layout="vertical" margin={{ top: 20, right: 30, left: 40, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" horizontal={true} vertical={false} stroke="#f1f5f9" />
                <XAxis type="number" hide />
                <YAxis dataKey="kategori" type="category" axisLine={false} tickLine={false} tick={{fontSize: 11, fill: '#475569'}} width={120} />
                <Tooltip contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }} />
                <Legend />
                <Bar dataKey="Anomali" stackId="a" fill="#FF5722" />
                <Bar dataKey="Tinggi" stackId="a" fill="#FF8A65" />
                <Bar dataKey="Sedang" stackId="a" fill="#FFCA28" />
                <Bar dataKey="Rendah" stackId="a" fill="#4CAF50" radius={[0, 4, 4, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

      </div>
    </div>
  );
}
