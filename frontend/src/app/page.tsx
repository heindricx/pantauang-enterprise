import Link from 'next/link';

export default function LandingPage() {
  return (
    <div className="relative min-h-screen overflow-hidden bg-slate-50">
      {/* Animated background gradient mesh simulation */}
      <div className="absolute top-0 left-0 w-full h-full overflow-hidden -z-10">
        <div className="absolute -top-40 -left-40 w-96 h-96 bg-blue-400 rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-blob"></div>
        <div className="absolute top-0 -right-40 w-96 h-96 bg-purple-400 rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-blob animation-delay-2000"></div>
        <div className="absolute -bottom-40 left-20 w-96 h-96 bg-orange-400 rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-blob animation-delay-4000"></div>
      </div>

      <main className="flex flex-col items-center justify-center min-h-screen px-4 text-center">
        <h1 className="text-6xl md:text-8xl font-extrabold tracking-tight text-slate-900 mb-6 drop-shadow-sm">
          PantaUang Kita
        </h1>
        <p className="text-xl md:text-2xl font-medium text-slate-600 mb-10 max-w-3xl">
          Platform Intelijen Risiko Pengadaan Nasional Berbasis AI
        </p>
        
        <div className="flex flex-col sm:flex-row gap-4">
          <Link href="/dashboard" className="px-8 py-4 bg-[#0D5CBD] hover:bg-blue-700 text-white rounded-lg font-semibold text-lg transition-all shadow-lg hover:shadow-xl hover:-translate-y-1">
            Eksplor Data
          </Link>
          <Link href="/dashboard" className="px-8 py-4 bg-white border-2 border-slate-200 hover:border-slate-300 text-slate-700 rounded-lg font-semibold text-lg transition-all shadow-sm hover:shadow-md hover:-translate-y-1">
            Lihat Analisis
          </Link>
        </div>
      </main>
    </div>
  );
}
