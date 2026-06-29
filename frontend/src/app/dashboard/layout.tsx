import { Sidebar } from "@/components/layout/Sidebar";

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex h-screen bg-[#FDFBF7] overflow-hidden relative">
      {/* Subtle background element for dashboard */}
      <div className="absolute top-0 right-0 w-[800px] h-[800px] bg-gradient-to-bl from-blue-100/40 to-transparent rounded-full blur-[100px] -z-10 pointer-events-none" />
      
      <Sidebar />
      
      <div className="flex-1 flex flex-col ml-72">
        <header className="h-24 flex items-end pb-4 px-10 z-10">
          <h2 className="text-3xl font-bold tracking-tight text-slate-800">Ringkasan Eksekutif</h2>
        </header>
        <main className="flex-1 overflow-auto p-10 pt-4 pb-24">
          {children}
        </main>
      </div>
    </div>
  );
}
