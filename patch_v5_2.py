"""Patch Peta (better frame with gradient fade) and DataClient (fix data loading fallback)"""
import os

FRONTEND_APP = r"D:\satdat 2026\sec\pantauang-enterprise\frontend\src\app"

# ─── PetaClient.tsx — Better frame, gradient fade, quantitative legend ───
peta_tsx = '''"use client";
import Map, { NavigationControl, Source, Layer } from "react-map-gl/maplibre";
import "maplibre-gl/dist/maplibre-gl.css";
import { useState, useMemo, useEffect } from "react";
import { Info } from "lucide-react";

const FILTERS = ["Rendah", "Sedang", "Tinggi", "Anomali", "Total Paket"];

// Quantitative legend breakpoints per filter
const LEGEND_STEPS: Record<string, { label: string; color: string }[]> = {
  "Rendah":      [{ label: "0-100",  color:"#EFF6FF" }, { label:"101-500", color:"#93C5FD" }, { label:"501-2K", color:"#4DB6AC" }, { label:"2K-10K", color:"#4CAF50" }, { label:"10K+", color:"#FBC02D" }],
  "Sedang":      [{ label: "0-100",  color:"#FFF7ED" }, { label:"101-500", color:"#FED7AA" }, { label:"501-2K", color:"#FB923C" }, { label:"2K-10K", color:"#F57C00" }, { label:"10K+", color:"#E65100" }],
  "Tinggi":      [{ label: "0-100",  color:"#FFF1EE" }, { label:"101-500", color:"#FFCCBC" }, { label:"501-2K", color:"#FF8A65" }, { label:"2K-10K", color:"#D84315" }, { label:"10K+", color:"#BF360C" }],
  "Anomali":     [{ label: "0-100",  color:"#FEF2F2" }, { label:"101-500", color:"#FECACA" }, { label:"501-2K", color:"#F87171" }, { label:"2K-10K", color:"#DC2626" }, { label:"10K+", color:"#7F1D1D" }],
  "Total Paket": [{ label: "0-1K",   color:"#F5F3FF" }, { label:"1K-10K", color:"#C4B5FD" }, { label:"10K-50K", color:"#8B5CF6" }, { label:"50K-200K", color:"#6D28D9" }, { label:"200K+", color:"#3B0764" }],
};

function getColor(val: number, filter: string): string {
  if (val === 0) return "#F1F5F9";
  const steps = LEGEND_STEPS[filter] || LEGEND_STEPS["Total Paket"];
  const thresholds = [100, 500, 2000, 10000];
  if (filter === "Total Paket") {
    const tpThresholds = [1000, 10000, 50000, 200000];
    const idx = tpThresholds.findIndex(t => val <= t);
    return idx === -1 ? steps[4].color : steps[Math.max(0, idx)].color;
  }
  const idx = thresholds.findIndex(t => val <= t);
  return idx === -1 ? steps[4].color : steps[Math.max(0, idx)].color;
}

export default function PetaClient({ initialRegions }: { initialRegions: any[] }) {
  const [activeFilter, setActiveFilter] = useState("Anomali");
  const [hoverInfo, setHoverInfo] = useState<any>(null);
  const [geoData, setGeoData] = useState<any>(null);

  useEffect(() => {
    fetch("/provinsi.json").then(r => r.json()).then(setGeoData);
  }, []);

  const fillColorExpression = useMemo(() => {
    const matchExpr: any[] = ["match", ["get", "PROVINSI"]];
    initialRegions.forEach(r => {
      let val = 0;
      if (activeFilter === "Rendah")       val = r.rendah;
      else if (activeFilter === "Sedang")  val = r.menengah;
      else if (activeFilter === "Tinggi")  val = r.tinggi;
      else if (activeFilter === "Anomali") val = r.ekstrem;
      else                                  val = r.total;
      matchExpr.push(r.provinsi, getColor(val, activeFilter));
    });
    matchExpr.push("#F1F5F9");
    return matchExpr;
  }, [activeFilter, initialRegions]);

  const onHover = (event: any) => {
    const { features, point: { x, y } } = event;
    const feature = features?.[0];
    if (feature) {
      const prov = feature.properties.PROVINSI;
      const data = initialRegions.find(r => r.provinsi === prov);
      let val = 0;
      if (data) {
        if (activeFilter === "Rendah")       val = data.rendah;
        else if (activeFilter === "Sedang")  val = data.menengah;
        else if (activeFilter === "Tinggi")  val = data.tinggi;
        else if (activeFilter === "Anomali") val = data.ekstrem;
        else                                  val = data.total;
      }
      // Rank among all regions
      const sorted = [...initialRegions].sort((a, b) => {
        const va = activeFilter === "Rendah" ? a.rendah : activeFilter === "Sedang" ? a.menengah : activeFilter === "Tinggi" ? a.tinggi : activeFilter === "Anomali" ? a.ekstrem : a.total;
        const vb = activeFilter === "Rendah" ? b.rendah : activeFilter === "Sedang" ? b.menengah : activeFilter === "Tinggi" ? b.tinggi : activeFilter === "Anomali" ? b.ekstrem : b.total;
        return vb - va;
      });
      const rank = sorted.findIndex(r => r.provinsi === prov) + 1;
      setHoverInfo({ x, y, prov, val, total: data?.total || 0, rank, total_prov: sorted.length });
    } else {
      setHoverInfo(null);
    }
  };

  const steps = LEGEND_STEPS[activeFilter] || [];

  return (
    <div className="flex flex-col" style={{ minHeight: "calc(100vh - 4rem)" }}>
      {/* CONTROL PANEL */}
      <div className="bg-white/85 backdrop-blur-md border-b border-slate-100 px-4 md:px-8 py-3 z-20 shrink-0 shadow-sm">
        <div className="max-w-7xl mx-auto flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <h1 className="font-serif font-bold text-xl text-slate-900">Peta Sebaran Risiko</h1>
            <p className="text-slate-400 text-xs font-sans">3.009.417 paket — hover provinsi untuk detail</p>
          </div>
          <div className="flex flex-col sm:flex-row sm:items-center gap-3">
            {/* Toggle buttons */}
            <div className="flex bg-slate-100 p-1 rounded-xl overflow-x-auto scrollbar-hide gap-0.5">
              {FILTERS.map(f => (
                <button key={f} onClick={() => setActiveFilter(f)}
                  className={`px-3 py-1.5 text-xs font-bold rounded-lg transition-all whitespace-nowrap font-sans ${
                    activeFilter === f ? "bg-white shadow-sm text-slate-900 border border-slate-200" : "text-slate-500 hover:text-slate-700"
                  }`}>
                  {f}
                </button>
              ))}
            </div>
            {/* Quantitative Legend */}
            <div className="flex items-center gap-2 shrink-0">
              <span className="text-[10px] text-slate-400 font-sans">Jumlah paket:</span>
              <div className="flex items-center gap-1">
                {steps.map((s, i) => (
                  <div key={i} className="group relative flex flex-col items-center">
                    <div className="w-5 h-5 rounded-sm border border-white shadow-sm" style={{ backgroundColor: s.color }} />
                    <span className="hidden group-hover:block absolute -top-7 left-1/2 -translate-x-1/2 bg-slate-900 text-white text-[9px] px-1.5 py-0.5 rounded whitespace-nowrap z-50 font-sans">
                      {s.label}
                    </span>
                  </div>
                ))}
                <div className="flex flex-col justify-between text-[9px] text-slate-400 font-sans ml-1">
                  <span>Sedikit</span>
                </div>
                <div className="flex flex-col justify-between text-[9px] text-slate-400 font-sans">
                  <span>Banyak</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* MAP CANVAS — gradient fade top and bottom */}
      <div className="flex-1 relative" style={{ minHeight: "60vh" }}>
        {/* Top gradient fade (transparent at map, solid toward control) */}
        <div className="absolute top-0 left-0 right-0 h-6 z-10 pointer-events-none"
          style={{ background: "linear-gradient(to bottom, rgba(248,250,252,0.4) 0%, rgba(248,250,252,0) 100%)" }} />
        {/* Bottom gradient fade */}
        <div className="absolute bottom-0 left-0 right-0 h-8 z-10 pointer-events-none"
          style={{ background: "linear-gradient(to top, rgba(248,250,252,0.5) 0%, rgba(248,250,252,0) 100%)" }} />

        <Map
          style={{ width: "100%", height: "100%", position: "absolute", inset: 0 }}
          initialViewState={{ longitude: 118, latitude: -2.5, zoom: 4.5 }}
          mapStyle="https://basemaps.cartocdn.com/gl/positron-gl-style/style.json"
          interactiveLayerIds={["provinsi-fill"]}
          onMouseMove={onHover}
          onMouseLeave={() => setHoverInfo(null)}
        >
          <NavigationControl position="bottom-right" />
          {geoData && (
            <Source id="provinsi" type="geojson" data={geoData}>
              <Layer id="provinsi-fill" type="fill" paint={{
                "fill-color": fillColorExpression as any,
                "fill-opacity": 0.85,
                "fill-outline-color": "#ffffff"
              }} />
            </Source>
          )}
        </Map>

        {/* Hover Tooltip */}
        {hoverInfo && (
          <div className="absolute pointer-events-none z-50 font-sans" style={{ left: hoverInfo.x + 12, top: hoverInfo.y - 60 }}>
            <div className="glass-dark rounded-xl px-4 py-3 shadow-2xl min-w-[220px] border border-white/10">
              <div className="font-bold text-sm text-[#26C6DA] mb-1.5 uppercase tracking-wide">{hoverInfo.prov}</div>
              <div className="text-xs text-slate-300 space-y-1 font-sans">
                <div className="flex justify-between gap-6">
                  <span>Paket {activeFilter !== "Total Paket" ? activeFilter : "Total"}:</span>
                  <span className="font-bold text-white">{hoverInfo.val.toLocaleString("id-ID")}</span>
                </div>
                <div className="flex justify-between gap-6">
                  <span>Total paket:</span>
                  <span className="text-slate-300">{hoverInfo.total.toLocaleString("id-ID")}</span>
                </div>
                <div className="flex justify-between gap-6">
                  <span>Peringkat:</span>
                  <span className="font-bold text-[#FFCA28]">#{hoverInfo.rank} dari {hoverInfo.total_prov}</span>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Top-5 mini panel */}
        <div className="absolute top-4 left-4 z-20 glass rounded-xl p-4 border border-white/40 shadow-xl min-w-[200px] hidden lg:block">
          <div className="flex items-center gap-2 mb-3">
            <Info className="w-3.5 h-3.5 text-slate-400" />
            <span className="text-xs font-bold text-slate-600 font-sans uppercase tracking-wider">Top 5 - {activeFilter}</span>
          </div>
          {[...initialRegions]
            .sort((a, b) => {
              const va = activeFilter === "Rendah" ? a.rendah : activeFilter === "Sedang" ? a.menengah : activeFilter === "Tinggi" ? a.tinggi : activeFilter === "Anomali" ? a.ekstrem : a.total;
              const vb = activeFilter === "Rendah" ? b.rendah : activeFilter === "Sedang" ? b.menengah : activeFilter === "Tinggi" ? b.tinggi : activeFilter === "Anomali" ? b.ekstrem : b.total;
              return vb - va;
            })
            .slice(0, 5)
            .map((r, i) => {
              const v = activeFilter === "Rendah" ? r.rendah : activeFilter === "Sedang" ? r.menengah : activeFilter === "Tinggi" ? r.tinggi : activeFilter === "Anomali" ? r.ekstrem : r.total;
              return (
                <div key={r.provinsi} className="flex items-center justify-between gap-3 py-1 border-b border-slate-100 last:border-0">
                  <div className="flex items-center gap-2">
                    <span className="text-[10px] font-bold text-slate-400 font-sans w-3">{i+1}</span>
                    <span className="text-xs text-slate-700 font-sans truncate max-w-[100px]">{r.provinsi}</span>
                  </div>
                  <span className="text-xs font-bold font-mono text-slate-800">{v.toLocaleString("id-ID")}</span>
                </div>
              );
            })}
        </div>
      </div>
    </div>
  );
}
'''
with open(os.path.join(FRONTEND_APP, "peta/PetaClient.tsx"), "w", encoding="utf-8") as f:
    f.write(peta_tsx)

print("PetaClient done")
