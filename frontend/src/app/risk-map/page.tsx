import { Sidebar } from "@/components/layout/Sidebar";
import RiskMap from "@/components/map/RiskMap";

export default function RiskMapPage() {
  return (
    <div className="flex h-screen bg-slate-50 overflow-hidden">
      <Sidebar />
      <div className="flex-1 flex flex-col ml-64">
        <header className="h-16 bg-white border-b border-slate-200 flex items-center px-8 shadow-sm z-10">
          <h2 className="text-lg font-semibold text-slate-800">Peta Risiko Interaktif</h2>
        </header>
        <main className="flex-1 p-6 relative">
          <RiskMap />
        </main>
      </div>
    </div>
  );
}
