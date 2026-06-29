"use client";
import { useEffect, useState } from "react";
import {
  createColumnHelper,
  flexRender,
  getCoreRowModel,
  getSortedRowModel,
  useReactTable,
} from "@tanstack/react-table";
import { Search, Download, Filter } from "lucide-react";

type ProcurementData = {
  id: string;
  agenda: string;
  lembaga: string;
  pagu: number;
  skor_risiko: number;
};

const columnHelper = createColumnHelper<ProcurementData>();

const columns = [
  columnHelper.accessor("agenda", {
    header: "AGENDA / PAKET",
    cell: info => <div className="max-w-md truncate font-medium" title={info.getValue()}>{info.getValue()}</div>,
  }),
  columnHelper.accessor("lembaga", {
    header: "LEMBAGA",
    cell: info => info.getValue(),
  }),
  columnHelper.accessor("pagu", {
    header: "PAGU (RP)",
    cell: info => <span className="font-mono">{(info.getValue() / 1e9).toFixed(2)} M</span>,
  }),
  columnHelper.accessor("skor_risiko", {
    header: "R SCORE",
    cell: info => {
      const val = info.getValue();
      return <span className="font-mono font-bold">{val.toFixed(2)}</span>;
    },
  })
];

export default function DataPage() {
  const [data, setData] = useState<ProcurementData[]>([]);
  const [loading, setLoading] = useState(true);
  const [globalFilter, setGlobalFilter] = useState("");

  useEffect(() => {
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
    fetch(`${apiUrl}/procurement?limit=100`)
      .then(res => res.json())
      .then(d => {
        setData(d.data || []);
        setLoading(false);
      });
  }, []);

  const table = useReactTable({
    data,
    columns,
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
    state: { globalFilter },
    onGlobalFilterChange: setGlobalFilter,
  });

  // Strict R Score Rules
  const getRowClass = (r: number) => {
    if (r >= 90.16) return "bg-red-950/40 hover:bg-red-900/60 border-l-4 border-l-red-500 text-red-200";
    if (r >= 23.75) return "bg-orange-950/40 hover:bg-orange-900/60 border-l-4 border-l-orange-500 text-orange-200";
    if (r > 0) return "bg-yellow-950/40 hover:bg-yellow-900/60 border-l-4 border-l-yellow-500 text-yellow-200";
    return "bg-green-950/10 hover:bg-green-900/20 border-l-4 border-l-green-500/50 text-slate-300";
  };

  return (
    <div className="h-full flex flex-col p-6">
      <header className="mb-6 flex justify-between items-end">
        <div>
          <h1 className="text-2xl font-black uppercase tracking-tight text-white">Audit-Ready Data Explorer</h1>
          <p className="text-slate-500 text-sm font-mono mt-1">Quantile Regression Strict Classification</p>
        </div>
        <div className="flex gap-4">
          <div className="relative">
            <Search className="w-4 h-4 absolute left-3 top-3 text-slate-500" />
            <input 
              type="text" 
              placeholder="Global search..." 
              value={globalFilter}
              onChange={e => setGlobalFilter(e.target.value)}
              className="pl-9 pr-4 py-2 bg-slate-900 border border-slate-700 rounded-md text-sm text-white focus:outline-none focus:border-[#0D5CBD]"
            />
          </div>
          <button className="flex items-center gap-2 px-4 py-2 bg-[#0D5CBD] hover:bg-[#0D5CBD]/80 text-white rounded-md text-sm font-medium transition-colors">
            <Download className="w-4 h-4" /> Export CSV
          </button>
        </div>
      </header>

      <div className="flex-1 flex gap-6 min-h-0">
        {/* Left Filter Sidebar */}
        <div className="w-64 bg-slate-900/50 border border-slate-800 rounded-lg p-4 overflow-y-auto hidden md:block">
          <div className="flex items-center gap-2 text-slate-300 mb-6 font-bold uppercase text-xs">
            <Filter className="w-4 h-4" /> Attributes Filter
          </div>
          {/* Mock filters for structural layout */}
          <FilterSection title="RISK CLASSIFICATION" options={["Extreme Anomaly", "High Risk", "Medium Risk", "Low Risk"]} />
          <FilterSection title="PROCUREMENT METHOD" options={["Tender", "Pengadaan Langsung", "E-Purchasing"]} />
          <FilterSection title="FUNDING SOURCE" options={["APBN", "APBD", "BLU"]} />
        </div>

        {/* Main Table */}
        <div className="flex-1 bg-slate-900/30 border border-slate-800 rounded-lg overflow-auto">
          {loading ? (
            <div className="h-full flex items-center justify-center text-slate-500 font-mono">LOADING TELEMETRY...</div>
          ) : (
            <table className="w-full text-sm text-left whitespace-nowrap">
              <thead className="text-xs text-slate-400 bg-slate-950 uppercase border-b border-slate-800 sticky top-0 z-10">
                {table.getHeaderGroups().map(headerGroup => (
                  <tr key={headerGroup.id}>
                    {headerGroup.headers.map(header => (
                      <th key={header.id} className="px-6 py-4 tracking-wider cursor-pointer hover:text-white" onClick={header.column.getToggleSortingHandler()}>
                        {flexRender(header.column.columnDef.header, header.getContext())}
                      </th>
                    ))}
                  </tr>
                ))}
              </thead>
              <tbody className="divide-y divide-slate-800/50">
                {table.getRowModel().rows.map(row => (
                  <tr key={row.id} className={`transition-colors ${getRowClass(row.original.skor_risiko)}`}>
                    {row.getVisibleCells().map(cell => (
                      <td key={cell.id} className="px-6 py-4">
                        {flexRender(cell.column.columnDef.cell, cell.getContext())}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </div>
    </div>
  );
}

function FilterSection({ title, options }: { title: string, options: string[] }) {
  return (
    <div className="mb-6">
      <h3 className="text-xs font-mono text-slate-500 mb-3">{title}</h3>
      <div className="space-y-2">
        {options.map(opt => (
          <label key={opt} className="flex items-center gap-2 text-sm text-slate-300 cursor-pointer hover:text-white transition-colors">
            <input type="checkbox" className="rounded bg-slate-800 border-slate-700 text-[#0D5CBD] focus:ring-[#0D5CBD]" />
            {opt}
          </label>
        ))}
      </div>
    </div>
  );
}
