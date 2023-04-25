import { apiUrl } from "$lib/stores";

interface IncidentItemFull {
    station: string;
    line: string;
    train_number: string;
    incident: string;
    date: string;
}

export async function _load(date: string, line: string) {
    const getIncidents = async () => {
        const url = `i${apiUrl}/incidents?date=${date}&line=${line}`;
        const res = await fetch(encodeURI(url));
        if (!res.ok) throw new Error(`failed to fetch line delays: ${res.body}`);
        const body = (await res.json()) as IncidentItemFull[];
        return body.map((incidentFull) => ({
            station: incidentFull.station,
            line: incidentFull.line,
            incident: incidentFull.incident,
        }));
    };
    return { incidents: getIncidents() };
}
