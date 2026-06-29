import os

frontend_src_dir = r"D:\satdat 2026\sec\pantauang-enterprise\frontend\src"
backend_dir = r"D:\satdat 2026\sec\pantauang-enterprise\backend"

# 1. MapLibre GL Component
map_component = os.path.join(frontend_src_dir, "components/map/RiskMap.tsx")
with open(map_component, "w") as f:
    f.write('''"use client";
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
''')

map_page = os.path.join(frontend_src_dir, "app/risk-map/page.tsx")
with open(map_page, "w") as f:
    f.write('''import { Sidebar } from "@/components/layout/Sidebar";
import RiskMap from "@/components/map/RiskMap";

export default function RiskMapPage() {
  return (
    <div className="flex h-screen bg-slate-50 overflow-hidden">
      <Sidebar />
      <div className="flex-1 flex flex-col ml-64">
        <header className="h-16 bg-white border-b border-slate-200 flex items-center px-8 shadow-sm z-10">
          <h2 className="text-lg font-semibold text-slate-800">Peta Risiko Interaktif</h2>
        </header>
        <main className="flex-1 p-6 relative">
          <RiskMap />
        </main>
      </div>
    </div>
  );
}
''')

# 2. Backend Dockerfile
dockerfile = os.path.join(backend_dir, "Dockerfile")
with open(dockerfile, "w") as f:
    f.write('''FROM python:3.13-slim

WORKDIR /app

# System dependencies for LightGBM and others
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
''')

# 3. Docker Compose (root)
root_dir = r"D:\satdat 2026\sec\pantauang-enterprise"
docker_compose = os.path.join(root_dir, "docker-compose.yml")
with open(docker_compose, "w") as f:
    f.write('''version: '3.8'

services:
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - WORKERS=4
    restart: unless-stopped
    depends_on:
      - redis

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    restart: always

  celery_worker:
    build:
      context: ./backend
      dockerfile: Dockerfile
    command: celery -A app.worker.celery_app worker --loglevel=info
    depends_on:
      - backend
      - redis
    restart: unless-stopped
''')

print("MapLibre GL and Docker setup scaffolded successfully!")
