async function fetchSSR(endpoint: string) {
  try {
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || "https://heindricx-pantauang-backend.hf.space";
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
