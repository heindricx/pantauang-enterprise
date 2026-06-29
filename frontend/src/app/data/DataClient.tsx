"use client";
import { useState } from "react";
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
    cell: info => <div className="max-w-md truncate font-medium text-slate-700" title={info.getValue()}>{info.getValue()}</div>,
  }),
  columnHelper.accessor("lembaga", {
    header: "LEMBAGA",
    cell: info => <span className="text-slate-600">{info.getValue()}</span>,
  }),
  columnHelper.accessor("pagu", {
    header: "PAGU (RP)",
    cell: info => <span className="font-mono text-slate-800">{(info.getValue() / 1e9).toFixed(2)} M</span>,
  }),
  columnHelper.accessor("skor_risiko", {
    header: "R SCORE",
    cell: info => {
      const val = info.getValue();
      return <span className="font-mono font-bold text-slate-800">{val.toFixed(2)}</span>;
    },
  })
];

export default function DataClient({ initialData }: { initialData: ProcurementData[] }) {
  const [globalFilter, setGlobalFilter] = useState("");

  const table = useReactTable({
    data: initialData || [],
    columns,
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
    state: { globalFilter },
    onGlobalFilterChange: setGlobalFilter,
  });

  const getRowClass = (r: number) => {
    if (r >= 90.16) return "bg-red-50 hover:bg-red-100 border-l-4 border-l-[#FF5722]";
    if (r >= 23.75) return "bg-orange-50 hover:bg-orange-100 border-l-4 border-l-[#FF8A65]";
    if (r > 0) return "bg-yellow-50 hover:bg-yellow-100 border-l-4 border-l-yellow-400";
    return "bg-green-50 hover:bg-green-100 border-l-4 border-l-[#4CAF50]";
  };

  return (
    <div className="h-full flex flex-col p-6">
      <header className="mb-6 flex justify-between items-end">
        <div>
          <h1 className="text-2xl font-black uppercase tracking-tight text-slate-800">Audit-Ready Data Explorer</h1>
          <p className="text-slate-500 text-sm font-mono mt-1">Quantile Regression Strict Classification</p>
        </div>
        <div className="flex gap-4">
          <div className="relative">
            <Search className="w-4 h-4 absolute left-3 top-3 text-slate-400" />
            <input 
              type="text" 
              placeholder="Global search..." 
              value={globalFilter}
              onChange={e => setGlobalFilter(e.target.value)}
              className="pl-9 pr-4 py-2 bg-white border border-slate-200 rounded-md text-sm text-slate-800 focus:outline-none focus:border-[#1E88E5] focus:ring-1 focus:ring-[#1E88E5]"
            />
          </div>
          <button className="flex items-center gap-2 px-4 py-2 bg-[#7E57C2] hover:bg-[#6b47ab] text-white rounded-md text-sm font-medium transition-colors">
            <Download className="w-4 h-4" /> Export CSV
          </button>
        </div>
      </header>

      <div className="flex-1 flex gap-6 min-h-0">
        <div className="w-64 bg-white border border-slate-200 rounded-lg p-4 overflow-y-auto hidden md:block shadow-sm">
          <div className="flex items-center gap-2 text-slate-800 mb-6 font-bold uppercase text-xs">
            <Filter className="w-4 h-4 text-[#1E88E5]" /> Attributes Filter
          </div>
          <FilterSection title="RISK CLASSIFICATION" options={["Extreme Anomaly", "High Risk", "Medium Risk", "Low Risk"]} color="text-[#FF5722]" />
          <FilterSection title="PROCUREMENT METHOD" options={["Tender", "Pengadaan Langsung", "E-Purchasing"]} color="text-[#7E57C2]" />
          <FilterSection title="FUNDING SOURCE" options={["APBN", "APBD", "BLU"]} color="text-[#26C6DA]" />
        </div>

        <div className="flex-1 bg-white border border-slate-200 rounded-lg overflow-auto shadow-sm">
          <table className="w-full text-sm text-left whitespace-nowrap">
            <thead className="text-xs text-slate-500 bg-slate-50 uppercase border-b border-slate-200 sticky top-0 z-10">
              {table.getHeaderGroups().map(headerGroup => (
                <tr key={headerGroup.id}>
                  {headerGroup.headers.map(header => (
                    <th key={header.id} className="px-6 py-4 tracking-wider cursor-pointer hover:text-slate-800 bg-slate-50" onClick={header.column.getToggleSortingHandler()}>
                      {flexRender(header.column.columnDef.header, header.getContext())}
                    </th>
                  ))}
                </tr>
              ))}
            </thead>
            <tbody className="divide-y divide-slate-100">
              {table.getRowModel().rows.map(row => (
                <tr key={row.id} className={`transition-colors ${getRowClass(row.original.skor_risiko)}`}>
                  {row.getVisibleCells().map(cell => (
                    <td key={cell.id} className="px-6 py-4">
                      {flexRender(cell.column.columnDef.cell, cell.getContext())}
                    </td>
                  ))}
                </tr>
              ))}
              {table.getRowModel().rows.length === 0 && (
                <tr><td colSpan={4} className="p-8 text-center text-slate-400 font-mono">No telemetry data found.</td></tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

function FilterSection({ title, options, color }: { title: string, options: string[], color: string }) {
  return (
    <div className="mb-6">
      <h3 className={`text-xs font-bold ${color} mb-3 uppercase tracking-wider`}>{title}</h3>
      <div className="space-y-2">
        {options.map(opt => (
          <label key={opt} className="flex items-center gap-2 text-sm text-slate-600 cursor-pointer hover:text-slate-900 transition-colors">
            <input type="checkbox" className="rounded border-slate-300 text-[#1E88E5] focus:ring-[#1E88E5]" />
            {opt}
          </label>
        ))}
      </div>
    </div>
  );
}
