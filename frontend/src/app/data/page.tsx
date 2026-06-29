
async function fetchSSR(endpoint: string) {
  try {
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";
    const res = await fetch(`${apiUrl}${endpoint}`, { cache: 'no-store' });
    if (!res.ok) return null;
    return await res.json();
  } catch (e) {
    console.error("SSR Fetch Error for", endpoint, e);
    return null;
  }
}

import DataClient from "./DataClient";

export default async function DataPage() {
  const data = await fetchSSR("/procurement?limit=100") || { data: [] };
  
  return <DataClient initialData={data.data} />;
}
