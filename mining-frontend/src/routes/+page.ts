import { type LineDelay, apiUrl } from "$lib/stores";

export async function load() {
  const getLineDelays = async () => {
    const res = await fetch(`${apiUrl}/lines/prime`);
    if (!res.ok) throw new Error(`failed to fetch line delays: ${res.body}`);
    const body = (await res.json()) as LineDelay[];
    return body;
  };
  return { delays: getLineDelays() };
}
