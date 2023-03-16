/** @type {import('./$types').PageLoad} */
export async function load({ params }) {
	const getStationDelays = async () => {
		const res = await fetch("http://localhost:3000/stations");
		if (!res.ok) throw new Error(`failed to fetch station delays: ${res.body}`);
		const body = (await res.json()) as StationDelay[];
		return body;
	};
	return { delays: getStationDelays() };
}

type StationDelay = {
	name: string;
	line: string;
	avg_delay: number;
};
