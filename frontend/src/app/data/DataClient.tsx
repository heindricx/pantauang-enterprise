"use client";
import React, { useState, useEffect, useCallback } from "react";
import { ChevronDown, ChevronRight, Search, Download, X, ArrowUpDown, ArrowUp, ArrowDown, ChevronLeft } from "lucide-react";
import { ChevronRight as ChRight } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

// ─── Types ────────────────────────────────────────────────────────────
type Row = {
  id: string; agenda: string; lembaga: string; satker?: string;
  provinsi?: string; kota?: string; metode?: string; jenis?: string;
  pagu: number; p10?: number; p90?: number; fraud_value?: number;
  skor_risiko: number; kategori_risiko?: string;
};
type Filters = { risiko: string; provinsi: string; metode: string; search: string };
type Sort    = { col: string; dir: "asc" | "desc" };

const PILL: Record<string, string> = {
  Anomali: "bg-red-100 text-red-700 border-red-200",
  Tinggi:  "bg-orange-100 text-orange-700 border-orange-200",
  Sedang:  "bg-yellow-100 text-yellow-700 border-yellow-200",
  Rendah:  "bg-green-100 text-green-700 border-green-200",
};
const BORDER: Record<string, string> = {
  Anomali: "border-l-[#FF5722]", Tinggi: "border-l-[#FF8A65]",
  Sedang:  "border-l-amber-400",  Rendah: "border-l-green-400",
};

function classify(s: number) {
  if (s >= 90.16) return "Anomali";
  if (s >= 23.75) return "Tinggi";
  if (s > 0)      return "Sedang";
  return "Rendah";
}

// ─── Async Data Hook (client-side fetch) ─────────────────────────────
function useData(pageSize: number, filters: Filters, sort: Sort) {
  const [rows, setRows]     = useState<Row[]>([]);
  const [total, setTotal]   = useState(0);
  const [pages, setPages]   = useState(1);
  const [page, setPage]     = useState(1);
  const [loading, setLoad]  = useState(false);
  const [error, setError]   = useState(false);

  const fetch_ = useCallback(async (p: number) => {
    setLoad(true);
    setError(false);
    try {
      const base = process.env.NEXT_PUBLIC_API_URL || "https://heindricx-pantauang-backend.hf.space";
      const q = new URLSearchParams({
        limit: String(pageSize),
        offset: String((p - 1) * pageSize),
        sort_by:  sort.col,
        sort_dir: sort.dir,
      });
      if (filters.search)   q.set("search",   filters.search);
      if (filters.risiko)   q.set("risiko",   filters.risiko);
      if (filters.provinsi) q.set("provinsi", filters.provinsi);
      if (filters.metode)   q.set("metode",   filters.metode);

      const controller = new AbortController();
      const timeout = setTimeout(() => controller.abort(), 60000); // 60s timeout for Hugging Face cold start
      const res = await fetch(`${base}/procurement?${q}`, { signal: controller.signal, cache: "no-store" });
      clearTimeout(timeout);
      if (!res.ok) throw new Error("bad response");
      const json = await res.json();
      const data = (json.data || []).map((r: Row) => ({
        ...r, kategori_risiko: r.kategori_risiko || classify(r.skor_risiko)
      }));
      setRows(data);
      setTotal(json.total || 3009417);
      setPages(json.total_pages || 1);
    } catch {
      setError(true);
      setRows([]);
      setTotal(0);
      setPages(1);
    } finally {
      setLoad(false);
    }
  }, [pageSize, filters, sort]);

  useEffect(() => { setPage(1); }, [filters, sort, pageSize]);
  useEffect(() => { fetch_(page); }, [page, fetch_]);

  return { rows, total, pages, page, setPage, loading, error };
}

