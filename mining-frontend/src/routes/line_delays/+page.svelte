<script lang="ts">
  import TableWithPaginator from "../TableWithPaginator.svelte";
  import Accordion from "./Accordion.svelte";
  const source = [
    {
      line: "IC",
      avg_delay: 154.2671,
    },
  ];

  let sourceBody: string[][] = source.map(
    (x: { line: string; avg_delay: number }) => [x.line, x.avg_delay.toString()]
  );

  let sourceHeaders: string[] = ["Linie", "Durchschnittliche Verspätung"];
</script>

<Accordion />

<div class="px-4 py-4">
  <hr class="pb-2" />
  <h2 class="pr-4 py-4">Hier könnten Ihre Linien stehen</h2>
  <TableWithPaginator {sourceHeaders} {sourceBody} />
</div>
