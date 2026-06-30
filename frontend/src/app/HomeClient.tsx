"use client";
import { motion, useMotionValue, useTransform, animate } from "framer-motion";
import { Database, AlertOctagon, TrendingUp, ChevronRight, ArrowRight, ExternalLink, Map as MapIcon, BarChart2, Zap } from "lucide-react";
import Link from "next/link";
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from "recharts";
import { useEffect } from "react";

const RISK_COLORS = { Anomali: "#FF5722", Tinggi: "#FF8A65", Sedang: "#FFCA28", Rendah: "#4CAF50" };
const TOTAL = 3009417;

const fadeUp = { hidden: { opacity: 0, y: 30 }, visible: (i: number) => ({ opacity: 1, y: 0, transition: { delay: i * 0.1, duration: 0.5 } }) };

function AnimatedNumber({ value, formatString = false }: { value: number, formatString?: boolean }) {
  const count = useMotionValue(0);
  const rounded = useTransform(count, Math.round);
  
  useEffect(() => {
    const animation = animate(count, value, { duration: 2, ease: "easeOut" });
    return animation.stop;
  }, [value, count]);

  if (formatString) {
    // specific to our string values like Rp 642,2T or 7,47%
    // actually, we will just use a simpler approach for string values, 
    // or just let them be numbers.
  }
  
  // Custom display for specific values
  return <motion.span>{useTransform(rounded, (latest) => latest.toLocaleString("id-ID"))}</motion.span>;
}

// Custom Counter for strings
function AnimatedCounterString({ value, prefix = "", suffix = "", decimal = 0, divisor = 1 }: { value: number, prefix?: string, suffix?: string, decimal?: number, divisor?: number }) {
  const count = useMotionValue(0);
  
  useEffect(() => {
    const animation = animate(count, value, { duration: 2, ease: "easeOut" });
    return animation.stop;
  }, [value, count]);

  const display = useTransform(count, (latest) => {
    return prefix + (latest / divisor).toFixed(decimal).replace(".", ",") + suffix;
  });

  return <motion.span>{display}</motion.span>;
}

