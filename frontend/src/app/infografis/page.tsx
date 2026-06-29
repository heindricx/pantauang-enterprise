
async function fetchSSR(endpoint: string) {
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
  return <InfografisClient metricsData={metrics} />;
}
