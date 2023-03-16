<script lang="ts">
  import TableWithPaginator from "../TableWithPaginator.svelte";
  import Accordion from "./Accordion.svelte";
  import { lineDelaySource } from "../../lib/stores";
  import type { LineDelay } from "../../lib/stores";
  /** @type {import('./$types').PageData} */
  export let data: any;

  lineDelaySource.update((value) => (value = data.delays));

  let subscribedSource: LineDelay[] = [];

  lineDelaySource.subscribe((value) => {
    subscribedSource = value;
  });
  let sourceBody: string[][];
  $: sourceBody = subscribedSource.map((x: LineDelay) => [
    x.line,
    x.avg_delay.toString(),
  ]);

  let sourceHeaders: string[] = ["Linie", "Durchschnittliche Verspätung"];
</script>

<Accordion />

<div class="px-4 py-4">
  <hr class="pb-2" />
  <h2 class="pr-4 py-4">Hier könnten Ihre Linien stehen</h2>
  <TableWithPaginator {sourceHeaders} {sourceBody} />
</div>
