<script lang="ts">
  import Accordion from "./Accordion.svelte";
  import TableWithPaginator from "../TableWithPaginator.svelte";

  interface SourceItem {
    name: string;
    transportation_name: string;
    content: string;
  }

  let source: SourceItem[] = [];

  export function applyFilter() {
    source = [
      {
        name: "Backnang",
        transportation_name: "R-Bahn MEX19",
        content: "Warten auf einen entgegenkommenden Zug",
      },
      {
        name: "Backnang",
        transportation_name: "R-Bahn MEX90",
        content: "Verspätung eines vorausfahrenden Zuges",
      },
    ];
  }

  let sourceBody: string[][] = source.map((x: SourceItem) => [
    x.name,
    x.transportation_name,
    x.content,
  ]);
  let sourceHeaders: string[] = ["Haltestelle", "Zugname", "Meldung"];
</script>

<Accordion />

<div class="px-4 py-4">
  <hr class="pb-2" />
  <h2 class="pr-4 py-4">Hier könnten Ihre Verspätungs Infos stehen</h2>

  <TableWithPaginator {sourceHeaders} {sourceBody} />
</div>
