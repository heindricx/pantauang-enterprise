"use client";
import { motion } from "framer-motion";
import { Activity, Database, AlertOctagon, TrendingUp, ArrowRight, ExternalLink, Map as MapIcon, BarChart2 } from "lucide-react";
import Link from "next/link";
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from "recharts";

const RISK_COLORS = { Anomali: "#FF5722", Tinggi: "#FF8A65", Sedang: "#FFCA28", Rendah: "#4CAF50" };

const fadeUp = { hidden: { opacity: 0, y: 30 }, visible: (i: number) => ({ opacity: 1, y: 0, transition: { delay: i * 0.1, duration: 0.5 } }) };

export default function HomeClient({ tickerData, metricsData }: { tickerData: any, metricsData: any }) {
  const pieData = metricsData ? [
    { name: "Anomali", value: metricsData.ekstrem || 75120, fill: RISK_COLORS.Anomali },
    { name: "Tinggi", value: metricsData.risiko_tinggi || 149871, fill: RISK_COLORS.Tinggi },
    { name: "Sedang", value: Math.floor((metricsData.total_paket || 3009417) * 0.15), fill: RISK_COLORS.Sedang },
    { name: "Rendah", value: metricsData.total_paket - (metricsData.ekstrem || 75120) - (metricsData.risiko_tinggi || 149871) - Math.floor((metricsData.total_paket || 3009417) * 0.15), fill: RISK_COLORS.Rendah },
  ] : [];

  const stats = [
    { icon: Database, label: "Data Analisis", value: (metricsData?.total_data_exact || 3009417).toLocaleString(), color: "#1E88E5", bg: "bg-[#EFF6FF]" },
    { icon: TrendingUp, label: "Total Anggaran", value: `Rp ${((metricsData?.total_anggaran || 1.2e14) / 1e12).toFixed(1)}T`, color: "#7E57C2", bg: "bg-[#F5F3FF]" },
    { icon: AlertOctagon, label: "Rasio Anomali", value: `${metricsData?.anomaly_ratio || 7.47}%`, color: "#FF5722", bg: "bg-[#FFF7ED]" },
  ];

  return (
    <div className="w-full font-sans">
      {/* TICKER */}
      <div className="h-9 bg-white/80 backdrop-blur border-b border-slate-200/60 flex items-center overflow-hidden shrink-0">
        <div className="flex items-center px-4 bg-[#FF5722]/10 h-full border-r border-[#FF5722]/20 gap-2 shrink-0">
          <Activity className="w-3.5 h-3.5 text-[#FF5722] animate-pulse" />
          <span className="text-[10px] font-bold text-[#FF5722] uppercase tracking-widest whitespace-nowrap font-sans">Live Anomalies</span>
        </div>
        <div className="flex-1 overflow-hidden relative h-full">
          <div className="animate-[marquee_25s_linear_infinite] whitespace-nowrap flex gap-8 absolute items-center h-full px-4">
            {tickerData?.length > 0 ? tickerData.map((t: any, i: number) => (
              <span key={i} className="text-slate-600 text-xs font-sans">
                <span className="text-[#FF5722] font-bold">[{t.score?.toFixed(2)}]</span> {t.agenda} � Rp {(t.pagu / 1e9).toFixed(1)}M
              </span>
            )) : <span className="text-slate-400 text-xs">Menghubungkan ke server data...</span>}
          </div>
        </div>
      </div>

      {/* HERO */}
      <section className="relative min-h-[90vh] flex items-center justify-center px-6 md:px-12 py-20 overflow-hidden">
        {/* Background gradient blobs */}
        <div className="absolute top-[-10%] left-[-5%] w-[500px] h-[500px] rounded-full bg-[#1E88E5]/8 blur-3xl pointer-events-none" />
        <div className="absolute bottom-[-10%] right-[-5%] w-[400px] h-[400px] rounded-full bg-[#7E57C2]/8 blur-3xl pointer-events-none" />

        <div className="max-w-6xl mx-auto w-full">
          <div className="grid md:grid-cols-2 gap-12 items-center">
            <div>
              <motion.div variants={fadeUp} custom={0} initial="hidden" animate="visible"
                className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-[#1E88E5]/10 border border-[#1E88E5]/20 text-[#1E88E5] text-xs font-bold font-sans mb-6">
                <span className="w-1.5 h-1.5 rounded-full bg-[#1E88E5] animate-pulse" />
                Live � {(metricsData?.total_data_exact || 3009417).toLocaleString()}+ Data Analisis
              </motion.div>

              <motion.h1 variants={fadeUp} custom={1} initial="hidden" animate="visible"
                className="font-serif font-black text-[clamp(2.8rem,5vw,4.5rem)] text-slate-900 leading-[1.08] tracking-tight mb-6">
                Intelijen Pengadaan{" "}
                <span className="text-transparent bg-clip-text bg-gradient-to-r from-[#1E88E5] to-[#7E57C2]">
                  Transparan &amp; Akurat.
                </span>
              </motion.h1>

              <motion.p variants={fadeUp} custom={2} initial="hidden" animate="visible"
                className="text-slate-500 font-sans text-[clamp(1rem,1.3vw,1.125rem)] leading-relaxed mb-8 max-w-lg">
                Platform PantaUang Kita menyediakan analisis risiko pengadaan barang dan jasa pemerintah menggunakan machine learning mutakhir. Eksplorasi hasil training dan testing klasifikasi risiko dengan mudah.
              </motion.p>

              <motion.div variants={fadeUp} custom={3} initial="hidden" animate="visible" className="flex flex-col sm:flex-row gap-3">
                <Link href="/data" className="flex items-center justify-center gap-2 px-6 py-3.5 bg-slate-900 hover:bg-slate-800 text-white rounded-xl font-bold text-sm transition-all shadow-lg hover:shadow-xl hover:-translate-y-0.5">
                  Mulai Eksplorasi Data <ArrowRight className="w-4 h-4" />
                </Link>
                <Link href="/peta" className="flex items-center justify-center gap-2 px-6 py-3.5 glass border border-slate-200 text-slate-700 hover:bg-white rounded-xl font-bold text-sm transition-all">
                  Lihat Peta Risiko <ExternalLink className="w-4 h-4" />
                </Link>
              </motion.div>
            </div>

            {/* Donut Preview */}
            <motion.div variants={fadeUp} custom={2} initial="hidden" animate="visible"
              className="glass rounded-3xl p-8 shadow-xl border border-white/60 hover-lift">
              <h3 className="font-serif text-lg font-bold text-slate-800 mb-1">Distribusi Kategori Risiko</h3>
              <p className="text-slate-400 text-xs font-sans mb-4">Berdasarkan skor QRLGBM � 3.009.417 paket</p>
              <div className="h-[220px]">
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie data={pieData} innerRadius={65} outerRadius={95} paddingAngle={3} dataKey="value" stroke="none">
                      {pieData.map((entry, i) => <Cell key={i} fill={entry.fill} />)}
                    </Pie>
                    <Tooltip contentStyle={{ borderRadius: '10px', border: 'none', boxShadow: '0 8px 24px rgba(0,0,0,0.1)', fontFamily: 'var(--font-jakarta)' }} />
                  </PieChart>
                </ResponsiveContainer>
              </div>
              <div className="flex flex-wrap gap-3 justify-center mt-2">
                {Object.entries(RISK_COLORS).map(([k, c]) => (
                  <div key={k} className="flex items-center gap-1.5 text-xs font-sans font-bold text-slate-600">
                    <div className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: c }} />
                    {k}
                  </div>
                ))}
              </div>
            </motion.div>
          </div>

          {/* Stat Cards */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mt-12">
            {stats.map((s, i) => (
              <motion.div key={s.label} variants={fadeUp} custom={4 + i} initial="hidden" animate="visible"
                className="glass rounded-2xl p-5 border border-white/60 hover-lift cursor-default">
                <div className={`w-9 h-9 ${s.bg} rounded-xl flex items-center justify-center mb-3`}>
                  <s.icon className="w-4.5 h-4.5" style={{ color: s.color }} />
                </div>
                <div className="text-2xl font-black font-sans text-slate-900 mb-0.5">{s.value}</div>
                <div className="text-xs font-sans font-medium text-slate-400">{s.label}</div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* FEATURE CARDS SECTION */}
      <section className="bg-slate-900 bg-dot-dark px-6 md:px-12 py-20">
        <div className="max-w-6xl mx-auto">
          <motion.h2 initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }}
            className="font-serif font-black text-[clamp(2rem,3vw,3rem)] text-white text-center mb-3">
            Modul Analitik Terintegrasi
          </motion.h2>
          <p className="text-slate-500 font-sans text-center text-sm mb-12 max-w-xl mx-auto">
            Setiap modul dirancang untuk penyelidikan data dari sudut pandang yang berbeda namun saling melengkapi.
          </p>

          <div className="grid md:grid-cols-3 gap-6">
            {[
              { href: "/infografis", icon: BarChart2, color: "#FF8A65", bg: "from-orange-500/20 to-red-500/10", label: "Infografis", desc: "Visualisasi distribusi risiko, tren musiman, dan analisis sektoral dalam format Flourish-inspired yang dinamis." },
              { href: "/peta", icon: MapIcon, color: "#26C6DA", bg: "from-cyan-500/20 to-blue-500/10", label: "Peta Risiko", desc: "Choropleth interaktif 38 Provinsi dengan gradasi warna multi-dimensi berdasarkan kategori risiko yang dipilih." },
              { href: "/data", icon: Database, color: "#7E57C2", bg: "from-purple-500/20 to-indigo-500/10", label: "Data Explorer", desc: "Tabel audit 3 juta+ baris dengan filter majemuk, pagination cepat, dan ekspansi baris akordion granular." },
            ].map((card, i) => (
              <motion.div key={card.href} initial={{ opacity: 0, y: 30 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ delay: i * 0.1 }}>
                <Link href={card.href} className={`group block glass-dark rounded-2xl p-7 border border-white/5 hover:border-white/15 hover-lift transition-all`}>
                  <div className={`w-12 h-12 bg-gradient-to-br ${card.bg} rounded-xl flex items-center justify-center mb-5`}>
                    <card.icon className="w-5 h-5" style={{ color: card.color }} />
                  </div>
                  <h3 className="font-serif font-bold text-xl text-white mb-2">{card.label}</h3>
                  <p className="text-slate-500 text-sm font-sans leading-relaxed">{card.desc}</p>
                  <div className="flex items-center gap-2 mt-5 text-xs font-bold font-sans" style={{ color: card.color }}>
                    Eksplorasi <ArrowRight className="w-3.5 h-3.5 group-hover:translate-x-1 transition-transform" />
                  </div>
                </Link>
              </motion.div>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}
