import { type StationDelay, apiUrl } from "$lib/stores";
/** @type {import('./$types').PageLoad} */
export async function load() {
	const getStationDelays = async () => {
		const res = await fetch(`${apiUrl}/stations`);
		if (!res.ok) throw new Error(`failed to fetch station delays: ${res.body}`);
		const body = (await res.json()) as StationDelay[];
		return body;
	};
	return { delays: getStationDelays() };
}

export async function _load_date(date: String) {
	const getStationDelays = async () => {
		const url = `${apiUrl}/stations/date?date=${date}`;
		const res = await fetch(url);
		if (!res.ok) throw new Error(`failed to fetch station delays: ${res.body}`);
		const body = (await res.json()) as StationDelay[];
		return body;
	};
	return { delays: getStationDelays() };
}

export async function _load_timeframe(lower: String, upper: String) {
	const getStationDelays = async () => {
		const url = `${apiUrl}/stations/timeframe?lower_limit=${lower}&upper_limit=${upper}`;
		const res = await fetch(encodeURI(url));
		if (!res.ok) throw new Error(`failed to fetch station delays: ${res.body}`);
		const body = (await res.json()) as StationDelay[];
		return body;
	};
	return { delays: getStationDelays() };
}

export async function _load() {
	const getStationDelays = async () => {
		const res = await fetch(`${apiUrl}/stations`);
		if (!res.ok) throw new Error(`failed to fetch station delays: ${res.body}`);
		const body = (await res.json()) as StationDelay[];
		return body;
	};
	return { delays: getStationDelays() };
}

export async function _load_prime() {
	const getStationDelays = async () => {
		const res = await fetch(`${apiUrl}/stations/prime`);
		if (!res.ok) throw new Error(`failed to fetch station delays: ${res.body}`);
		const body = (await res.json()) as StationDelay[];
		return body;
	};
	return { delays: getStationDelays() };
}
