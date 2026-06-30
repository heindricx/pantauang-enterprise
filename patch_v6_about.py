import os

FRONTEND_APP = r"D:\satdat 2026\sec\pantauang-enterprise\frontend\src\app"

about_tsx = r'''"use client";
import { Server, Target, ArrowRight, BrainCircuit, Database, FileText, Cpu, CheckCircle2 } from "lucide-react";
import { motion } from "framer-motion";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Cell } from "recharts";

export default function AboutClient({ stats }: { stats: any }) {
  const picpTrain = parseFloat(stats?.evaluation_matrix?.PICP?.train || "80.09");
  const picpTest  = parseFloat(stats?.evaluation_matrix?.PICP?.test  || "80.13");
  
  const chartData = [
    { name: "PICP (Train)", value: picpTrain, fill: "#1E88E5" },
    { name: "PICP (Test)",  value: picpTest,  fill: "#4CAF50" }
  ];

  const fadeUp = { hidden: { opacity: 0, y: 20 }, visible: { opacity: 1, y: 0, transition: { duration: 0.5 } } };

  return (
    <div className="min-h-screen font-sans py-12 px-4 md:px-8 bg-grid">
      <div className="max-w-6xl mx-auto space-y-12">
        {/* Header */}
        <motion.div initial="hidden" animate="visible" variants={fadeUp} className="text-center">
          <h1 className="font-serif font-black text-[clamp(2rem,4vw,3.5rem)] tracking-tight mb-3 text-slate-900">
            Metodologi &amp; <span className="text-[#7E57C2]">Model Card</span>
          </h1>
          <p className="text-slate-500 font-sans text-sm max-w-2xl mx-auto leading-relaxed">
            Transparansi penuh atas arsitektur model machine learning yang kami gunakan untuk memproses jutaan data pengadaan. 
            Sistem kami menggabungkan NLP (Natural Language Processing) dan Regresi Kuantil untuk mendeteksi anomali.
          </p>
        </motion.div>

        {/* Pipeline Diagram */}
        <motion.section initial="hidden" whileInView="visible" viewport={{ once: true }} variants={fadeUp} className="glass rounded-3xl p-8 border border-white/60 shadow-lg">
          <h2 className="font-serif text-2xl font-bold text-slate-900 mb-8 text-center">Alur Pipeline Machine Learning</h2>
          
          <div className="flex flex-col lg:flex-row items-center justify-between gap-4">
            {/* Step 1 */}
            <div className="flex-1 bg-white border border-slate-200 rounded-2xl p-5 text-center shadow-sm hover-lift relative z-10 w-full">
              <div className="w-12 h-12 bg-blue-50 text-blue-600 rounded-full flex items-center justify-center mx-auto mb-3">
                <Database className="w-6 h-6" />
              </div>
              <h3 className="font-bold text-slate-800 text-sm mb-1">Data Inaproc</h3>
              <p className="text-xs text-slate-500">3.009.417 baris data mentah</p>
            </div>

            <ArrowRight className="w-6 h-6 text-slate-300 hidden lg:block shrink-0" />
            <div className="h-6 w-[2px] bg-slate-200 lg:hidden" />

            {/* Step 2 */}
            <div className="flex-1 bg-white border border-slate-200 rounded-2xl p-5 text-center shadow-sm hover-lift relative z-10 w-full">
              <div className="w-12 h-12 bg-purple-50 text-purple-600 rounded-full flex items-center justify-center mx-auto mb-3">
                <FileText className="w-6 h-6" />
              </div>
              <h3 className="font-bold text-slate-800 text-sm mb-1">NLP Preprocessing</h3>
              <p className="text-xs text-slate-500">Pembersihan teks agenda</p>
            </div>

            <ArrowRight className="w-6 h-6 text-slate-300 hidden lg:block shrink-0" />
            <div className="h-6 w-[2px] bg-slate-200 lg:hidden" />

            {/* Step 3 */}
            <div className="flex-1 bg-white border border-slate-200 rounded-2xl p-5 text-center shadow-sm hover-lift relative z-10 w-full">
              <div className="w-12 h-12 bg-indigo-50 text-indigo-600 rounded-full flex items-center justify-center mx-auto mb-3">
                <BrainCircuit className="w-6 h-6" />
              </div>
              <h3 className="font-bold text-slate-800 text-sm mb-1">DistilIndoBERT</h3>
              <p className="text-xs text-slate-500">Ekstraksi fitur semantik</p>
            </div>

            <ArrowRight className="w-6 h-6 text-slate-300 hidden lg:block shrink-0" />
            <div className="h-6 w-[2px] bg-slate-200 lg:hidden" />

            {/* Step 4 */}
            <div className="flex-1 bg-white border border-slate-200 rounded-2xl p-5 text-center shadow-sm hover-lift relative z-10 w-full">
              <div className="w-12 h-12 bg-orange-50 text-orange-600 rounded-full flex items-center justify-center mx-auto mb-3">
                <Cpu className="w-6 h-6" />
              </div>
              <h3 className="font-bold text-slate-800 text-sm mb-1">QRLGBM</h3>
              <p className="text-xs text-slate-500">Prediksi Kuantil (P10 & P90)</p>
            </div>

            <ArrowRight className="w-6 h-6 text-slate-300 hidden lg:block shrink-0" />
            <div className="h-6 w-[2px] bg-slate-200 lg:hidden" />

            {/* Step 5 */}
            <div className="flex-1 bg-white border border-green-200 rounded-2xl p-5 text-center shadow-md hover-lift relative z-10 w-full ring-2 ring-green-100">
              <div className="w-12 h-12 bg-green-50 text-green-600 rounded-full flex items-center justify-center mx-auto mb-3">
                <CheckCircle2 className="w-6 h-6" />
              </div>
              <h3 className="font-bold text-green-700 text-sm mb-1">Risk Score</h3>
              <p className="text-xs text-green-600">Skoring Risiko Akhir</p>
            </div>
          </div>
        </motion.section>

        <div className="grid md:grid-cols-2 gap-8">
          {/* Performa Model */}
          <motion.section initial={{ opacity:0, x:-20 }} whileInView={{ opacity:1, x:0 }} viewport={{ once:true }} className="glass rounded-3xl p-8 border border-white/60 shadow-lg flex flex-col">
            <div className="flex items-center gap-3 mb-6">
              <div className="w-10 h-10 rounded-xl bg-blue-100 flex items-center justify-center text-blue-600">
                <Target className="w-5 h-5" />
              </div>
              <div>
                <h2 className="font-serif text-xl font-bold text-slate-900">Performa Model (PICP)</h2>
                <p className="text-xs text-slate-500 font-sans">Prediction Interval Coverage Probability</p>
              </div>
            </div>
            
            <div className="flex-1 w-full h-64 mb-6">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={chartData} margin={{ top: 20, right: 30, left: -20, bottom: 5 }}>
                  <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
                  <XAxis dataKey="name" axisLine={false} tickLine={false} tick={{ fontSize: 12, fill: "#64748b", fontFamily: "var(--font-jakarta)" }} />
                  <YAxis domain={[0, 100]} axisLine={false} tickLine={false} tick={{ fontSize: 12, fill: "#64748b" }} />
                  <Tooltip cursor={{ fill: 'transparent' }} contentStyle={{ borderRadius: "12px", border: "none", boxShadow: "0 10px 25px rgba(0,0,0,0.1)", fontFamily: "var(--font-jakarta)" }} />
                  <Bar dataKey="value" radius={[6, 6, 0, 0]} maxBarSize={60}>
                    {chartData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.fill} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>

            <div className="bg-slate-50 rounded-xl p-4 border border-slate-200">
              <h4 className="text-xs font-bold text-slate-700 uppercase tracking-wider mb-2">Penjelasan Singkat</h4>
              <p className="text-sm text-slate-600 leading-relaxed font-sans">
                <strong>PICP</strong> mengukur persentase data aktual yang jatuh di dalam rentang prediksi (antara P10 dan P90). Nilai idealnya adalah sekitar 80%. 
                Model kami mencapai <strong className="text-blue-600">{picpTrain}%</strong> (Train) dan <strong className="text-green-600">{picpTest}%</strong> (Test), menunjukkan bahwa model sangat akurat dan tidak <em>overfitting</em>.
              </p>
            </div>
          </motion.section>

          {/* Hyperparameter */}
          <motion.section initial={{ opacity:0, x:20 }} whileInView={{ opacity:1, x:0 }} viewport={{ once:true }} className="glass rounded-3xl p-8 border border-white/60 shadow-lg">
            <div className="flex items-center gap-3 mb-6">
              <div className="w-10 h-10 rounded-xl bg-orange-100 flex items-center justify-center text-orange-600">
                <Server className="w-5 h-5" />
              </div>
              <div>
                <h2 className="font-serif text-xl font-bold text-slate-900">Hyperparameter (TPE Optuna)</h2>
                <p className="text-xs text-slate-500 font-sans">Konfigurasi optimal hasil tuning</p>
              </div>
            </div>

            <div className="space-y-6">
              {stats?.optuna_hyperparameters && Object.entries(stats.optuna_hyperparameters).map(([model, params]: any) => (
                <div key={model} className="bg-white rounded-2xl p-5 border border-slate-100 shadow-sm hover-lift">
                  <h3 className="font-sans font-bold text-slate-800 mb-4 flex items-center justify-between">
                    {model}
                    <span className="px-2 py-0.5 bg-slate-100 text-slate-400 text-[10px] rounded-full font-mono">Optimized</span>
                  </h3>
                  <div className="grid grid-cols-2 gap-3">
                    {Object.entries(params).map(([p, v]: any) => (
                      <div key={p} className="bg-slate-50 rounded-lg p-3 border border-slate-100 flex flex-col justify-between">
                        <span className="text-[10px] text-slate-400 font-bold uppercase tracking-wider mb-1">{p}</span>
                        <span className="text-sm font-mono font-black text-slate-700">{v}</span>
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </motion.section>
        </div>
      </div>
    </div>
  );
}
'''
with open(os.path.join(FRONTEND_APP, "about/AboutClient.tsx"), "w", encoding="utf-8") as f:
    f.write(about_tsx)

print("AboutClient updated with Visuals")
