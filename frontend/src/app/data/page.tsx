async function fetchSSR(endpoint: string) {
  try {
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || "https://heindricx-pantauang-backend.hf.space";
    const res = await fetch(`${apiUrl}${endpoint}`, { cache: "no-store" });
    if (!res.ok) return null;
    return await res.json();
  } catch { return null; }
}

import DataClient from "./DataClient";

export default async function DataPage() {
  const filterOptions = await fetchSSR("/procurement/filters") || { provinsi: [], metode: [] };
  return <DataClient filterOptions={filterOptions} />;
}
