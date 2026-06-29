"use client";
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
