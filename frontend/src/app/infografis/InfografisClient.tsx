"use client";
import {
  PieChart, Pie, Cell, AreaChart, Area, BarChart, Bar,
  XAxis, YAxis, Tooltip, ResponsiveContainer, Legend, CartesianGrid
} from "recharts";
import { motion } from "framer-motion";

const RISK_COLORS: Record<string, string> = { Anomali: "#FF5722", Tinggi: "#FF8A65", Sedang: "#FFCA28", Rendah: "#4CAF50" };
const RISK_LIGHT:  Record<string, string> = { Anomali: "#FFF3F0", Tinggi: "#FFF7F4", Sedang: "#FEFCE8", Rendah: "#F0FDF4" };

const CustomTooltip = ({ active, payload, label }: any) => {
  if (!active || !payload?.length) return null;
  return (
    <div className="glass rounded-xl px-4 py-3 shadow-xl border border-white/60 font-sans text-xs min-w-[160px]">
      <p className="font-bold text-slate-700 mb-2">{label}</p>
      {payload.map((p: any) => (
        <div key={p.dataKey} className="flex justify-between gap-4 text-slate-500">
          <span style={{ color: p.color }}>{p.dataKey}</span>
          <span className="font-bold text-slate-700">{p.value?.toLocaleString()}</span>
        </div>
      ))}
    </div>
  );
};

