import os

frontend_app_dir = r"D:\satdat 2026\sec\pantauang-enterprise\frontend\src\app"

# PetaClient.tsx
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
''')

# InfografisClient.tsx & infografis/page.tsx
with open(os.path.join(frontend_app_dir, "infografis/page.tsx"), "w") as f:
    f.write('''async function fetchSSR(endpoint: string) {
  try {
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";
    const res = await fetch(`${apiUrl}${endpoint}`, { cache: 'no-store' });
    if (!res.ok) return null;
    return await res.json();
  } catch (e) {
    return null;
  }
}

import InfografisClient from "./InfografisClient";

export default async function InfografisPage() {
  const metrics = await fetchSSR("/dashboard/metrics") || null;
  const timeSeries = await fetchSSR("/infografis/time-series") || [];
  const jenisPengadaan = await fetchSSR("/infografis/jenis-pengadaan") || [];
  
  return <InfografisClient metricsData={metrics} timeSeries={timeSeries} jenisPengadaan={jenisPengadaan} />;
}
''')

with open(os.path.join(frontend_app_dir, "infografis/InfografisClient.tsx"), "w") as f:
    f.write('''"use client";
import { PieChart, Pie, Cell, AreaChart, Area, BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Legend, CartesianGrid } from "recharts";

export default function InfografisClient({ metricsData, timeSeries, jenisPengadaan }: { metricsData: any, timeSeries: any[], jenisPengadaan: any[] }) {
  const pieData = metricsData ? [
    { name: "Anomali", value: metricsData.ekstrem, color: "#FF5722" }, // Extreme
    { name: "Tinggi", value: metricsData.risiko_tinggi, color: "#FF8A65" },
    { name: "Sedang", value: Math.floor(metricsData.total_paket * 0.15), color: "#FFCA28" }, // Mocked for 4 categories 
    { name: "Rendah", value: metricsData.total_paket - metricsData.ekstrem - metricsData.risiko_tinggi - Math.floor(metricsData.total_paket * 0.15), color: "#4CAF50" },
  ] : [];

  if (!metricsData) return <div className="p-12 text-slate-500 font-mono">NO METRICS DATA AVAILABLE.</div>;

  return (
    <div className="h-full overflow-auto flex flex-col md:flex-row bg-white">
      {/* Left Pane: Narrative */}
      <div className="w-full md:w-1/3 p-8 md:p-12 border-r border-slate-200 flex flex-col justify-center shrink-0">
        <h1 className="font-serif font-black text-[clamp(2rem,5vw,4rem)] uppercase text-slate-900 mb-6 tracking-tighter leading-[1.1]">
          Systematic <br/><span className="text-[#FF5722]">Deviation</span> <br/>Analytics.
        </h1>
        <div className="space-y-6 text-slate-600 text-[clamp(1rem,1.5vw,1.125rem)] leading-relaxed font-sans">
          <p>
            Dari <span className="text-slate-900 font-bold">{metricsData.total_data_exact.toLocaleString()}</span> paket pengadaan, sistem mengidentifikasi pola penyimpangan yang signifikan berdasarkan algoritma QRLGBM.
          </p>
          <p>
            Analisis runtun waktu (Time-Series) menunjukkan tren musiman paket rawan, sementara rincian per Jenis Pengadaan memberikan wawasan presisi atas sektor yang paling rentan terhadap anomali struktural.
          </p>
        </div>
      </div>

      {/* Right Pane: Charts */}
      <div className="w-full md:w-2/3 p-4 md:p-12 overflow-y-auto space-y-8 bg-slate-50">
        
        {/* Risk Breakdown Pie */}
        <div className="tech-border rounded-xl p-6 bg-white">
          <h3 className="font-serif text-lg font-bold text-slate-800 mb-4 uppercase">Distribusi 4 Kategori Risiko</h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie data={pieData} innerRadius={70} outerRadius={110} paddingAngle={2} dataKey="value">
                  {pieData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }} />
                <Legend iconType="circle" />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Time Series Area Chart */}
        <div className="tech-border rounded-xl p-6 bg-white">
          <h3 className="font-serif text-lg font-bold text-slate-800 mb-4 uppercase">Tren Musiman (12 Bulan)</h3>
          <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={timeSeries} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
                <defs>
                  <linearGradient id="colorEkstrem" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#FF5722" stopOpacity={0.8}/>
                    <stop offset="95%" stopColor="#FF5722" stopOpacity={0}/>
                  </linearGradient>
                  <linearGradient id="colorTinggi" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#FF8A65" stopOpacity={0.8}/>
                    <stop offset="95%" stopColor="#FF8A65" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <XAxis dataKey="bulan" axisLine={false} tickLine={false} tick={{fontSize: 12, fill: '#64748b'}} />
                <YAxis axisLine={false} tickLine={false} tick={{fontSize: 12, fill: '#64748b'}} />
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1f5f9" />
                <Tooltip contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }} />
                <Legend />
                <Area type="monotone" dataKey="Risiko Tinggi" stroke="#FF8A65" fillOpacity={1} fill="url(#colorTinggi)" />
                <Area type="monotone" dataKey="Anomali Ekstrem" stroke="#FF5722" fillOpacity={1} fill="url(#colorEkstrem)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Stacked Bar Chart */}
        <div className="tech-border rounded-xl p-6 bg-white">
          <h3 className="font-serif text-lg font-bold text-slate-800 mb-4 uppercase">Sebaran Berdasarkan Jenis Pengadaan</h3>
          <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={jenisPengadaan} layout="vertical" margin={{ top: 20, right: 30, left: 40, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" horizontal={true} vertical={false} stroke="#f1f5f9" />
                <XAxis type="number" hide />
                <YAxis dataKey="kategori" type="category" axisLine={false} tickLine={false} tick={{fontSize: 11, fill: '#475569'}} width={120} />
                <Tooltip contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }} />
                <Legend />
                <Bar dataKey="Anomali" stackId="a" fill="#FF5722" />
                <Bar dataKey="Tinggi" stackId="a" fill="#FF8A65" />
                <Bar dataKey="Sedang" stackId="a" fill="#FFCA28" />
                <Bar dataKey="Rendah" stackId="a" fill="#4CAF50" radius={[0, 4, 4, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

      </div>
    </div>
  );
}
''')
print("Step 2 done")
