"use client";
import { Sidebar } from "@/components/layout/Sidebar";
import { useEffect, useState } from "react";

export default function ProcurementPage() {
  const [data, setData] = useState([]);
  
  useEffect(() => {
    fetch("https://heindricx-pantauang-backend.hf.space")
      .then(res => res.json())
      .then(d => setData(d.data || []));
  }, []);

  return (
    <div className="flex h-screen bg-slate-50 overflow-hidden">
      <Sidebar />
      <div className="flex-1 flex flex-col ml-64">
        <header className="h-16 bg-white border-b border-slate-200 flex items-center px-8 shadow-sm z-10">
          <h2 className="text-lg font-semibold text-slate-800">Eksplorasi Data Pengadaan</h2>
        </header>
        <main className="flex-1 p-6 relative overflow-auto">
          <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full text-sm text-left">
                <thead className="text-xs text-slate-500 bg-slate-50 uppercase sticky top-0">
                  <tr>
                    <th className="px-6 py-4">Agenda / Paket</th>
                    <th className="px-6 py-4">Lembaga</th>
                    <th className="px-6 py-4">Pagu (Rp)</th>
                    <th className="px-6 py-4">P90 (Wajar)</th>
                    <th className="px-6 py-4">Skor Risiko</th>
                    <th className="px-6 py-4">Status</th>
                  </tr>
                </thead>
                <tbody>
                  {data.map((row: any) => (
                    <tr key={row.id} className="border-b border-slate-100 hover:bg-slate-50">
                      <td className="px-6 py-4 font-medium text-slate-900 line-clamp-2" title={row.agenda}>{row.agenda.substring(0, 50)}...</td>
                      <td className="px-6 py-4">{row.lembaga}</td>
                      <td className="px-6 py-4">{row.pagu?.toLocaleString()}</td>
                      <td className="px-6 py-4">{row.p90?.toLocaleString()}</td>
                      <td className="px-6 py-4">{row.skor_risiko?.toFixed(2)}</td>
                      <td className="px-6 py-4">
                        <span className={`px-2 py-1 rounded-full text-xs font-semibold ${row.kategori_risiko === 'Tinggi' ? 'bg-red-100 text-red-700' : 'bg-green-100 text-green-700'}`}>
                          {row.kategori_risiko}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
