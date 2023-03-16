import { writable } from "svelte/store";
export interface SourceItem {
    name: string;
    transportation_name: string;
    content: string;
  }
export  const sourceItemSource = writable<SourceItem[]>([]);


export interface  LineDelay{
    avg_delay: number;
    line: string;
};
export  const lineDelaySource = writable<LineDelay[]>([]);
