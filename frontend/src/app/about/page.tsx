"use client";
import { useEffect, useState } from "react";
import { ShieldCheck, Server, Key, Target } from "lucide-react";

export default function AboutPage() {
  const [stats, setStats] = useState<any>(null);

  useEffect(() => {
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
    fetch(`${apiUrl}/api/methodology-stats`).then(res => res.json()).then(setStats).catch(console.error);
  }, []);

  return (
    <div className="h-full overflow-auto p-8 md:p-12">
      <div className="max-w-5xl mx-auto space-y-12">
        <header>
          <h1 className="text-3xl font-black uppercase tracking-tight mb-2">Technical Model Card</h1>
          <p className="text-slate-400 font-mono text-sm">Satria Data 2026 / 16_NOCturnal_SEC Documentation</p>
        </header>

        <section className="tech-border rounded-xl p-8">
          <div className="flex items-center gap-2 text-[#52C7D8] mb-6">
            <Target className="w-5 h-5" />
            <h2 className="text-lg font-bold uppercase tracking-wider">Model Evaluation Matrix</h2>
          </div>
          
          <div className="overflow-x-auto">
            <table className="w-full text-left font-mono text-sm">
              <thead className="text-xs uppercase bg-slate-900 text-slate-400">
                <tr>
                  <th className="px-6 py-4">Metric</th>
                  <th className="px-6 py-4">Train</th>
                  <th className="px-6 py-4">Test</th>
                  <th className="px-6 py-4">Notes</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800">
                {stats?.evaluation_matrix && Object.entries(stats.evaluation_matrix).map(([key, val]: any) => (
                  <tr key={key} className="hover:bg-slate-800/50 transition-colors">
                    <td className="px-6 py-4 font-bold text-white">{key}</td>
                    <td className="px-6 py-4 text-green-400">{val.train}</td>
                    <td className="px-6 py-4 text-green-400">{val.test}</td>
                    <td className="px-6 py-4 text-slate-500 text-xs">{val.note}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>

        <section className="tech-border rounded-xl p-8">
          <div className="flex items-center gap-2 text-[#8A63E8] mb-6">
            <Server className="w-5 h-5" />
            <h2 className="text-lg font-bold uppercase tracking-wider">Hyperparameter Transparency (TPE Optuna)</h2>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {stats?.optuna_hyperparameters && Object.entries(stats.optuna_hyperparameters).map(([model, params]: any) => (
              <div key={model} className="bg-slate-900/50 p-6 rounded-lg border border-slate-800">
                <h3 className="text-md font-bold mb-4 font-mono text-white">{model}</h3>
                <ul className="space-y-3 font-mono text-xs">
                  {Object.entries(params).map(([p, v]: any) => (
                    <li key={p} className="flex justify-between items-center border-b border-slate-800 pb-2">
                      <span className="text-slate-400">{p}</span>
                      <span className="text-[#0D5CBD] font-bold bg-blue-950 px-2 py-1 rounded">{v}</span>
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
