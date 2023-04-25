import { writable } from "svelte/store";
export interface IncidentItem {
	station: string;
	line: string;
	incident: string;
}
export const incidentSource = writable<IncidentItem[]>([]);

export interface LineDelay {
	avg_delay: number;
	line: string;
}
export const lineDelaySource = writable<LineDelay[]>([]);

export interface StopInfo {
	station: string;
	short: string;
	long: string;
}
export const stopInfoSource = writable<StopInfo[]>([]);

export interface StationDelay {
	name: string;
	avg_delay: number;
	line: string;
}
export const stationDelaySource = writable<StationDelay[]>([]);
