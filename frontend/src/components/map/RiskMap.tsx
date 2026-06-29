"use client";
import { useEffect, useRef, useState } from "react";
import maplibregl from "maplibre-gl";
import "maplibre-gl/dist/maplibre-gl.css";

export default function RiskMap() {
  const mapContainer = useRef<HTMLDivElement>(null);
  const map = useRef<maplibregl.Map | null>(null);
  const [lng] = useState(113.9213);
  const [lat] = useState(-0.7893);
  const [zoom] = useState(4);

  useEffect(() => {
    if (map.current || !mapContainer.current) return; // initialize map only once
    
    map.current = new maplibregl.Map({
      container: mapContainer.current,
      style: "https://basemaps.cartocdn.com/gl/positron-gl-style/style.json",
      center: [lng, lat],
      zoom: zoom,
      pitch: 45,
    });

    map.current.on("load", () => {
      // Add 3D building layer if needed, or risk choropleth
      // Placeholder for national data aggregation
      map.current?.addSource("risk-data", {
        type: "geojson",
        data: {
          type: "FeatureCollection",
          features: []
        }
      });
    });
  }, [lng, lat, zoom]);

  return (
    <div className="w-full h-full relative rounded-xl overflow-hidden border border-slate-200 shadow-sm">
      <div ref={mapContainer} className="absolute inset-0" />
      <div className="absolute top-4 left-4 bg-white/90 backdrop-blur-md p-4 rounded-lg shadow-md border border-slate-200 z-10">
        <h3 className="font-bold text-slate-800">Peta Risiko Nasional</h3>
        <p className="text-sm text-slate-500">Visualisasi 3D Pengadaan</p>
      </div>
    </div>
  );
}
