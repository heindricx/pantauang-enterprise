
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

import AboutClient from "./AboutClient";

export default async function AboutPage() {
  const stats = await fetchSSR("/api/methodology-stats") || null;
  return <AboutClient stats={stats} />;
}