export default function InfografisClient({ metricsData, timeSeries, jenisPengadaan }: {
  metricsData: any; timeSeries: any[]; jenisPengadaan: any[];
}) {
  const total   = 3009417;
  const anomali = 74900;
  const tinggi  = 149801;
  const sedang  = 74900;
  const rendah  = 2709816;

  const pieData = [
    { name: "Anomali", value: anomali },
    { name: "Tinggi",  value: tinggi  },
    { name: "Sedang",  value: sedang  },
    { name: "Rendah",  value: rendah  },
  ];

  const summaryCards = [
    { label: "Total Paket",     value: total.toLocaleString(),   color: "#1E88E5", pct: "100%"                             },
    { label: "Anomali Ekstrem", value: anomali.toLocaleString(), color: RISK_COLORS.Anomali, pct: ((anomali/total)*100).toFixed(2)+"%" },
    { label: "Risiko Tinggi",   value: tinggi.toLocaleString(),  color: RISK_COLORS.Tinggi,  pct: ((tinggi/total)*100).toFixed(2)+"%"  },
    { label: "Risiko Sedang",   value: sedang.toLocaleString(),  color: RISK_COLORS.Sedang,  pct: ((sedang/total)*100).toFixed(2)+"%"  },
    { label: "Risiko Rendah",   value: rendah.toLocaleString(),  color: RISK_COLORS.Rendah,  pct: ((rendah/total)*100).toFixed(2)+"%"  },
  ];

  return (
    <div className="min-h-screen font-sans py-10 px-4 md:px-8 bg-grid">
      <div className="max-w-7xl mx-auto">

        {/* HEADER */}
        <motion.div initial={{ opacity:0, y:20 }} animate={{ opacity:1, y:0 }} className="mb-10 text-center">
          <h1 className="font-serif font-black text-[clamp(2.2rem,4vw,3.5rem)] text-slate-900 leading-tight">
            Infografis <span className="text-[#FF5722]">Risiko</span> Pengadaan
          </h1>
          <p className="text-slate-500 font-sans text-sm mt-3 max-w-2xl mx-auto">
            Dari {total.toLocaleString()} paket pengadaan, sistem mengidentifikasi pola penyimpangan signifikan menggunakan QRLGBM.
          </p>
        </motion.div>

        {/* SUMMARY STRIP */}
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3 mb-8">
          {summaryCards.map((c, i) => (
            <motion.div key={c.label} initial={{ opacity:0, y:16 }} animate={{ opacity:1, y:0 }} transition={{ delay: i*0.06 }}
              className="glass rounded-2xl p-4 border border-white/60 hover-lift cursor-default text-center">
              <div className="text-xl font-black font-sans mb-0.5" style={{ color: c.color }}>{c.pct}</div>
              <div className="text-base font-bold text-slate-800 font-sans">{c.value}</div>
              <div className="text-[10px] text-slate-400 font-sans mt-1">{c.label}</div>
            </motion.div>
          ))}
        </div>

        {/* CHARTS */}
        <div className="grid lg:grid-cols-3 gap-6">
          {/* Donut */}
          <div className="flex flex-col gap-6">
            <motion.div initial={{ opacity:0 }} whileInView={{ opacity:1 }} viewport={{ once:true }}
              className="glass rounded-3xl p-6 border border-white/60 hover-lift">
              <h3 className="font-serif font-bold text-slate-800 text-lg mb-1">Distribusi 4 Kategori</h3>
              <p className="text-slate-400 text-xs font-sans mb-4">Proporsi risiko keseluruhan paket</p>
              <div className="h-52">
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie data={pieData} innerRadius={55} outerRadius={85} paddingAngle={3} dataKey="value" stroke="none">
                      {pieData.map((e) => <Cell key={e.name} fill={RISK_COLORS[e.name]} />)}
                    </Pie>
                    <Tooltip content={<CustomTooltip />} />
                  </PieChart>
                </ResponsiveContainer>
              </div>
              <div className="grid grid-cols-2 gap-2 mt-2">
                {pieData.map(d => (
                  <div key={d.name} className="flex items-center gap-2 rounded-lg px-3 py-2 text-xs" style={{ backgroundColor: RISK_LIGHT[d.name] }}>
                    <div className="w-2 h-2 rounded-full shrink-0" style={{ backgroundColor: RISK_COLORS[d.name] }} />
                    <span className="font-bold text-slate-700 font-sans">{d.name}</span>
                    <span className="text-slate-400 ml-auto font-sans">{((d.value/total)*100).toFixed(1)}%</span>
                  </div>
                ))}
              </div>
            </motion.div>

            <motion.div initial={{ opacity:0 }} whileInView={{ opacity:1 }} viewport={{ once:true }}
              className="glass rounded-3xl p-6 border border-white/60 flex-1">
              <h3 className="font-serif font-bold text-slate-800 text-lg mb-3">Insight Kunci</h3>
              <div className="space-y-4 text-sm font-sans text-slate-600 leading-relaxed">
                <p className="p-3 bg-[#FFF3F0] rounded-xl border border-[#FF5722]/10 text-[#FF5722] font-bold">
                  {((anomali/total)*100).toFixed(2)}% dari seluruh paket terdeteksi sebagai Anomali Ekstrem (skor &gt;= 90.16)
                </p>
                <p>Akurasi model PICP Train: <strong className="text-slate-800">80.09%</strong> — Test: <strong className="text-slate-800">80.13%</strong>.</p>
                <p>Anggaran berisiko Tinggi-Anomali mencapai <strong className="text-slate-800">Rp {((metricsData?.total_anggaran || 1.2e14)/1e12).toFixed(1)} Triliun</strong>.</p>
              </div>
            </motion.div>
          </div>

          {/* Charts Right */}
          <div className="lg:col-span-2 flex flex-col gap-6">
            <motion.div initial={{ opacity:0 }} whileInView={{ opacity:1 }} viewport={{ once:true }}
              className="glass rounded-3xl p-6 border border-white/60 hover-lift">
              <h3 className="font-serif font-bold text-slate-800 text-lg mb-1">Tren Musiman — 12 Bulan</h3>
              <p className="text-slate-400 text-xs font-sans mb-4">Fluktuasi anomali dan risiko tinggi sepanjang tahun</p>
              <div className="h-64">
                <ResponsiveContainer width="100%" height="100%">
                  <AreaChart data={(timeSeries && timeSeries.length > 0) ? timeSeries : [
                    { bulan: "Jan", "Risiko Tinggi": 12500, "Anomali Ekstrem": 6200 },
                    { bulan: "Feb", "Risiko Tinggi": 13200, "Anomali Ekstrem": 6500 },
                    { bulan: "Mar", "Risiko Tinggi": 11800, "Anomali Ekstrem": 5800 },
                    { bulan: "Apr", "Risiko Tinggi": 14100, "Anomali Ekstrem": 7100 },
                    { bulan: "Mei", "Risiko Tinggi": 11000, "Anomali Ekstrem": 5200 },
                    { bulan: "Jun", "Risiko Tinggi": 15400, "Anomali Ekstrem": 7800 }
                  ]} margin={{ top: 5, right: 10, bottom: 0, left: -20 }}>
                    <defs>
                      <linearGradient id="gAnomali" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#FF5722" stopOpacity={0.25}/>
                        <stop offset="95%" stopColor="#FF5722" stopOpacity={0}/>
                      </linearGradient>
                      <linearGradient id="gTinggi" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#FF8A65" stopOpacity={0.25}/>
                        <stop offset="95%" stopColor="#FF8A65" stopOpacity={0}/>
                      </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
                    <XAxis dataKey="bulan" axisLine={false} tickLine={false} tick={{ fontSize: 11, fill: "#94a3b8" }} />
                    <YAxis axisLine={false} tickLine={false} tick={{ fontSize: 10, fill: "#94a3b8" }} />
                    <Tooltip content={<CustomTooltip />} />
                    <Area type="monotone" dataKey="Risiko Tinggi" stroke="#FF8A65" strokeWidth={2} fill="url(#gTinggi)" dot={false} />
                    <Area type="monotone" dataKey="Anomali Ekstrem" stroke="#FF5722" strokeWidth={2.5} fill="url(#gAnomali)" dot={false} />
                    <Legend wrapperStyle={{ fontFamily: "var(--font-jakarta)", fontSize: 12 }} />
                  </AreaChart>
                </ResponsiveContainer>
              </div>
            </motion.div>

            <motion.div initial={{ opacity:0 }} whileInView={{ opacity:1 }} viewport={{ once:true }}
              className="glass rounded-3xl p-6 border border-white/60 hover-lift">
              <h3 className="font-serif font-bold text-slate-800 text-lg mb-1">Sebaran Per Jenis Pengadaan</h3>
              <p className="text-slate-400 text-xs font-sans mb-4">Volume risiko berdasarkan kategori pengadaan</p>
              <div className="h-64">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={(jenisPengadaan && jenisPengadaan.length > 0) ? jenisPengadaan : [
                    { kategori: "Barang", Anomali: 35000, Tinggi: 60000, Sedang: 30000, Rendah: 800000 },
                    { kategori: "Konsultansi", Anomali: 15000, Tinggi: 40000, Sedang: 20000, Rendah: 500000 },
                    { kategori: "Konstruksi", Anomali: 20000, Tinggi: 45000, Sedang: 22000, Rendah: 600000 }
                  ]} layout="vertical" margin={{ top: 0, right: 10, left: 10, bottom: 0 }}>
                    <CartesianGrid strokeDasharray="3 3" horizontal={false} vertical={true} stroke="#e2e8f0" />
                    <XAxis type="number" hide />
                    <YAxis dataKey="kategori" type="category" axisLine={false} tickLine={false}
                      tick={{ fontSize: 11, fill: "#64748b" }} width={100} />
                    <Tooltip content={<CustomTooltip />} />
                    <Legend wrapperStyle={{ fontFamily: "var(--font-jakarta)", fontSize: 12 }} />
                    <Bar dataKey="Anomali" stackId="a" fill={RISK_COLORS.Anomali} />
                    <Bar dataKey="Tinggi"  stackId="a" fill={RISK_COLORS.Tinggi}  />
                    <Bar dataKey="Sedang"  stackId="a" fill={RISK_COLORS.Sedang}  />
                    <Bar dataKey="Rendah"  stackId="a" fill={RISK_COLORS.Rendah}  radius={[0,4,4,0]} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </motion.div>
          </div>
        </div>
      </div>
    </div>
  );
}
