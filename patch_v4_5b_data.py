"""Write DataClient.tsx and data/page.tsx with UTF-8 encoding"""
import os

FRONTEND_APP = r"D:\satdat 2026\sec\pantauang-enterprise\frontend\src\app"

data_client_tsx = r'''"use client";
import React, { useState, useEffect, useCallback } from "react";
import { ChevronDown, ChevronRight, Search, Download, X, ArrowUpDown, ArrowUp, ArrowDown, ChevronLeft } from "lucide-react";
import { ChevronRight as ChevronRightIcon } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

type Row = {
  id: string; agenda: string; lembaga: string; satker?: string;
  provinsi?: string; kota?: string; metode?: string; jenis?: string;
  pagu: number; p10?: number; p90?: number; fraud_value?: number;
  skor_risiko: number; kategori_risiko?: string;
};

type FilterState = { risiko: string; provinsi: string; metode: string; search: string };
type SortState   = { col: string; dir: "asc"|"desc" };

const RISK_PILL: Record<string, string> = {
  Anomali: "bg-red-100 text-red-700 border-red-200",
  Tinggi:  "bg-orange-100 text-orange-700 border-orange-200",
  Sedang:  "bg-yellow-100 text-yellow-700 border-yellow-200",
  Rendah:  "bg-green-100 text-green-700 border-green-200",
};
const RISK_BORDER: Record<string, string> = {
  Anomali: "border-l-[#FF5722]", Tinggi: "border-l-[#FF8A65]",
  Sedang:  "border-l-amber-400",  Rendah: "border-l-green-400",
};

function classify(skor: number) {
  if (skor >= 90.16) return "Anomali";
  if (skor >= 23.75) return "Tinggi";
  if (skor > 0)      return "Sedang";
  return "Rendah";
}

// ─── Async Data Hook ─────────────────────────────────────────────────
function useDataGrid(pageSize: number, filters: FilterState, sort: SortState) {
  const [data, setData]         = useState<Row[]>([]);
  const [total, setTotal]       = useState(0);
  const [totalPages, setTotalPages] = useState(1);
  const [page, setPage]         = useState(1);
  const [loading, setLoading]   = useState(false);

  const load = useCallback(async (p: number) => {
    setLoading(true);
    try {
      const base = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";
      const q = new URLSearchParams({ limit: String(pageSize), offset: String((p-1)*pageSize) });
      if (filters.search)   q.set("search",   filters.search);
      if (filters.risiko)   q.set("risiko",   filters.risiko);
      if (filters.provinsi) q.set("provinsi", filters.provinsi);
      if (filters.metode)   q.set("metode",   filters.metode);
      q.set("sort_by",  sort.col);
      q.set("sort_dir", sort.dir);

      const res  = await fetch(`${base}/procurement?${q}`, { cache: "no-store" });
      const json = await res.json();
      setData((json.data || []).map((r: Row) => ({ ...r, kategori_risiko: r.kategori_risiko || classify(r.skor_risiko) })));
      setTotal(json.total || 0);
      setTotalPages(json.total_pages || 1);
    } catch { setData([]); }
    finally { setLoading(false); }
  }, [pageSize, filters, sort]);

  useEffect(() => { setPage(1); }, [filters, sort, pageSize]);
  useEffect(() => { load(page); }, [page, load]);

  return { data, total, totalPages, page, setPage, loading };
}

// ─── Pagination Bar ──────────────────────────────────────────────────
function Pagination({ page, totalPages, onChange }: { page: number; totalPages: number; onChange: (p: number) => void }) {
  const pages: (number|string)[] = [];
  if (totalPages <= 9) {
    for (let i = 1; i <= totalPages; i++) pages.push(i);
  } else {
    [1,2,3].forEach(n => pages.push(n));
    if (page > 5) pages.push("...");
    for (let i = Math.max(4, page-1); i <= Math.min(totalPages-3, page+1); i++) pages.push(i);
    if (page < totalPages-4) pages.push("...");
    [totalPages-2, totalPages-1, totalPages].forEach(n => { if (!pages.includes(n)) pages.push(n); });
  }

  return (
    <div className="flex items-center justify-between px-4 py-3 border-t border-slate-100 bg-white/80 font-sans flex-wrap gap-3">
      <span className="text-xs text-slate-400">Hal. {page.toLocaleString()} / {totalPages.toLocaleString()}</span>
      <div className="flex items-center gap-1 flex-wrap">
        <button disabled={page <= 1} onClick={() => onChange(page-1)}
          className="p-1.5 rounded-lg hover:bg-slate-100 disabled:opacity-30 transition-colors">
          <ChevronLeft className="w-4 h-4 text-slate-500" />
        </button>
        {pages.map((p, i) => p === "..."
          ? <span key={`e${i}`} className="px-1.5 text-slate-400 text-xs">...</span>
          : <button key={`${p}_${i}`} onClick={() => onChange(p as number)}
              className={`min-w-[28px] h-7 rounded-lg text-xs font-bold transition-all px-1 ${page===p ? "bg-slate-900 text-white" : "text-slate-500 hover:bg-slate-100"}`}>
              {(p as number).toLocaleString()}
            </button>
        )}
        <button disabled={page >= totalPages} onClick={() => onChange(page+1)}
          className="p-1.5 rounded-lg hover:bg-slate-100 disabled:opacity-30 transition-colors">
          <ChevronRightIcon className="w-4 h-4 text-slate-500" />
        </button>
      </div>
    </div>
  );
}

// ─── Accordion Detail Panel ──────────────────────────────────────────
function RowDetail({ row }: { row: Row }) {
  const fields: [string, string][] = [
    ["Nama Paket Lengkap", row.agenda],
    ["Instansi / Lembaga", row.lembaga],
    ["Satker", row.satker || "—"],
    ["Provinsi", row.provinsi || "—"],
    ["Kota / Kabupaten", row.kota || "—"],
    ["Metode Pengadaan", row.metode || "—"],
    ["Jenis Pengadaan", row.jenis || "—"],
    ["Pagu Anggaran", `Rp ${(row.pagu/1e6).toFixed(2)} Juta`],
    ["P10 (Quantile 10%)", row.p10 != null ? row.p10.toFixed(6) : "—"],
    ["P90 (Quantile 90%)", row.p90 != null ? row.p90.toFixed(6) : "—"],
    ["Fraud Value", row.fraud_value != null ? row.fraud_value.toFixed(6) : "—"],
    ["Skor Risiko QRLGBM", row.skor_risiko.toFixed(6)],
    ["Kategori Risiko", row.kategori_risiko || "—"],
    ["ID Paket", row.id],
  ];
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 p-5 bg-slate-50/70 border-t border-slate-100">
      {fields.map(([label, val]) => (
        <div key={label}>
          <div className="text-[10px] text-slate-400 font-bold uppercase tracking-wider font-sans mb-0.5">{label}</div>
          <div className="text-sm text-slate-800 font-sans font-medium break-words">{val}</div>
        </div>
      ))}
    </div>
  );
}

// ─── Main Export ─────────────────────────────────────────────────────
export default function DataClient({ filterOptions }: { filterOptions?: any }) {
  const [pageSize, setPageSize] = useState(25);
  const [filters, setFilters]   = useState<FilterState>({ risiko:"", provinsi:"", metode:"", search:"" });
  const [sort, setSort]         = useState<SortState>({ col:"skor_risiko", dir:"desc" });
  const [expanded, setExpanded] = useState<Set<string>>(new Set());
  const [searchInput, setSearch] = useState("");

  const { data, total, totalPages, page, setPage, loading } = useDataGrid(pageSize, filters, sort);

  const toggleSort = (col: string) => setSort(s => s.col === col ? { col, dir: s.dir==="desc" ? "asc" : "desc" } : { col, dir:"desc" });
  const toggleRow  = (id: string) => setExpanded(prev => { const n = new Set(prev); n.has(id) ? n.delete(id) : n.add(id); return n; });
  const applySearch = () => setFilters(f => ({...f, search: searchInput}));

  const SortIcon = ({ col }: { col: string }) => {
    if (sort.col !== col) return <ArrowUpDown className="w-3 h-3 text-slate-300" />;
    return sort.dir==="desc" ? <ArrowDown className="w-3 h-3 text-slate-600" /> : <ArrowUp className="w-3 h-3 text-slate-600" />;
  };

  const provinceOpts = filterOptions?.provinsi?.slice(0,50) || [];
  const metodeOpts   = filterOptions?.metode || [];
  const hasFilter    = !!(filters.risiko || filters.provinsi || filters.metode || filters.search);

  return (
    <div className="min-h-screen font-sans py-8 px-4 md:px-8 bg-grid">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-6">
          <h1 className="font-serif font-black text-[clamp(1.8rem,3vw,2.8rem)] text-slate-900">Audit-Ready Data Explorer</h1>
          <p className="text-slate-500 text-sm font-sans mt-1">
            {loading ? "Memuat..." : <><span className="font-bold text-slate-700">{total.toLocaleString()}</span> baris ditemukan</>}
          </p>
        </div>

        {/* Filter Bar */}
        <div className="glass rounded-2xl border border-white/60 p-4 mb-4 shadow-sm">
          <div className="flex flex-col sm:flex-row flex-wrap gap-3">
            <div className="relative flex-1 min-w-[200px]">
              <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
              <input value={searchInput} onChange={e => setSearch(e.target.value)} onKeyDown={e => e.key==="Enter" && applySearch()}
                placeholder="Cari nama paket atau ID..." 
                className="w-full pl-9 pr-4 py-2.5 bg-white/80 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-[#1E88E5]/30 focus:border-[#1E88E5] transition-all font-sans" />
            </div>
            <select value={filters.risiko} onChange={e => setFilters(f => ({...f, risiko: e.target.value}))}
              className="py-2.5 px-3 bg-white/80 border border-slate-200 rounded-xl text-sm font-sans focus:outline-none focus:ring-2 focus:ring-[#1E88E5]/30">
              <option value="">Semua Risiko</option>
              {["Rendah","Sedang","Tinggi","Anomali"].map(r => <option key={r} value={r}>{r}</option>)}
            </select>
            <select value={filters.provinsi} onChange={e => setFilters(f => ({...f, provinsi: e.target.value}))}
              className="py-2.5 px-3 bg-white/80 border border-slate-200 rounded-xl text-sm font-sans focus:outline-none focus:ring-2 focus:ring-[#1E88E5]/30">
              <option value="">Semua Provinsi</option>
              {provinceOpts.map((p: string) => <option key={p} value={p}>{p}</option>)}
            </select>
            <select value={filters.metode} onChange={e => setFilters(f => ({...f, metode: e.target.value}))}
              className="py-2.5 px-3 bg-white/80 border border-slate-200 rounded-xl text-sm font-sans focus:outline-none focus:ring-2 focus:ring-[#1E88E5]/30">
              <option value="">Semua Metode</option>
              {metodeOpts.map((m: string) => <option key={m} value={m}>{m}</option>)}
            </select>
            <button onClick={applySearch} className="px-5 py-2.5 bg-slate-900 text-white text-sm font-bold rounded-xl hover:bg-slate-800 transition-all shadow-sm">Cari</button>
            {hasFilter && (
              <button onClick={() => { setFilters({ risiko:"", provinsi:"", metode:"", search:"" }); setSearch(""); }}
                className="flex items-center gap-1.5 px-3 py-2.5 text-sm text-slate-500 hover:text-slate-800 rounded-xl hover:bg-slate-100 transition-all font-sans">
                <X className="w-3.5 h-3.5" /> Reset
              </button>
            )}
          </div>
        </div>

        {/* Table */}
        <div className="glass rounded-2xl border border-white/60 shadow-md overflow-hidden">
          {/* Controls */}
          <div className="flex items-center justify-between px-4 py-3 border-b border-slate-100 bg-white/50 gap-3 flex-wrap">
            <div className="flex items-center gap-2 text-xs font-sans text-slate-500">
              Tampilkan
              <select value={pageSize} onChange={e => setPageSize(Number(e.target.value))}
                className="border border-slate-200 rounded-lg px-2 py-1 bg-white text-slate-700 font-bold focus:outline-none">
                {[10,25,50,100].map(n => <option key={n} value={n}>{n}</option>)}
              </select>
              baris per halaman
            </div>
            <button className="flex items-center gap-2 px-3 py-1.5 text-xs font-bold text-slate-500 hover:text-slate-800 border border-slate-200 rounded-lg hover:bg-slate-50 transition-all font-sans">
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
                  <th className="px-4 py-3 text-left cursor-pointer select-none whitespace-nowrap" onClick={() => toggleSort("pagu")}>
                    <div className="flex items-center gap-1.5 text-xs font-bold font-sans text-slate-500 uppercase tracking-wider">Pagu (Rp) <SortIcon col="pagu" /></div>
                  </th>
                  <th className="px-4 py-3 text-left cursor-pointer select-none whitespace-nowrap" onClick={() => toggleSort("skor_risiko")}>
                    <div className="flex items-center gap-1.5 text-xs font-bold font-sans text-slate-500 uppercase tracking-wider">R-Score <SortIcon col="skor_risiko" /></div>
                  </th>
                  <th className="px-4 py-3 text-left text-xs font-bold font-sans text-slate-500 uppercase tracking-wider whitespace-nowrap">Kategori</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {loading ? Array.from({ length: 5 }).map((_,i) => (
                  <tr key={i} className="animate-pulse">
                    {Array.from({length:7}).map((_,j) => <td key={j} className="px-4 py-3"><div className="h-4 bg-slate-100 rounded"/></td>)}
                  </tr>
                )) : data.length === 0 ? (
                  <tr><td colSpan={7} className="py-16 text-center text-slate-400 text-sm font-sans">Tidak ada data untuk filter ini.</td></tr>
                ) : data.map(row => {
                  const cat  = row.kategori_risiko || "Rendah";
                  const isExp = expanded.has(row.id);
                  return (
                    <React.Fragment key={row.id}>
                      <tr className={`border-l-4 ${RISK_BORDER[cat] || "border-l-slate-200"} hover:bg-slate-50/80 transition-colors`}>
                        <td className="px-3 py-3 text-center">
                          <button onClick={() => toggleRow(row.id)} className="w-6 h-6 flex items-center justify-center rounded-md hover:bg-slate-200 transition-colors">
                            {isExp ? <ChevronDown className="w-3.5 h-3.5 text-slate-500" /> : <ChevronRight className="w-3.5 h-3.5 text-slate-400" />}
                          </button>
                        </td>
                        <td className="px-4 py-3 max-w-[200px]"><div className="truncate text-slate-800 font-medium font-sans text-sm" title={row.agenda}>{row.agenda}</div></td>
                        <td className="px-4 py-3 text-slate-500 text-xs font-sans max-w-[130px]"><div className="truncate">{row.lembaga}</div></td>
                        <td className="px-4 py-3 text-slate-500 text-xs font-sans hidden md:table-cell whitespace-nowrap">{row.provinsi || "—"}</td>
                        <td className="px-4 py-3 font-mono text-slate-700 text-xs whitespace-nowrap">{(row.pagu/1e9).toFixed(2)} M</td>
                        <td className="px-4 py-3 font-mono font-black text-slate-900 text-sm whitespace-nowrap">{row.skor_risiko.toFixed(2)}</td>
                        <td className="px-4 py-3">
                          <span className={`inline-flex px-2 py-0.5 rounded-full text-[11px] font-bold border font-sans ${RISK_PILL[cat] || "bg-slate-100 text-slate-600"}`}>{cat}</span>
                        </td>
                      </tr>
                      <AnimatePresence>
                        {isExp && (
                          <tr><td colSpan={7} className="p-0">
                            <motion.div initial={{ height:0, opacity:0 }} animate={{ height:"auto", opacity:1 }} exit={{ height:0, opacity:0 }} transition={{ duration:0.18 }} className="overflow-hidden">
                              <RowDetail row={row} />
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
          <Pagination page={page} totalPages={totalPages} onChange={setPage} />
        </div>
      </div>
    </div>
  );
}
'''

with open(os.path.join(FRONTEND_APP, "data/DataClient.tsx"), "w", encoding="utf-8") as f:
    f.write(data_client_tsx)

# data/page.tsx
page_tsx = '''async function fetchSSR(endpoint: string) {
  try {
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";
    const res = await fetch(`${apiUrl}${endpoint}`, { cache: "no-store" });
    if (!res.ok) return null;
    return await res.json();
  } catch { return null; }
}

import DataClient from "./DataClient";

export default async function DataPage() {
  const filterOptions = await fetchSSR("/procurement/filters") || { provinsi: [], metode: [] };
  return <DataClient filterOptions={filterOptions} />;
}
'''

with open(os.path.join(FRONTEND_APP, "data/page.tsx"), "w", encoding="utf-8") as f:
    f.write(page_tsx)

print("DataClient + page.tsx done")
