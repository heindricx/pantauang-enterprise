export const dynamic = 'force-dynamic';

async function fetchSSR(endpoint: string) {
  try {
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || "https://heindricx-pantauang-backend.hf.space";
    const res = await fetch(`${apiUrl}${endpoint}`, { cache: 'no-store' });
    if (!res.ok) return null;
    return await res.json();
  } catch (e) {
    console.error("SSR Fetch Error for", endpoint, e);
    return null;
  }
}

import HomeClient from "./HomeClient";

export default async function Home() {
  const ticker = await fetchSSR("/api/ticker") || [];
  const metrics = await fetchSSR("/dashboard/metrics") || null;
  
  return <HomeClient tickerData={ticker} metricsData={metrics} />;
}
