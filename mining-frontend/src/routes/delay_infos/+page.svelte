<script lang="ts">
  import Accordion from "./Accordion.svelte";
  import TableWithPaginator from "../TableWithPaginator.svelte";

  import { sourceItemSource } from "../../lib/stores";
  import type { SourceItem } from "../../lib/stores";

  let subscribedSource: SourceItem[];

  sourceItemSource.subscribe((value) => {
    subscribedSource = value;
  });
  let sourceBody: string[][];
  let sourceHeaders: string[] = ["Haltestelle", "Zugname", "Meldung"];
  $: sourceBody = subscribedSource.map((x: SourceItem) => [
    x.name,
    x.transportation_name,
    x.content,
  ]);
</script>

<Accordion />

<div class="px-4 py-4">
  <hr class="pb-2" />
  <h2 class="pr-4 py-4">Hier könnten Ihre Verspätungs Infos stehen</h2>

  <TableWithPaginator {sourceHeaders} {sourceBody} />
</div>
