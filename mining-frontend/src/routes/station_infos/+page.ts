/** @type {import('./$types').PageLoad} */

interface StopInfoFull {
    name: string;
    short: string;
    long: string;
    date: string;
  }
function trim(body:StopInfoFull[]) {
    return body.map(stopInfoFull =>({
        station: stopInfoFull.name,
        short: stopInfoFull.short,
        long: stopInfoFull.long
    }));
}

export async function load({  }) {
    const getStationInfos = async () => {
        const res = await fetch("http://localhost:3000/infos");
        if (!res.ok) throw new Error(`failed to fetch line delays: ${res.body}`);
        const body = (await res.json()) as StopInfoFull[];
        return trim(body);
    };
    return { infos: getStationInfos() };
}

export async function _load_date(date:String) {
    const getStationInfosDate = async () => {
        const url = `http://localhost:3000/infos/date?date=${date}`
        const res = await fetch(url);
        if (!res.ok) throw new Error(`failed to fetch line delays: ${res.body}`);
        const body = (await res.json()) as StopInfoFull[];
        return trim(body)
    };
    return { infos: getStationInfosDate() };
}

export async function _load_timeframe(lower:String, upper:String) {
    const getStationInfosTimeframe = async () => {
        const url = `http://localhost:3000/infos/timeframe?lower_limit=${lower}&upper_limit=${upper}`
        const res = await fetch(encodeURI(url));
        if (!res.ok) throw new Error(`failed to fetch line delays: ${res.body}`);
        const body = (await res.json()) as StopInfoFull[];
        return trim(body)
    };
    return { infos: getStationInfosTimeframe() };
}

export async function _load() {
    const getStationInfos = async () => {
        const res = await fetch("http://localhost:3000/infos");
        if (!res.ok) throw new Error(`failed to fetch line delays: ${res.body}`);
        const body = (await res.json()) as StopInfoFull[];
        return trim(body)
    };
    return { infos: getStationInfos() };
}