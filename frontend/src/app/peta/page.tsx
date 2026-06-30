export const dynamic = 'force-dynamic';

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

import PetaClient from "./PetaClient";

export default async function PetaPage() {
  const regions = await fetchSSR("/api/map-regions") || [];
  return <PetaClient initialRegions={regions} />;
}
