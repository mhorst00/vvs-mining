<script lang="ts">
  import Accordion from "./Accordion.svelte";
  import TableWithPaginator from "../TableWithPaginator.svelte";
  import { stopInfoSource, type StopInfo } from "$lib/stores";

  export let data: any;

  stopInfoSource.update((value) => (value = data.infos));

  let subscribedSource: StopInfo[] = [];

  stopInfoSource.subscribe((value) => {
    subscribedSource = value;
  });

  let sourceBody: string[][];
  $: sourceBody = subscribedSource.map((x: StopInfo) => [
    x.station,
    x.short,
    x.long,
  ]);
  let sourceHeaders: string[] = [
    "Haltestelle",
    "Kurzmeldung",
    "Vollständige Meldung",
  ];
</script>

<Accordion />

<div class="px-4 py-4">
  <hr class="pb-2" />
  <h2 class="px-4 py-4">Haltestellen Infos:</h2>
  <TableWithPaginator {sourceHeaders} {sourceBody} />
</div>