export default function HomeClient({ tickerData, metricsData }: { tickerData: any; metricsData: any }) {
  const anomali = 74900;
  const tinggi  = 149801;
  const sedang  = 74900;
  const rendah  = 2709816;

  const pieData = [
    { name: "Anomali", value: anomali, fill: RISK_COLORS.Anomali },
    { name: "Tinggi",  value: tinggi,  fill: RISK_COLORS.Tinggi  },
    { name: "Sedang",  value: sedang,  fill: RISK_COLORS.Sedang  },
    { name: "Rendah",  value: rendah,  fill: RISK_COLORS.Rendah  },
  ];

  const tickerItems = tickerData?.length > 0 ? tickerData : [
    { score: 99.87, agenda: "Pengadaan Alat Kesehatan RSUD...", pagu: 12400000000 },
    { score: 98.54, agenda: "Pembangunan Jalan Lingkar Luar...", pagu: 8700000000 },
    { score: 97.12, agenda: "Pengadaan Kendaraan Dinas...",     pagu: 5300000000 },
  ];

  return (
    <div className="w-full font-sans">
      {/* TICKER */}
      <div className="h-9 bg-white/80 backdrop-blur border-b border-slate-200/60 flex items-center overflow-hidden shrink-0">
        <div className="flex items-center px-4 bg-[#FF5722]/10 h-full border-r border-[#FF5722]/20 gap-2 shrink-0">
          <Zap className="w-3.5 h-3.5 text-[#FF5722] fill-current" />
          <span className="text-[10px] font-bold text-[#FF5722] uppercase tracking-widest whitespace-nowrap font-sans">Live Anomalies</span>
        </div>
        <div className="flex-1 overflow-hidden relative h-full">
          <div className="animate-[marquee_25s_linear_infinite] whitespace-nowrap flex gap-8 absolute items-center h-full px-4">
            {tickerItems.map((t: any, i: number) => (
              <span key={i} className="text-slate-600 text-xs font-sans">
                <span className="text-[#FF5722] font-bold font-mono">[{(t.score || t.skor_risiko || 0).toFixed(2)}]</span>
                {" "}{(t.agenda || "").substring(0, 45)}{(t.agenda || "").length > 45 ? "..." : ""}
                {" "}<span className="text-slate-400">Rp {((t.pagu || 0) / 1e9).toFixed(1)}M</span>
              </span>
            ))}
          </div>
        </div>
      </div>

      {/* HERO */}
      <section className="relative min-h-[90vh] flex items-center justify-center px-6 md:px-12 py-20 overflow-hidden">
        <div className="absolute top-[-10%] left-[-5%] w-[500px] h-[500px] rounded-full bg-[#1E88E5]/8 blur-3xl pointer-events-none" />
        <div className="absolute bottom-[-10%] right-[-5%] w-[400px] h-[400px] rounded-full bg-[#7E57C2]/8 blur-3xl pointer-events-none" />

        <div className="max-w-6xl mx-auto w-full">
          <div className="grid md:grid-cols-2 gap-12 items-center">
            <div>
              <motion.div variants={fadeUp} custom={0} initial="hidden" animate="visible"
                className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-[#1E88E5]/10 border border-[#1E88E5]/20 text-[#1E88E5] text-xs font-bold font-sans mb-6">
                <span className="w-1.5 h-1.5 rounded-full bg-[#1E88E5] animate-pulse" />
                Live — 3.009.417 Data Dianalisis
              </motion.div>

              <motion.h1 variants={fadeUp} custom={1} initial="hidden" animate="visible"
                className="font-serif font-black text-[clamp(2.5rem,5vw,4.5rem)] text-slate-900 leading-[1.1] tracking-tight">
                Selamat datang di <span className="text-transparent bg-clip-text bg-gradient-to-r from-[#1E88E5] to-[#42A5F5]">PantaUang</span>
              </motion.h1>

              <motion.p variants={fadeUp} custom={2} initial="hidden" animate="visible"
                className="text-slate-500 font-sans text-lg md:text-xl max-w-3xl mx-auto leading-relaxed mb-8">
                Platform PantaUang menyediakan analisis risiko pengadaan barang dan jasa pemerintah menggunakan metode machine learning.
              </motion.p>

              <motion.div variants={fadeUp} custom={3} initial="hidden" animate="visible" className="flex flex-col sm:flex-row items-center gap-4 pt-4">
                <Link href="/data" className="group px-8 py-4 bg-slate-900 text-white rounded-full font-bold font-sans hover:bg-slate-800 transition-all flex items-center gap-2 shadow-lg hover:shadow-xl hover:-translate-y-1">
                  Cek Data Risiko <ChevronRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
                </Link>
                <Link href="/peta" className="px-8 py-4 bg-white text-slate-700 rounded-full font-bold font-sans border border-slate-200 hover:border-slate-300 hover:bg-slate-50 transition-all shadow-sm hover:-translate-y-1">
                  Cek Peta Risiko
                </Link>
              </motion.div>
            </div>

            {/* Smooth Reveal Pie Chart */}
            <motion.div variants={fadeUp} custom={2} initial={{ opacity: 0, scale: 0.9 }} animate={{ opacity: 1, scale: 1, transition: { duration: 0.8, delay: 0.2, ease: "easeOut" } }}
              className="glass rounded-3xl p-8 shadow-xl border border-white/60 hover-lift">
              <h3 className="font-serif text-lg font-bold text-slate-800 mb-1">Distribusi Kategori Risiko</h3>
              <p className="text-slate-400 text-xs font-sans mb-4">Berdasarkan skor QRLGBM — 3.009.417 paket</p>
              <div className="h-[200px]">
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie data={pieData} innerRadius={60} outerRadius={90} paddingAngle={3} dataKey="value" stroke="none" isAnimationActive={true} animationDuration={1500} animationEasing="ease-out">
                      {pieData.map((entry, i) => <Cell key={i} fill={entry.fill} />)}
                    </Pie>
                    <Tooltip contentStyle={{ borderRadius: "10px", border: "none", boxShadow: "0 8px 24px rgba(0,0,0,0.1)", fontFamily: "var(--font-jakarta)", fontSize: "12px" }}
                      formatter={(val: any, name: any) => [`${val.toLocaleString("id-ID")} paket`, name]} />
                  </PieChart>
                </ResponsiveContainer>
              </div>
              <div className="flex flex-wrap gap-x-4 gap-y-2 justify-center mt-2">
                {Object.entries(RISK_COLORS).map(([k, c]) => (
                  <div key={k} className="flex items-center gap-1.5 text-xs font-sans font-bold text-slate-600">
                    <div className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: c }} />
                    {k}
                  </div>
                ))}
              </div>
            </motion.div>
          </div>

          {/* Animated Stat Cards */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mt-12">
            <motion.div variants={fadeUp} custom={4} initial="hidden" animate="visible" className="glass rounded-2xl p-5 border border-white/60 hover-lift cursor-default relative overflow-hidden group">
              <div className="absolute top-0 right-0 w-24 h-24 bg-blue-500/5 rounded-full blur-2xl group-hover:bg-blue-500/10 transition-colors" />
              <div className="w-9 h-9 bg-blue-50 rounded-xl flex items-center justify-center mb-3 text-[#1E88E5]">
                <Database className="w-4 h-4" />
              </div>
              <div className="text-2xl font-black font-sans text-slate-900 mb-0.5"><AnimatedNumber value={3009417} /></div>
              <div className="text-xs font-sans font-medium text-slate-400">Data Dianalisis</div>
            </motion.div>
            
            <motion.div variants={fadeUp} custom={5} initial="hidden" animate="visible" className="glass rounded-2xl p-5 border border-white/60 hover-lift cursor-default relative overflow-hidden group">
              <div className="absolute top-0 right-0 w-24 h-24 bg-purple-500/5 rounded-full blur-2xl group-hover:bg-purple-500/10 transition-colors" />
              <div className="w-9 h-9 bg-purple-50 rounded-xl flex items-center justify-center mb-3 text-[#7E57C2]">
                <TrendingUp className="w-4 h-4" />
              </div>
              <div className="text-2xl font-black font-sans text-slate-900 mb-0.5"><AnimatedCounterString value={642.2} prefix="Rp " suffix="T" decimal={1} /></div>
              <div className="text-xs font-sans font-medium text-slate-400">Total Anggaran</div>
            </motion.div>

            <motion.div variants={fadeUp} custom={6} initial="hidden" animate="visible" className="glass rounded-2xl p-5 border border-white/60 hover-lift cursor-default relative overflow-hidden group">
              <div className="absolute top-0 right-0 w-24 h-24 bg-orange-500/5 rounded-full blur-2xl group-hover:bg-orange-500/10 transition-colors" />
              <div className="w-9 h-9 bg-red-50 rounded-xl flex items-center justify-center mb-3 text-[#FF5722]">
                <AlertOctagon className="w-4 h-4" />
              </div>
              <div className="text-2xl font-black font-sans text-slate-900 mb-0.5"><AnimatedCounterString value={7.47} suffix="%" decimal={2} /></div>
              <div className="text-xs font-sans font-medium text-slate-400">Rasio Anomali</div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* FEATURE CARDS with Visual Miniatures */}
      <section className="bg-slate-900 bg-dot-dark px-6 md:px-12 py-20">
        <div className="max-w-6xl mx-auto">
            <motion.h2 initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }}
              className="font-serif font-black text-[clamp(2rem,3vw,3rem)] text-white text-center mb-3">
              Data Hasil Analisis
            </motion.h2>
            <p className="text-slate-500 font-sans text-center text-sm mb-12 max-w-xl mx-auto">
              Data hasil analisis disajikan dalam bentuk infografis, peta risiko, dan data tabel.
            </p>

          <div className="grid md:grid-cols-3 gap-6">
            <motion.div initial={{ opacity: 0, y: 30 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ delay: 0 }}>
              <Link href="/infografis" className="group block glass-dark rounded-2xl p-7 border border-white/5 hover:border-white/15 hover-lift transition-all relative overflow-hidden h-full flex flex-col">
                <div className="absolute -right-10 -top-10 w-40 h-40 bg-gradient-to-br from-orange-500/10 to-red-500/5 rounded-full blur-3xl pointer-events-none" />
                <div className="w-12 h-12 bg-gradient-to-br from-orange-500/20 to-red-500/10 rounded-xl flex items-center justify-center mb-5 shrink-0">
                  <BarChart2 className="w-5 h-5 text-[#FF8A65]" />
                </div>
                <h3 className="font-serif font-bold text-xl text-white mb-2">Infografis</h3>
                <p className="text-slate-500 text-sm font-sans leading-relaxed mb-6 flex-1">Visualisasi distribusi risiko, tren musiman, dan analisis sektoral secara dinamis.</p>
                {/* Visual Thumbnail */}
                <div className="h-20 w-full rounded-xl bg-white/5 border border-white/10 p-2 flex items-end gap-1 justify-center overflow-hidden">
                  <div className="w-6 bg-orange-400/40 rounded-t-sm" style={{ height: "40%" }} />
                  <div className="w-6 bg-orange-500/60 rounded-t-sm" style={{ height: "65%" }} />
                  <div className="w-6 bg-red-500/80 rounded-t-sm" style={{ height: "90%" }} />
                  <div className="w-6 bg-orange-400/50 rounded-t-sm" style={{ height: "55%" }} />
                </div>
                <div className="flex items-center gap-2 mt-5 text-xs font-bold font-sans text-[#FF8A65]">
                  Eksplorasi <ArrowRight className="w-3.5 h-3.5 group-hover:translate-x-1 transition-transform" />
                </div>
              </Link>
            </motion.div>

            <motion.div initial={{ opacity: 0, y: 30 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ delay: 0.1 }}>
              <Link href="/peta" className="group block glass-dark rounded-2xl p-7 border border-white/5 hover:border-white/15 hover-lift transition-all relative overflow-hidden h-full flex flex-col">
                <div className="absolute -right-10 -top-10 w-40 h-40 bg-gradient-to-br from-cyan-500/10 to-blue-500/5 rounded-full blur-3xl pointer-events-none" />
                <div className="w-12 h-12 bg-gradient-to-br from-cyan-500/20 to-blue-500/10 rounded-xl flex items-center justify-center mb-5 shrink-0">
                  <MapIcon className="w-5 h-5 text-[#26C6DA]" />
                </div>
                <h3 className="font-serif font-bold text-xl text-white mb-2">Peta Risiko</h3>
                <p className="text-slate-500 text-sm font-sans leading-relaxed mb-6 flex-1">Choropleth interaktif 38 Provinsi dengan gradasi warna berdasarkan kategori risiko.</p>
                {/* Visual Thumbnail */}
                <div className="h-20 w-full rounded-xl bg-white/5 border border-white/10 p-2 flex items-center justify-center overflow-hidden relative">
                  <div className="w-20 h-12 rounded-full border border-cyan-500/30 bg-cyan-500/10 absolute -rotate-12" />
                  <div className="w-3 h-3 rounded-full bg-cyan-400 absolute ml-4 mb-2 animate-pulse" />
                  <div className="w-2 h-2 rounded-full bg-blue-400 absolute mr-6 mt-4" />
                </div>
                <div className="flex items-center gap-2 mt-5 text-xs font-bold font-sans text-[#26C6DA]">
                  Eksplorasi <ArrowRight className="w-3.5 h-3.5 group-hover:translate-x-1 transition-transform" />
                </div>
              </Link>
            </motion.div>

            <motion.div initial={{ opacity: 0, y: 30 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ delay: 0.2 }}>
              <Link href="/data" className="group block glass-dark rounded-2xl p-7 border border-white/5 hover:border-white/15 hover-lift transition-all relative overflow-hidden h-full flex flex-col">
                <div className="absolute -right-10 -top-10 w-40 h-40 bg-gradient-to-br from-purple-500/10 to-indigo-500/5 rounded-full blur-3xl pointer-events-none" />
                <div className="w-12 h-12 bg-gradient-to-br from-purple-500/20 to-indigo-500/10 rounded-xl flex items-center justify-center mb-5 shrink-0">
                  <Database className="w-5 h-5 text-[#7E57C2]" />
                </div>
                <h3 className="font-serif font-bold text-xl text-white mb-2">Data Explorer</h3>
                <p className="text-slate-500 text-sm font-sans leading-relaxed mb-6 flex-1">Tabel audit 3.009.417 paket dengan filter majemuk, pagination, dan detail akordion.</p>
                {/* Visual Thumbnail */}
                <div className="h-20 w-full rounded-xl bg-white/5 border border-white/10 p-3 flex flex-col gap-1.5 justify-center overflow-hidden">
                  <div className="w-full h-2 bg-white/10 rounded-full" />
                  <div className="w-3/4 h-2 bg-white/5 rounded-full" />
                  <div className="w-5/6 h-2 bg-white/5 rounded-full" />
                  <div className="w-full h-2 bg-purple-500/20 rounded-full mt-1" />
                </div>
                <div className="flex items-center gap-2 mt-5 text-xs font-bold font-sans text-[#7E57C2]">
                  Eksplorasi <ArrowRight className="w-3.5 h-3.5 group-hover:translate-x-1 transition-transform" />
                </div>
              </Link>
            </motion.div>
          </div>
        </div>
      </section>
    </div>
  );
}
