<script lang="ts">
  import Accordion from "./Accordion.svelte";
  import TableWithPaginator from "../TableWithPaginator.svelte";

  import { incidentSource } from "$lib/stores";
  import type { IncidentItem } from "$lib/stores";

  let subscribedSource: IncidentItem[];

  incidentSource.subscribe((value) => {
    subscribedSource = value;
  });
  let sourceBody: string[][];
  let sourceHeaders: string[] = ["Haltestelle", "Zugname", "Meldung"];
  $: sourceBody = subscribedSource.map((x: IncidentItem) => [
    x.station,
    x.line,
    x.incident,
  ]);
</script>

<Accordion />

<div class="px-4 py-4">
  <hr class="pb-2" />
  <h2 class="pr-4 py-4">Verspätungs Infos:</h2>

  <TableWithPaginator {sourceHeaders} {sourceBody} />
</div>
