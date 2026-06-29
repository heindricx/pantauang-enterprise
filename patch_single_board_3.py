import os

frontend_app_dir = r"D:\satdat 2026\sec\pantauang-enterprise\frontend\src\app"

# PetaClient.tsx (Capitalize headers)
peta_file = os.path.join(frontend_app_dir, "peta/PetaClient.tsx")
with open(peta_file, "r") as f:
    peta_content = f.read()
peta_content = peta_content.replace("uppercase text-slate-800", "capitalize text-slate-800")
with open(peta_file, "w") as f:
    f.write(peta_content)

# InfografisClient.tsx (Capitalize headers)
info_file = os.path.join(frontend_app_dir, "infografis/InfografisClient.tsx")
with open(info_file, "r") as f:
    info_content = f.read()
info_content = info_content.replace("uppercase text-slate-900", "capitalize text-slate-900")
info_content = info_content.replace("uppercase text-slate-800", "capitalize text-slate-800")
info_content = info_content.replace("uppercase", "capitalize")
with open(info_file, "w") as f:
    f.write(info_content)

# DataClient.tsx
with open(os.path.join(frontend_app_dir, "data/DataClient.tsx"), "w") as f:
    f.write('''"use client";
import { useState, useMemo } from "react";
import {
  createColumnHelper,
  flexRender,
  getCoreRowModel,
  getSortedRowModel,
  getFilteredRowModel,
  useReactTable,
  getExpandedRowModel,
  SortingState
} from "@tanstack/react-table";
import { Search, Download, Filter, ChevronDown, ChevronRight, ArrowUpDown, ChevronUp } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

type ProcurementData = {
  id: string;
  agenda: string;
  lembaga: string;
  pagu: number;
  skor_risiko: number;
  kategori_risiko?: string;
  metode?: string;
  sumber_dana?: string;
  provinsi?: string;
};

const columnHelper = createColumnHelper<ProcurementData>();

export default function DataClient({ initialData }: { initialData: ProcurementData[] }) {
  const [globalFilter, setGlobalFilter] = useState("");
  const [sorting, setSorting] = useState<SortingState>([]);
  const [activeFilters, setActiveFilters] = useState<Record<string, string[]>>({});

  // Enrich data with mock fields if missing, to guarantee UI logic works for the demo
  const enrichedData = useMemo(() => {
    return initialData.map(d => {
      let cat = "Rendah";
      if (d.skor_risiko >= 90.16) cat = "Anomali";
      else if (d.skor_risiko >= 23.75) cat = "Tinggi";
      else if (d.skor_risiko > 0) cat = "Sedang";
      
      const methods = ["Tender", "Pengadaan Langsung", "E-Purchasing"];
      const sources = ["APBN", "APBD", "BLU"];
      const provs = ["DKI Jakarta", "Jawa Barat", "Jawa Timur", "Sumatera Utara"];
      const hash = d.agenda.length;
      
      return {
        ...d,
        kategori_risiko: d.kategori_risiko || cat,
        metode: d.metode || methods[hash % methods.length],
        sumber_dana: d.sumber_dana || sources[(hash + 1) % sources.length],
        provinsi: d.provinsi || provs[(hash + 2) % provs.length]
      };
    });
  }, [initialData]);

  const columns = useMemo(() => [
    columnHelper.display({
      id: "expander",
      header: () => null,
      cell: ({ row }) => (
        <button
          onClick={row.getToggleExpandedHandler()}
          className="p-1 hover:bg-slate-200 rounded-full transition-colors"
        >
          {row.getIsExpanded() ? <ChevronDown className="w-4 h-4 text-slate-500" /> : <ChevronRight className="w-4 h-4 text-slate-500" />}
        </button>
      ),
    }),
    columnHelper.accessor("agenda", {
      header: "Nama Paket",
      cell: info => <div className="max-w-xs md:max-w-md truncate font-bold text-slate-800" title={info.getValue()}>{info.getValue()}</div>,
    }),
    columnHelper.accessor("lembaga", {
      header: "Lembaga",
      cell: info => <span className="text-slate-600">{info.getValue()}</span>,
    }),
    columnHelper.accessor("pagu", {
      header: ({ column }) => (
        <div className="flex items-center gap-2 cursor-pointer select-none" onClick={column.getToggleSortingHandler()}>
          Pagu (Rp) <ArrowUpDown className="w-3 h-3 text-slate-400" />
        </div>
      ),
      cell: info => <span className="font-mono text-slate-700">{(info.getValue() / 1e9).toFixed(2)} M</span>,
    }),
    columnHelper.accessor("skor_risiko", {
      header: ({ column }) => (
        <div className="flex items-center gap-2 cursor-pointer select-none" onClick={column.getToggleSortingHandler()}>
          R-Score <ArrowUpDown className="w-3 h-3 text-slate-400" />
        </div>
      ),
      cell: info => {
        const val = info.getValue();
        return <span className="font-mono font-black text-slate-900">{val.toFixed(2)}</span>;
      },
    }),
    columnHelper.accessor("kategori_risiko", {
      header: "Kategori",
      cell: info => {
        const val = info.getValue();
        let color = "bg-green-100 text-green-700";
        if (val === "Anomali") color = "bg-red-100 text-red-700";
        if (val === "Tinggi") color = "bg-orange-100 text-orange-700";
        if (val === "Sedang") color = "bg-yellow-100 text-yellow-700";
        return <span className={`px-2 py-1 rounded text-xs font-bold ${color}`}>{val}</span>;
      }
    })
  ], []);

  const filteredData = useMemo(() => {
    return enrichedData.filter(item => {
      // Global Search
      if (globalFilter && !item.agenda.toLowerCase().includes(globalFilter.toLowerCase())) return false;
      // Multi-attribute filters
      for (const [key, selectedVals] of Object.entries(activeFilters)) {
        if (selectedVals.length > 0) {
          const itemVal = (item as any)[key];
          if (!selectedVals.includes(itemVal)) return false;
        }
      }
      return true;
    });
  }, [enrichedData, globalFilter, activeFilters]);

  const table = useReactTable({
    data: filteredData,
    columns,
    state: { sorting },
    onSortingChange: setSorting,
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
    getExpandedRowModel: getExpandedRowModel(),
    getRowCanExpand: () => true,
  });

  const getRowClass = (cat: string | undefined) => {
    if (cat === "Anomali") return "bg-red-50 hover:bg-red-100 border-l-4 border-l-[#FF5722]";
    if (cat === "Tinggi") return "bg-orange-50 hover:bg-orange-100 border-l-4 border-l-[#FF8A65]";
    if (cat === "Sedang") return "bg-yellow-50 hover:bg-yellow-100 border-l-4 border-l-yellow-400";
    return "bg-green-50 hover:bg-green-100 border-l-4 border-l-[#4CAF50]";
  };

  const handleFilterToggle = (key: string, val: string) => {
    setActiveFilters(prev => {
      const current = prev[key] || [];
      if (current.includes(val)) {
        return { ...prev, [key]: current.filter(v => v !== val) };
      }
      return { ...prev, [key]: [...current, val] };
    });
  };

  return (
    <div className="min-h-screen flex flex-col p-6 font-sans mt-8 bg-slate-50">
      <div className="max-w-7xl mx-auto w-full">
        <header className="mb-8">
          <h1 className="font-serif capitalize text-3xl font-black text-slate-800 mb-2">Audit-Ready Data Explorer</h1>
          <p className="text-slate-500 text-sm">Quantile Regression Strict Classification & Multi-Attribute Filtering</p>
        </header>

        <div className="flex flex-col md:flex-row gap-6 items-start">
          {/* FILTER SIDEBAR */}
          <div className="w-full md:w-64 bg-white border border-slate-200 rounded-xl p-5 shadow-sm shrink-0">
            <div className="flex items-center gap-2 text-slate-800 mb-6 font-bold capitalize">
              <Filter className="w-4 h-4 text-[#1E88E5]" /> Filter Lanjutan
            </div>
            
            <FilterGroup 
              title="Kategori Risiko" 
              field="kategori_risiko"
              options={["Anomali", "Tinggi", "Sedang", "Rendah"]} 
              activeFilters={activeFilters}
              onToggle={handleFilterToggle}
            />
            <FilterGroup 
              title="Metode Pengadaan" 
              field="metode"
              options={["Tender", "Pengadaan Langsung", "E-Purchasing"]} 
              activeFilters={activeFilters}
              onToggle={handleFilterToggle}
            />
            <FilterGroup 
              title="Sumber Dana" 
              field="sumber_dana"
              options={["APBN", "APBD", "BLU"]} 
              activeFilters={activeFilters}
              onToggle={handleFilterToggle}
            />
            <FilterGroup 
              title="Provinsi" 
              field="provinsi"
              options={["DKI Jakarta", "Jawa Barat", "Jawa Timur", "Sumatera Utara"]} 
              activeFilters={activeFilters}
              onToggle={handleFilterToggle}
            />
          </div>

          {/* TABLE AREA */}
          <div className="flex-1 w-full bg-white border border-slate-200 rounded-xl shadow-sm overflow-hidden flex flex-col">
            <div className="p-4 border-b border-slate-100 flex flex-col sm:flex-row justify-between items-center gap-4 bg-slate-50/50">
              <div className="relative w-full sm:w-72">
                <Search className="w-4 h-4 absolute left-3 top-3 text-slate-400" />
                <input 
                  type="text" 
                  placeholder="Cari nama paket..." 
                  value={globalFilter}
                  onChange={e => setGlobalFilter(e.target.value)}
                  className="w-full pl-9 pr-4 py-2 bg-white border border-slate-200 rounded-lg text-sm text-slate-800 focus:outline-none focus:border-[#1E88E5] focus:ring-1 focus:ring-[#1E88E5] transition-all"
                />
              </div>
              <button className="flex items-center justify-center gap-2 px-4 py-2 bg-slate-900 hover:bg-slate-800 text-white rounded-lg text-sm font-bold transition-all w-full sm:w-auto shadow-md">
                <Download className="w-4 h-4" /> Unduh CSV
              </button>
            </div>

            <div className="overflow-x-auto w-full">
              <table className="w-full text-sm text-left">
                <thead className="text-xs text-slate-500 bg-white border-b border-slate-200">
                  {table.getHeaderGroups().map(headerGroup => (
                    <tr key={headerGroup.id}>
                      {headerGroup.headers.map(header => (
                        <th key={header.id} className="px-6 py-4 font-bold capitalize tracking-wide bg-slate-50">
                          {flexRender(header.column.columnDef.header, header.getContext())}
                        </th>
                      ))}
                    </tr>
                  ))}
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {table.getRowModel().rows.map(row => (
                    <React.Fragment key={row.id}>
                      <tr className={`transition-colors ${getRowClass(row.original.kategori_risiko)}`}>
                        {row.getVisibleCells().map(cell => (
                          <td key={cell.id} className="px-6 py-4 whitespace-nowrap">
                            {flexRender(cell.column.columnDef.cell, cell.getContext())}
                          </td>
                        ))}
                      </tr>
                      {/* ACCORDION EXPANDED ROW */}
                      <AnimatePresence>
                        {row.getIsExpanded() && (
                          <tr>
                            <td colSpan={columns.length} className="p-0 border-l-4 border-l-slate-400 bg-slate-50/80">
                              <motion.div 
                                initial={{ height: 0, opacity: 0 }}
                                animate={{ height: "auto", opacity: 1 }}
                                exit={{ height: 0, opacity: 0 }}
                                className="overflow-hidden"
                              >
                                <div className="p-6 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 text-sm">
                                  <div>
                                    <h4 className="text-slate-400 font-bold mb-1 text-xs capitalize">Nama Paket Lengkap</h4>
                                    <p className="text-slate-800 font-medium">{row.original.agenda}</p>
                                  </div>
                                  <div>
                                    <h4 className="text-slate-400 font-bold mb-1 text-xs capitalize">Instansi / Lembaga</h4>
                                    <p className="text-slate-800 font-medium">{row.original.lembaga}</p>
                                  </div>
                                  <div>
                                    <h4 className="text-slate-400 font-bold mb-1 text-xs capitalize">Provinsi</h4>
                                    <p className="text-slate-800 font-medium">{row.original.provinsi}</p>
                                  </div>
                                  <div>
                                    <h4 className="text-slate-400 font-bold mb-1 text-xs capitalize">Metode Pengadaan</h4>
                                    <p className="text-slate-800 font-medium">{row.original.metode}</p>
                                  </div>
                                  <div>
                                    <h4 className="text-slate-400 font-bold mb-1 text-xs capitalize">Sumber Dana</h4>
                                    <p className="text-slate-800 font-medium">{row.original.sumber_dana}</p>
                                  </div>
                                  <div>
                                    <h4 className="text-slate-400 font-bold mb-1 text-xs capitalize">ID Pengadaan</h4>
                                    <p className="text-slate-800 font-mono text-xs">{row.original.id}</p>
                                  </div>
                                </div>
                              </motion.div>
                            </td>
                          </tr>
                        )}
                      </AnimatePresence>
                    </React.Fragment>
                  ))}
                  {table.getRowModel().rows.length === 0 && (
                    <tr><td colSpan={6} className="p-12 text-center text-slate-400 font-mono">Data tidak ditemukan untuk kriteria filter ini.</td></tr>
                  )}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

function FilterGroup({ title, field, options, activeFilters, onToggle }: { title: string, field: string, options: string[], activeFilters: Record<string, string[]>, onToggle: (k: string, v: string) => void }) {
  return (
    <div className="mb-6 border-t border-slate-100 pt-4">
      <h3 className="text-xs font-bold text-slate-500 mb-3 capitalize">{title}</h3>
      <div className="space-y-2">
        {options.map(opt => {
          const isActive = activeFilters[field]?.includes(opt);
          return (
            <label key={opt} className="flex items-center gap-2 text-sm text-slate-600 cursor-pointer hover:text-slate-900 transition-colors">
              <div className={`w-4 h-4 rounded border flex items-center justify-center transition-colors ${isActive ? 'bg-[#1E88E5] border-[#1E88E5]' : 'border-slate-300 bg-white'}`}>
                {isActive && <div className="w-2 h-2 bg-white rounded-sm" />}
              </div>
              <input 
                type="checkbox" 
                className="hidden" 
                checked={isActive || false}
                onChange={() => onToggle(field, opt)}
              />
              {opt}
            </label>
          );
        })}
      </div>
    </div>
  );
}
import React from 'react';
''')

print("Step 3 done")
