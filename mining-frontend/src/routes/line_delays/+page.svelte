<script lang="ts">
  import {
    Table,
    tableMapperValues,
    type TableSource,
  } from "@skeletonlabs/skeleton";
  import Accordion from "./Accordion.svelte";
  const sourceBody = [
    {
      line: "IC",
      avg_delay: 154.2671,
    },
  ];

  const tableSimple: TableSource = {
    // A list of heading labels.
    head: ["Linie", "Durchschnittliche Verspätung"],
    // The data visibly shown in your table body UI.
    body: tableMapperValues(sourceBody, ["line", "avg_delay"]),
    // Optional: The data returned when interactive is enabled and a row is clicked.
    meta: tableMapperValues(sourceBody, [
      "Linie",
      "Durchschnittliche Verspätung",
    ]),
  };
</script>

<Accordion />

<div class="px-4 py-4">
  <hr class="pb-2" />
  <h2 class="pr-4 py-4">Hier könnten Ihre Linien stehen</h2>
  <Table source={tableSimple} />
</div>
