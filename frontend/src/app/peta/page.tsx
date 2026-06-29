"use client";
import { useEffect, useState } from "react";
import Map, { NavigationControl } from "react-map-gl/maplibre";
import "maplibre-gl/dist/maplibre-gl.css";
import { MapPin, AlertTriangle } from "lucide-react";

export default function PetaPage() {
  const [regions, setRegions] = useState([]);
  
  useEffect(() => {
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
    fetch(`${apiUrl}/api/map-regions`).then(res => res.json()).then(setRegions).catch(console.error);
  }, []);

  return (
    <div className="h-full w-full flex relative">
      {/* Sidebar Top 5 Regions */}
      <div className="w-80 h-full bg-[#070b14]/90 backdrop-blur-xl border-r border-slate-800 flex flex-col absolute left-0 top-0 z-10">
        <header className="p-6 border-b border-slate-800">
          <h2 className="text-xl font-bold uppercase tracking-widest text-white">Spatial Risk</h2>
          <p className="text-xs font-mono text-slate-500 mt-1">Top 5 Endangered Regions</p>
        </header>
        <div className="flex-1 overflow-auto p-4 space-y-4">
          {regions.slice(0, 5).map((r: any, idx) => (
            <div key={idx} className="bg-slate-900/80 border border-red-900/50 rounded-lg p-4 cursor-pointer hover:bg-slate-800 transition-colors group">
              <div className="flex items-center justify-between mb-2">
                <h3 className="font-bold text-white group-hover:text-[#52C7D8] transition-colors flex items-center gap-2">
                  <span className="text-xs bg-red-900 text-red-200 px-1.5 py-0.5 rounded font-mono">#{idx+1}</span>
                  {r.provinsi}
                </h3>
                <MapPin className="w-4 h-4 text-slate-600 group-hover:text-[#52C7D8]" />
              </div>
              <div className="flex justify-between items-end mt-4 font-mono text-xs text-slate-400">
                <div>
                  <div className="uppercase text-[10px] text-slate-600">Incidents</div>
                  <div className="text-red-400 font-bold">{r.incident_count} Flags</div>
                </div>
                <div className="text-right">
                  <div className="uppercase text-[10px] text-slate-600">Budget at Risk</div>
                  <div className="text-white">Rp {(r.total_budget / 1e12).toFixed(1)}T</div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Mapbox Canvas */}
      <div className="flex-1 w-full h-full">
        <Map
          initialViewState={{ longitude: 118, latitude: -2.5, zoom: 4.5 }}
          mapStyle="https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json"
        >
          <NavigationControl position="bottom-right" />
          
          {/* We would render actual GeoJSON polygons here, but we'll use a placeholder overlay to simulate the map loaded state for now */}
          <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 bg-black/60 backdrop-blur-md px-6 py-4 rounded-xl border border-slate-800 flex items-center gap-4 animate-pulse">
            <AlertTriangle className="w-8 h-8 text-yellow-500" />
            <div>
              <h3 className="text-white font-bold font-mono">MAP TILE SERVER ACTIVE</h3>
              <p className="text-slate-400 text-xs">Waiting for Vector Tiles Rendering...</p>
            </div>
          </div>
        </Map>
      </div>
    </div>
  );
}
