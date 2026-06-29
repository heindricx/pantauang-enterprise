"use client";
import Map, { NavigationControl, Source, Layer } from "react-map-gl/maplibre";
import "maplibre-gl/dist/maplibre-gl.css";
import { useState, useMemo, useEffect } from "react";

export default function PetaClient({ initialRegions }: { initialRegions: any[] }) {
  const [activeFilter, setActiveFilter] = useState("Rendah");
  const [hoverInfo, setHoverInfo] = useState<any>(null);
  const [geoData, setGeoData] = useState<any>(null);

  const filters = ["Rendah", "Sedang", "Tinggi", "Anomali", "Total Paket"];

  useEffect(() => {
    fetch("/provinsi.json")
      .then(r => r.json())
      .then(d => setGeoData(d));
  }, []);

  const fillColorExpression = useMemo(() => {
    const matchExpr: any[] = ["match", ["get", "PROVINSI"]];
    
    // Normalize data for color scale
    let maxVal = 1;
    initialRegions.forEach(r => {
      let val = 0;
      if (activeFilter === "Rendah") val = r.rendah;
      else if (activeFilter === "Sedang") val = r.menengah;
      else if (activeFilter === "Tinggi") val = r.tinggi;
      else if (activeFilter === "Anomali") val = r.ekstrem;
      else if (activeFilter === "Total Paket") val = r.total;
      if (val > maxVal) maxVal = val;
    });

    initialRegions.forEach(r => {
      let val = 0;
      if (activeFilter === "Rendah") val = r.rendah;
      else if (activeFilter === "Sedang") val = r.menengah;
      else if (activeFilter === "Tinggi") val = r.tinggi;
      else if (activeFilter === "Anomali") val = r.ekstrem;
      else if (activeFilter === "Total Paket") val = r.total;
      
      const ratio = maxVal > 0 ? val / maxVal : 0;
      
      let color = "#e2e8f0"; // default slate-200
      if (val > 0) {
        if (activeFilter === "Rendah") {
          // Cool Blue to Warm Yellow
          color = ratio > 0.8 ? "#FBC02D" : ratio > 0.5 ? "#4DB6AC" : "#1E88E5";
        } else if (activeFilter === "Sedang") {
          color = ratio > 0.8 ? "#F57C00" : ratio > 0.5 ? "#FFB74D" : "#FFE0B2";
        } else if (activeFilter === "Tinggi") {
          color = ratio > 0.8 ? "#D84315" : ratio > 0.5 ? "#FF8A65" : "#FFCCBC";
        } else if (activeFilter === "Anomali") {
          color = ratio > 0.8 ? "#B71C1C" : ratio > 0.5 ? "#E53935" : "#FFCDD2";
        } else {
          color = ratio > 0.8 ? "#4A148C" : ratio > 0.5 ? "#7E57C2" : "#D1C4E9";
        }
      }
      matchExpr.push(r.provinsi, color);
    });
    
    matchExpr.push("#e2e8f0"); // default
    return matchExpr;
  }, [activeFilter, initialRegions]);

  const onHover = (event: any) => {
    const { features, point: { x, y } } = event;
    const hoveredFeature = features && features[0];
    if (hoveredFeature) {
      const prov = hoveredFeature.properties.PROVINSI;
      const data = initialRegions.find(r => r.provinsi === prov);
      let val = 0;
      if (data) {
        if (activeFilter === "Rendah") val = data.rendah;
        else if (activeFilter === "Sedang") val = data.menengah;
        else if (activeFilter === "Tinggi") val = data.tinggi;
        else if (activeFilter === "Anomali") val = data.ekstrem;
        else if (activeFilter === "Total Paket") val = data.total;
      }
      setHoverInfo({ x, y, prov, val, total: data?.total || 0 });
    } else {
      setHoverInfo(null);
    }
  };

  return (
    <div className="h-full w-full flex flex-col relative">
      <div className="bg-white p-4 border-b border-slate-200 z-10 flex flex-wrap gap-2 justify-center shadow-sm">
        <h2 className="w-full text-center font-serif font-black text-xl mb-2 uppercase text-slate-800">Spatial Risk Intelligence</h2>
        <div className="flex bg-slate-100 p-1 rounded-lg">
          {filters.map(f => (
            <button 
              key={f}
              onClick={() => setActiveFilter(f)}
              className={`px-4 py-2 text-sm font-bold rounded-md transition-all ${activeFilter === f ? 'bg-white shadow-sm text-slate-900 border border-slate-200' : 'text-slate-500 hover:text-slate-700'}`}
            >
              {f}
            </button>
          ))}
        </div>
      </div>

      <div className="flex-1 w-full relative">
        <Map
          initialViewState={{ longitude: 118, latitude: -2.5, zoom: 4.5 }}
          mapStyle="https://basemaps.cartocdn.com/gl/positron-gl-style/style.json"
          interactiveLayerIds={["provinsi-fill"]}
          onMouseMove={onHover}
          onMouseLeave={() => setHoverInfo(null)}
        >
          <NavigationControl position="bottom-right" />
          
          {geoData && (
            <Source id="provinsi" type="geojson" data={geoData}>
              <Layer 
                id="provinsi-fill" 
                type="fill" 
                paint={{
                  "fill-color": fillColorExpression as any,
                  "fill-opacity": 0.75,
                  "fill-outline-color": "#ffffff"
                }} 
              />
            </Source>
          )}
        </Map>

        {hoverInfo && (
          <div 
            className="absolute bg-slate-900 text-white p-3 rounded-lg shadow-xl pointer-events-none z-50 text-xs font-sans transform -translate-x-1/2 -translate-y-full mt-[-10px]"
            style={{ left: hoverInfo.x, top: hoverInfo.y }}
          >
            <div className="font-bold text-sm mb-1 text-[#26C6DA] uppercase">{hoverInfo.prov}</div>
            <div className="text-slate-200">
              Total Paket {activeFilter !== "Total Paket" ? `Risiko ${activeFilter}` : ""}: 
              <span className="font-bold text-white ml-1">{hoverInfo.val.toLocaleString()}</span> dari {hoverInfo.total.toLocaleString()} paket
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
