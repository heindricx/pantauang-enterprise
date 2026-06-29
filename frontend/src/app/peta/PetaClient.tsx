"use client";
import Map, { NavigationControl, Marker } from "react-map-gl/maplibre";
import "maplibre-gl/dist/maplibre-gl.css";
import { MapPin } from "lucide-react";

export default function PetaClient({ initialRegions }: { initialRegions: any[] }) {
  // Mock coordinates for regions for visual purpose
  const coords: any = {
    "Jawa Barat": { lat: -6.9, lng: 107.6 },
    "Jawa Timur": { lat: -7.2, lng: 112.7 },
    "DKI Jakarta": { lat: -6.2, lng: 106.8 },
    "Jawa Tengah": { lat: -7.0, lng: 110.4 },
    "Sumatera Utara": { lat: 3.5, lng: 98.6 }
  };

  return (
    <div className="h-full w-full flex relative">
      <div className="w-80 h-full bg-white/95 backdrop-blur-xl border-r border-slate-200 flex flex-col absolute left-0 top-0 z-10 shadow-lg">
        <header className="p-6 border-b border-slate-100">
          <h2 className="text-xl font-bold uppercase tracking-widest text-slate-800">Spatial Risk</h2>
          <p className="text-xs font-mono text-[#26C6DA] mt-1 font-bold">Top 5 Endangered Regions</p>
        </header>
        <div className="flex-1 overflow-auto p-4 space-y-4">
          {initialRegions.slice(0, 5).map((r: any, idx) => (
            <div key={idx} className="bg-slate-50 border border-slate-200 rounded-lg p-4 cursor-pointer hover:bg-white hover:shadow-md transition-all group">
              <div className="flex items-center justify-between mb-2">
                <h3 className="font-bold text-slate-700 group-hover:text-[#1E88E5] transition-colors flex items-center gap-2">
                  <span className="text-xs bg-[#FF5722] text-white px-1.5 py-0.5 rounded font-mono">#{idx+1}</span>
                  {r.provinsi}
                </h3>
                <MapPin className="w-4 h-4 text-slate-400 group-hover:text-[#1E88E5]" />
              </div>
              <div className="flex justify-between items-end mt-4 font-mono text-xs text-slate-500">
                <div>
                  <div className="uppercase text-[10px] text-slate-400">Incidents</div>
                  <div className="text-[#FF5722] font-bold">{r.incident_count} Flags</div>
                </div>
                <div className="text-right">
                  <div className="uppercase text-[10px] text-slate-400">Budget at Risk</div>
                  <div className="text-slate-800 font-bold">Rp {(r.total_budget / 1e12).toFixed(1)}T</div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="flex-1 w-full h-full bg-slate-100">
        <Map
          initialViewState={{ longitude: 118, latitude: -2.5, zoom: 4.5 }}
          mapStyle="https://basemaps.cartocdn.com/gl/positron-gl-style/style.json"
        >
          <NavigationControl position="bottom-right" />
          {initialRegions.map((r, i) => {
            const loc = coords[r.provinsi];
            if (!loc) return null;
            return (
              <Marker key={i} longitude={loc.lng} latitude={loc.lat}>
                <div className="bg-[#FF5722]/20 p-2 rounded-full animate-pulse">
                  <div className="bg-[#FF5722] w-4 h-4 rounded-full shadow-lg border-2 border-white"></div>
                </div>
              </Marker>
            );
          })}
        </Map>
      </div>
    </div>
  );
}
