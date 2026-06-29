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
    
    // Extract all values for the active filter to calculate percentiles (so gradient is visible)
    const values = initialRegions.map(r => {
      if (activeFilter === "Rendah") return r.rendah;
      if (activeFilter === "Sedang") return r.menengah;
      if (activeFilter === "Tinggi") return r.tinggi;
      if (activeFilter === "Anomali") return r.ekstrem;
      return r.total;
    }).sort((a, b) => a - b);
    
    const getPercentile = (val: number) => {
      const idx = values.findIndex(v => v >= val);
      return idx / values.length;
    };

    initialRegions.forEach(r => {
      let val = 0;
      if (activeFilter === "Rendah") val = r.rendah;
      else if (activeFilter === "Sedang") val = r.menengah;
      else if (activeFilter === "Tinggi") val = r.tinggi;
      else if (activeFilter === "Anomali") val = r.ekstrem;
      else if (activeFilter === "Total Paket") val = r.total;
      
      const ratio = getPercentile(val); // Ratio is based on ranking, not absolute value!
      
      let color = "#e2e8f0"; // default slate-200
      if (val > 0) {
        if (activeFilter === "Rendah") {
          color = ratio > 0.8 ? "#FBC02D" : ratio > 0.6 ? "#81C784" : ratio > 0.4 ? "#4DB6AC" : ratio > 0.2 ? "#29B6F6" : "#1E88E5";
        } else if (activeFilter === "Sedang") {
          color = ratio > 0.8 ? "#E65100" : ratio > 0.6 ? "#F57C00" : ratio > 0.4 ? "#FF9800" : ratio > 0.2 ? "#FFB74D" : "#FFE0B2";
        } else if (activeFilter === "Tinggi") {
          color = ratio > 0.8 ? "#BF360C" : ratio > 0.6 ? "#D84315" : ratio > 0.4 ? "#F4511E" : ratio > 0.2 ? "#FF8A65" : "#FFCCBC";
        } else if (activeFilter === "Anomali") {
          color = ratio > 0.8 ? "#b91c1c" : ratio > 0.6 ? "#dc2626" : ratio > 0.4 ? "#ef4444" : ratio > 0.2 ? "#f87171" : "#fca5a5";
        } else {
          color = ratio > 0.8 ? "#4A148C" : ratio > 0.6 ? "#6A1B9A" : ratio > 0.4 ? "#8E24AA" : ratio > 0.2 ? "#AB47BC" : "#D1C4E9";
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

  const renderLegend = () => {
    let colors = [];
    if (activeFilter === "Rendah") colors = ["#1E88E5", "#29B6F6", "#4DB6AC", "#81C784", "#FBC02D"];
    else if (activeFilter === "Sedang") colors = ["#FFE0B2", "#FFB74D", "#FF9800", "#F57C00", "#E65100"];
    else if (activeFilter === "Tinggi") colors = ["#FFCCBC", "#FF8A65", "#F4511E", "#D84315", "#BF360C"];
    else if (activeFilter === "Anomali") colors = ["#fca5a5", "#f87171", "#ef4444", "#dc2626", "#b91c1c"];
    else colors = ["#D1C4E9", "#AB47BC", "#8E24AA", "#6A1B9A", "#4A148C"];

    return (
      <div className="flex items-center gap-2 mt-4 md:mt-0 text-xs font-sans">
        <span className="text-slate-500">Sedikit</span>
        <div className="flex h-3 w-32 rounded overflow-hidden">
          {colors.map((c, i) => <div key={i} className="flex-1" style={{backgroundColor: c}}></div>)}
        </div>
        <span className="text-slate-500">Banyak</span>
      </div>
    );
  };

  return (
    <div className="min-h-[calc(100vh-4rem)] w-full flex flex-col bg-slate-50 relative">
      {/* Container header diluar map agar tidak tertumpuk */}
      <div className="bg-white px-6 py-4 border-b border-slate-200 z-10 flex flex-col md:flex-row items-center justify-between shadow-sm shrink-0">
        <div className="text-center md:text-left mb-4 md:mb-0 w-full md:w-auto">
          <h1 className="font-serif font-black text-2xl capitalize text-slate-800">Peta Sebaran Risiko</h1>
          <p className="text-slate-500 text-sm font-sans mt-1">Pilih kategori untuk melihat gradasi wilayah</p>
        </div>
        
        <div className="flex flex-col items-center md:items-end w-full md:w-auto">
          <div className="flex bg-slate-100 p-1 rounded-lg w-full md:w-auto overflow-x-auto scrollbar-hide">
            {filters.map(f => (
              <button 
                key={f}
                onClick={() => setActiveFilter(f)}
                className={`px-3 py-1.5 md:px-4 md:py-2 text-xs md:text-sm font-bold rounded-md transition-all whitespace-nowrap ${activeFilter === f ? 'bg-white shadow-sm text-slate-900 border border-slate-200' : 'text-slate-500 hover:text-slate-700'}`}
              >
                {f}
              </button>
            ))}
          </div>
          {renderLegend()}
        </div>
      </div>

      <div className="flex-1 w-full relative min-h-[60vh]">
        <Map
          style={{ width: "100%", height: "100%", position: "absolute", inset: 0 }}
          initialViewState={{ longitude: 118, latitude: -2.5, zoom: 4.5 }}
          mapStyle="https://basemaps.cartocdn.com/gl/positron-gl-style/style.json"
          interactiveLayerIds={["provinsi-fill"]}
          onMouseMove={onHover}
          onMouseLeave={() => setHoverInfo(null)}
          dragPan={true}
          scrollZoom={true}
        >
          <NavigationControl position="bottom-right" />
          
          {geoData && (
            <Source id="provinsi" type="geojson" data={geoData}>
              <Layer 
                id="provinsi-fill" 
                type="fill" 
                paint={{
                  "fill-color": fillColorExpression as any,
                  "fill-opacity": 0.85,
                  "fill-outline-color": "#ffffff"
                }} 
              />
            </Source>
          )}
        </Map>

        {hoverInfo && (
          <div 
            className="absolute bg-slate-900 text-white p-3 rounded-lg shadow-xl pointer-events-none z-50 text-xs font-sans transform -translate-x-1/2 -translate-y-full mt-[-10px] min-w-[200px]"
            style={{ left: hoverInfo.x, top: hoverInfo.y }}
          >
            <div className="font-bold text-sm mb-1 text-[#26C6DA] uppercase">{hoverInfo.prov}</div>
            <div className="text-slate-200">
              Total Paket {activeFilter !== "Total Paket" ? `Risiko ${activeFilter}` : ""}: 
              <br/>
              <span className="font-bold text-white text-lg">{hoverInfo.val.toLocaleString()}</span> <span className="text-slate-400">dari {hoverInfo.total.toLocaleString()} paket</span>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
