export const dynamic = 'force-dynamic';
import { Sidebar } from "@/components/layout/Sidebar";
export default function ReportsPage() {
  return (
    <div className="flex h-screen bg-slate-50 overflow-hidden">
      <Sidebar />
      <div className="flex-1 flex flex-col ml-64">
        <header className="h-16 bg-white border-b border-slate-200 flex items-center px-8 shadow-sm z-10">
          <h2 className="text-lg font-semibold text-slate-800">Reports</h2>
        </header>
        <main className="flex-1 p-6 relative">
          <div className="bg-white p-8 rounded-xl border border-slate-200 shadow-sm text-center">
            <h3 className="text-xl font-medium text-slate-600">Modul reports sedang dalam tahap integrasi...</h3>
          </div>
        </main>
      </div>
    </div>
  );
}
