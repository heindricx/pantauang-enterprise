import Link from "next/link";

export function Footer() {
  return (
    <footer className="w-full bg-slate-900 text-slate-400 border-t border-slate-800 font-sans">
      <div className="max-w-7xl mx-auto px-6 py-10 grid grid-cols-1 md:grid-cols-3 gap-8">
        <div>
          <span className="font-serif font-black text-2xl tracking-tight text-white block mb-3">
            Panta<span className="text-[#1E88E5]">Uang</span>
          </span>
          <p className="text-xs leading-relaxed text-slate-500 max-w-xs">
            Platform intelijen pengadaan publik berbasis machine learning untuk deteksi anomali secara sistematis dan transparan.
          </p>
        </div>
        <div>
          <h4 className="text-slate-300 font-bold text-xs uppercase tracking-wider mb-4">Sumber Data</h4>
          <ul className="space-y-2 text-xs text-slate-500">
            <li><a href="https://inaproc.id" target="_blank" rel="noopener noreferrer" className="hover:text-slate-200 transition-colors">Inaproc — Sistem Pengadaan Nasional</a></li>
            <li><a href="https://e-rencana.lkpp.go.id" target="_blank" rel="noopener noreferrer" className="hover:text-slate-200 transition-colors">Sistem Informasi RUP — LKPP</a></li>
            <li><span className="text-slate-600">Data periode 2023–2024</span></li>
          </ul>
        </div>
        <div>
          <h4 className="text-slate-300 font-bold text-xs uppercase tracking-wider mb-4">Model & Teknologi</h4>
          <ul className="space-y-2 text-xs text-slate-500">
            <li>Distil-IndoBERT NLP Pipeline</li>
            <li>Quantile Regression LightGBM (QRLGBM)</li>
            <li>Optuna Hyperparameter Optimization</li>
          </ul>
        </div>
      </div>
      <div className="border-t border-slate-800 px-6 py-4 text-center text-xs text-slate-600">
        &copy; {new Date().getFullYear()} PantaUang Kita · Satria Data Enterprise 2026 · All rights reserved.
      </div>
    </footer>
  );
}
