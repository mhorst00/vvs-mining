<script lang="ts">
  import TableWithPaginator from "../TableWithPaginator.svelte";
  import Accordion from "./Accordion.svelte";
  const source = [
    {
      name: "Schwabstraße",
      train: "S3",
      avg_delay: 78.487144,
    },
  ];
  let sourceHeaders = ["Haltestelle", "Linie", "Durchschnittliche Verspätung"];

  let sourceBody: string[][] = source.map(
    (x: { name: string; train: string; avg_delay: number }) => [
      x.name,
      x.train,
      x.avg_delay.toString(),
    ]
  );
</script>

<Accordion />

<div class="px-4 py-4">
  <hr class="pb-2" />
  <h2 class="pr-4 py-4">Hier könnten Ihre Stationen stehen</h2>
  <TableWithPaginator {sourceHeaders} {sourceBody} />
</div>