// ─── Pagination ───────────────────────────────────────────────────────
function Pagination({ page, pages, onChange }: { page: number; pages: number; onChange: (p: number) => void }) {
  const nums: (number | string)[] = [];
  if (pages <= 9) {
    for (let i = 1; i <= pages; i++) nums.push(i);
  } else {
    [1,2,3].forEach(n => nums.push(n));
    if (page > 5) nums.push("...");
    for (let i = Math.max(4, page - 1); i <= Math.min(pages - 3, page + 1); i++) nums.push(i);
    if (page < pages - 4) nums.push("...");
    [pages-2, pages-1, pages].forEach(n => { if (!nums.includes(n)) nums.push(n); });
  }
  return (
    <div className="flex items-center justify-between px-4 py-3 border-t border-slate-100 bg-white/70 backdrop-blur flex-wrap gap-3">
      <span className="text-xs text-slate-400 font-sans">Hal. {page.toLocaleString("id-ID")} / {pages.toLocaleString("id-ID")}</span>
      <div className="flex items-center gap-1 flex-wrap">
        <button disabled={page <= 1} onClick={() => onChange(page - 1)} className="p-1.5 rounded-lg hover:bg-slate-100 disabled:opacity-30">
          <ChevronLeft className="w-4 h-4 text-slate-500" />
        </button>
        {nums.map((n, i) => n === "..." ? (
          <span key={`e${i}`} className="px-1 text-slate-400 text-xs">...</span>
        ) : (
          <button key={`${n}_${i}`} onClick={() => onChange(n as number)}
            className={`min-w-[28px] h-7 rounded-lg text-xs font-bold px-1 transition-all ${page === n ? "bg-slate-900 text-white" : "text-slate-500 hover:bg-slate-100"}`}>
            {(n as number).toLocaleString("id-ID")}
          </button>
        ))}
        <button disabled={page >= pages} onClick={() => onChange(page + 1)} className="p-1.5 rounded-lg hover:bg-slate-100 disabled:opacity-30">
          <ChRight className="w-4 h-4 text-slate-500" />
        </button>
      </div>
    </div>
  );
}

// ─── Row Detail ───────────────────────────────────────────────────────
function Detail({ row }: { row: Row }) {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 p-5 bg-slate-50/80 border-t border-slate-100">
      {([
        ["Nama Paket Lengkap", row.agenda],
        ["Instansi / Lembaga", row.lembaga],
        ["Satker", row.satker || "—"],
        ["Provinsi", row.provinsi || "—"],
        ["Kota / Kabupaten", row.kota || "—"],
        ["Metode Pengadaan", row.metode || "—"],
        ["Jenis Pengadaan", row.jenis || "—"],
        ["Pagu Anggaran", `Rp ${(row.pagu / 1e6).toFixed(2)} Juta`],
        ["P10 (Quantile 10%)", row.p10 != null ? row.p10.toFixed(6) : "—"],
        ["P90 (Quantile 90%)", row.p90 != null ? row.p90.toFixed(6) : "—"],
        ["Fraud Value", row.fraud_value != null ? row.fraud_value.toFixed(6) : "—"],
        ["Skor Risiko QRLGBM", row.skor_risiko.toFixed(6)],
        ["Kategori Risiko", row.kategori_risiko || "—"],
        ["ID Paket", row.id],
      ] as [string, string][]).map(([label, val]) => (
        <div key={label}>
          <div className="text-[10px] text-slate-400 font-bold uppercase tracking-wider font-sans mb-0.5">{label}</div>
          <div className="text-sm text-slate-800 font-sans font-medium break-words">{val}</div>
        </div>
      ))}
    </div>
  );
}

