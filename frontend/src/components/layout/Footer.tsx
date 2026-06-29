export function Footer() {
  return (
    <footer className="w-full bg-slate-900 text-slate-400 py-8 px-6 mt-12 font-sans shrink-0 border-t border-slate-800">
      <div className="max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-center gap-4">
        <div>
          <span className="font-serif font-black text-xl tracking-tighter text-white">
            Panta<span className="text-[#1E88E5]">Uang</span>
          </span>
          <p className="text-xs mt-2 max-w-sm leading-relaxed">
            Platform intelijen pengadaan barang dan jasa menggunakan machine learning untuk mendeteksi anomali secara sistematis dan transparan.
          </p>
        </div>
        <div className="text-left md:text-right text-xs space-y-1">
          <p className="text-slate-300 font-bold">Data Attribution & Methodology</p>
          <p>Sumber Data: Inaproc & Sistem Informasi RUP LKPP</p>
          <p>Model Baseline: Distil-IndoBERT + QRLGBM</p>
          <p className="mt-4 text-slate-600">&copy; {new Date().getFullYear()} Satria Data Enterprise. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
}
