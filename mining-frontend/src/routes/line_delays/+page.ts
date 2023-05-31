import { type LineDelay, apiUrl } from "$lib/stores";

export async function load() {
	const getLineDelays = async () => {
		const res = await fetch(`${apiUrl}/lines`);
		if (!res.ok) throw new Error(`failed to fetch line delays: ${res.body}`);
		const body = (await res.json()) as LineDelay[];
		return body;
	};
	return { delays: getLineDelays() };
}

export async function _load_date(date: String) {
	const getLineDelays = async () => {
		const url = `${apiUrl}/lines/date?date=${date}`;
		const res = await fetch(url);
		if (!res.ok) throw new Error(`failed to fetch line delays: ${res.body}`);
		const body = (await res.json()) as LineDelay[];
		return body;
	};
	return { delays: getLineDelays() };
}

export async function _load_timeframe(lower: String, upper: String) {
	const getLineDelays = async () => {
		const url = `${apiUrl}/lines/timeframe?lower_limit=${lower}&upper_limit=${upper}`;
		const res = await fetch(encodeURI(url));
		if (!res.ok) throw new Error(`failed to fetch line delays: ${res.body}`);
		const body = (await res.json()) as LineDelay[];
		return body;
	};
	return { delays: getLineDelays() };
}

export async function _load() {
	const getLineDelays = async () => {
		const res = await fetch(`${apiUrl}/lines`);
		if (!res.ok) throw new Error(`failed to fetch line delays: ${res.body}`);
		const body = (await res.json()) as LineDelay[];
		return body;
	};
	return { delays: getLineDelays() };
}

export async function _load_prime() {
	const getLineDelays = async () => {
		const res = await fetch(`${apiUrl}/lines/prime`);
		if (!res.ok) throw new Error(`failed to fetch line delays: ${res.body}`);
		const body = (await res.json()) as LineDelay[];
		return body;
	};
	return { delays: getLineDelays() };
}