// ─── Main ─────────────────────────────────────────────────────────────
export default function DataClient({ filterOptions }: { filterOptions?: any }) {
  const [pageSize, setPs]   = useState(25);
  const [filters, setF]     = useState<Filters>({ risiko:"", provinsi:"", metode:"", search:"" });
  const [sort, setSort]     = useState<Sort>({ col:"skor_risiko", dir:"desc" });
  const [expanded, setExp]  = useState<Set<string>>(new Set());
  const [searchIn, setSIn]  = useState("");

  const { rows, total, pages, page, setPage, loading, error } = useData(pageSize, filters, sort);

  const toggleSort = (col: string) => setSort(s => s.col === col ? { col, dir: s.dir === "desc" ? "asc" : "desc" } : { col, dir: "desc" });
  const toggleRow  = (id: string)  => setExp(prev => { const n = new Set(prev); n.has(id) ? n.delete(id) : n.add(id); return n; });

  const SIcon = ({ col }: { col: string }) => {
    if (sort.col !== col) return <ArrowUpDown className="w-3 h-3 text-slate-300" />;
    return sort.dir === "desc" ? <ArrowDown className="w-3 h-3 text-slate-600" /> : <ArrowUp className="w-3 h-3 text-slate-600" />;
  };

  const pOpts = filterOptions?.provinsi?.slice(0, 50) || [];
  const mOpts = filterOptions?.metode || [];
  const hasF  = !!(filters.risiko || filters.provinsi || filters.metode || filters.search);

  return (
    <div className="min-h-screen font-sans py-8 px-4 md:px-8 bg-grid">
      <div className="max-w-7xl mx-auto">
        <div className="mb-6">
          <h1 className="font-serif font-black text-[clamp(1.8rem,3vw,2.8rem)] text-slate-900">Audit-Ready Data Explorer</h1>
          <p className="text-slate-500 text-sm font-sans mt-1">
            {loading ? (
              <span className="inline-flex items-center gap-1.5 text-slate-400">
                <span className="w-1.5 h-1.5 rounded-full bg-[#1E88E5] animate-pulse" />
                Memfilter 3.009.417 baris data...
              </span>
            ) : error ? (
              <span className="text-orange-500">Gagal mengambil data dari server TiDB. Server mungkin sedang cold-start (butuh ~30 detik). Silakan refresh halaman.</span>
            ) : (
              <><span className="font-bold text-slate-700">{total.toLocaleString("id-ID")}</span> baris ditemukan</>
            )}
          </p>
        </div>

        {/* FILTER BAR */}
        <div className="glass rounded-2xl border border-white/60 p-4 mb-4 shadow-sm">
          <div className="flex flex-col sm:flex-row flex-wrap gap-3">
            <div className="relative flex-1 min-w-[180px]">
              <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
              <input value={searchIn} onChange={e => setSIn(e.target.value)}
                onKeyDown={e => e.key === "Enter" && setF(f => ({...f, search: searchIn}))}
                placeholder="Cari nama paket atau ID..."
                className="w-full pl-9 pr-4 py-2.5 bg-white/80 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-[#1E88E5]/30 focus:border-[#1E88E5] transition-all font-sans" />
            </div>
            <select value={filters.risiko} onChange={e => setF(f => ({...f, risiko:e.target.value}))}
              className="py-2.5 px-3 bg-white/80 border border-slate-200 rounded-xl text-sm font-sans focus:outline-none focus:ring-2 focus:ring-[#1E88E5]/30">
              <option value="">Semua Risiko</option>
              {["Rendah","Sedang","Tinggi","Anomali"].map(r => <option key={r} value={r}>{r}</option>)}
            </select>
            <select value={filters.provinsi} onChange={e => setF(f => ({...f, provinsi:e.target.value}))}
              className="py-2.5 px-3 bg-white/80 border border-slate-200 rounded-xl text-sm font-sans focus:outline-none focus:ring-2 focus:ring-[#1E88E5]/30">
              <option value="">Semua Provinsi</option>
              {pOpts.map((p: string) => <option key={p} value={p}>{p}</option>)}
            </select>
            <select value={filters.metode} onChange={e => setF(f => ({...f, metode:e.target.value}))}
              className="py-2.5 px-3 bg-white/80 border border-slate-200 rounded-xl text-sm font-sans focus:outline-none focus:ring-2 focus:ring-[#1E88E5]/30">
              <option value="">Semua Metode</option>
              {mOpts.map((m: string) => <option key={m} value={m}>{m}</option>)}
            </select>
            <button onClick={() => setF(f => ({...f, search: searchIn}))}
              className="px-5 py-2.5 bg-slate-900 text-white text-sm font-bold rounded-xl hover:bg-slate-800 transition-all shadow-sm font-sans">
              Cari
            </button>
            {hasF && (
              <button onClick={() => { setF({ risiko:"", provinsi:"", metode:"", search:"" }); setSIn(""); }}
                className="flex items-center gap-1.5 px-3 py-2.5 text-sm text-slate-500 hover:text-slate-800 rounded-xl hover:bg-slate-100 transition-all font-sans">
                <X className="w-3.5 h-3.5" /> Reset
              </button>
            )}
          </div>
        </div>

        {/* TABLE */}
        <div className="glass rounded-2xl border border-white/60 shadow-md overflow-hidden">
          {/* Table Controls */}
          <div className="flex items-center justify-between px-4 py-3 border-b border-slate-100 bg-white/50 gap-3 flex-wrap">
            <div className="flex items-center gap-2 text-xs font-sans text-slate-500">
              Tampilkan
              <select value={pageSize} onChange={e => setPs(Number(e.target.value))}
                className="border border-slate-200 rounded-lg px-2 py-1 bg-white text-slate-700 font-bold focus:outline-none">
                {[10, 25, 50, 100].map(n => <option key={n} value={n}>{n}</option>)}
              </select>
              baris/halaman
            </div>
            <button className="flex items-center gap-2 px-3 py-1.5 text-xs font-bold text-slate-500 hover:text-slate-800 border border-slate-200 rounded-lg hover:bg-slate-50 font-sans">
              <Download className="w-3.5 h-3.5" /> Export CSV
            </button>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead className="bg-slate-50/80 border-b border-slate-200">
                <tr>
                  <th className="w-10 px-3 py-3" />
                  <th className="px-4 py-3 text-left text-xs font-bold font-sans text-slate-500 uppercase tracking-wider">Nama Paket</th>
                  <th className="px-4 py-3 text-left text-xs font-bold font-sans text-slate-500 uppercase tracking-wider whitespace-nowrap">Lembaga</th>
                  <th className="px-4 py-3 text-left text-xs font-bold font-sans text-slate-500 uppercase tracking-wider hidden md:table-cell whitespace-nowrap">Provinsi</th>
                  <th className="px-4 py-3 cursor-pointer select-none whitespace-nowrap" onClick={() => toggleSort("pagu")}>
                    <div className="flex items-center gap-1 text-xs font-bold font-sans text-slate-500 uppercase tracking-wider">Pagu <SIcon col="pagu" /></div>
                  </th>
                  <th className="px-4 py-3 cursor-pointer select-none whitespace-nowrap" onClick={() => toggleSort("skor_risiko")}>
                    <div className="flex items-center gap-1 text-xs font-bold font-sans text-slate-500 uppercase tracking-wider">R-Score <SIcon col="skor_risiko" /></div>
                  </th>
                  <th className="px-4 py-3 text-left text-xs font-bold font-sans text-slate-500 uppercase tracking-wider whitespace-nowrap">Kategori</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {loading ? (
                  Array.from({ length: 8 }).map((_, i) => (
                    <tr key={i} className="animate-pulse">
                      {Array.from({ length: 7 }).map((_, j) => (
                        <td key={j} className="px-4 py-3"><div className="h-4 bg-slate-100 rounded" /></td>
                      ))}
                    </tr>
                  ))
                ) : error ? (
                  <tr>
                    <td colSpan={7} className="py-16 text-center">
                      <div className="flex flex-col items-center gap-3 text-slate-400 font-sans text-sm">
                        <div className="w-12 h-12 rounded-full bg-slate-100 flex items-center justify-center">
                          <Search className="w-5 h-5 text-slate-300" />
                        </div>
                        <p className="font-bold text-slate-600">Gagal Memuat Data</p>
                        <p className="text-xs max-w-xs text-center">Koneksi ke database TiDB terputus atau *timeout*. Silakan muat ulang (refresh) halaman ini.</p>
                      </div>
                    </td>
                  </tr>
                ) : rows.length === 0 ? (
                  <tr><td colSpan={7} className="py-12 text-center text-slate-400 text-sm font-sans">Tidak ada data untuk filter ini.</td></tr>
                ) : rows.map(row => {
                  const cat  = row.kategori_risiko || "Rendah";
                  const isExp = expanded.has(row.id);
                  return (
                    <React.Fragment key={row.id}>
                      <tr className={`border-l-4 ${BORDER[cat] || "border-l-slate-200"} hover:bg-slate-50/80 transition-colors cursor-default`}>
                        <td className="px-3 py-3 text-center">
                          <button onClick={() => toggleRow(row.id)}
                            className="w-6 h-6 flex items-center justify-center rounded-md hover:bg-slate-200 transition-colors">
                            {isExp ? <ChevronDown className="w-3.5 h-3.5 text-slate-500" /> : <ChevronRight className="w-3.5 h-3.5 text-slate-400" />}
                          </button>
                        </td>
                        <td className="px-4 py-3 max-w-[200px]">
                          <div className="truncate text-slate-800 font-medium font-sans text-sm" title={row.agenda}>{row.agenda}</div>
                        </td>
                        <td className="px-4 py-3 text-slate-500 text-xs font-sans max-w-[130px]"><div className="truncate">{row.lembaga}</div></td>
                        <td className="px-4 py-3 text-slate-500 text-xs font-sans hidden md:table-cell whitespace-nowrap">{row.provinsi || "—"}</td>
                        <td className="px-4 py-3 font-mono text-slate-700 text-xs whitespace-nowrap">{(row.pagu / 1e9).toFixed(2)} M</td>
                        <td className="px-4 py-3 font-mono font-black text-slate-900 text-sm whitespace-nowrap">{row.skor_risiko.toFixed(2)}</td>
                        <td className="px-4 py-3">
                          <span className={`inline-flex px-2 py-0.5 rounded-full text-[11px] font-bold border font-sans ${PILL[cat] || "bg-slate-100 text-slate-600"}`}>{cat}</span>
                        </td>
                      </tr>
                      <AnimatePresence>
                        {isExp && (
                          <tr><td colSpan={7} className="p-0">
                            <motion.div initial={{ height:0, opacity:0 }} animate={{ height:"auto", opacity:1 }} exit={{ height:0, opacity:0 }} transition={{ duration:0.18 }} className="overflow-hidden">
                              <Detail row={row} />
                            </motion.div>
                          </td></tr>
                        )}
                      </AnimatePresence>
                    </React.Fragment>
                  );
                })}
              </tbody>
            </table>
          </div>
          <Pagination page={page} pages={pages} onChange={setPage} />
        </div>
      </div>
    </div>
  );
}
