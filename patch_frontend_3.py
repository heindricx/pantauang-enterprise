import os

frontend_app_dir = r"D:\satdat 2026\sec\pantauang-enterprise\frontend\src\app"
frontend_components_dir = r"D:\satdat 2026\sec\pantauang-enterprise\frontend\src\components"

# 1. layout.tsx - Remove Plus Jakarta Sans, use Segoe UI
with open(os.path.join(frontend_app_dir, "layout.tsx"), "w") as f:
    f.write('''import type { Metadata } from "next";
import { Playfair_Display } from "next/font/google";
import "./globals.css";
import { Navbar } from "@/components/layout/Navbar";

const playfair = Playfair_Display({ subsets: ["latin"], variable: "--font-playfair" });

export const metadata: Metadata = {
  title: "PantaUang Kita | Intelligence Dashboard",
  description: "Government Intelligence Dashboard for public procurement anomaly detection.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="id" className={`light ${playfair.variable}`}>
      <body className="font-sans bg-slate-50 text-slate-800 overflow-hidden flex flex-col h-screen">
        <Navbar />
        <main className="flex-1 relative overflow-auto bg-slate-50 w-full">
          {children}
        </main>
      </body>
    </html>
  );
}
''')

# 2. globals.css - Add Segoe UI
with open(os.path.join(frontend_app_dir, "globals.css"), "w") as f:
    f.write('''@import "tailwindcss";

@layer base {
  :root {
    --background: #f8fafc;
    --foreground: #1e293b;
    
    --cp-blue: #1E88E5;      
    --cp-coral: #FF8A65;     
    --cp-purple: #7E57C2;    
    --cp-orange: #FF5722;    
    --cp-cyan: #26C6DA;      
  }
  
  html {
    scroll-behavior: smooth;
  }
  
  body {
    background-color: var(--background);
    color: var(--foreground);
    overflow-x: hidden;
  }
}

.font-sans {
  font-family: "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
}

.font-serif {
  font-family: var(--font-playfair), serif;
}

.scrollbar-hide::-webkit-scrollbar {
    display: none;
}
.scrollbar-hide {
    -ms-overflow-style: none;
    scrollbar-width: none;
}

.tech-border {
    border: 1px solid rgba(148, 163, 184, 0.3);
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
    background: #ffffff;
}
''')

# 3. PetaClient.tsx - Fix Choropleth math, add Legend, move title outside
with open(os.path.join(frontend_app_dir, "peta/PetaClient.tsx"), "w") as f:
    f.write('''"use client";
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
    <div className="h-full w-full flex flex-col bg-slate-50 relative">
      {/* Container header diluar map agar tidak tertumpuk */}
      <div className="bg-white px-6 py-4 border-b border-slate-200 z-10 flex flex-col md:flex-row items-center justify-between shadow-sm shrink-0">
        <div className="text-center md:text-left mb-4 md:mb-0 w-full md:w-auto">
          <h1 className="font-serif font-black text-2xl uppercase text-slate-800">Peta Sebaran Risiko</h1>
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

      <div className="flex-1 w-full relative min-h-[400px]">
        <Map
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
''')

print("Patch applied")
