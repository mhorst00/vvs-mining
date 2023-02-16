<script lang="ts">
  import {
    Table,
    tableMapperValues,
    type TableSource,
  } from "@skeletonlabs/skeleton";
  import Accordion from "./Accordion.svelte";

  /*   interface CustomFilter {
    name: String[];
    transportation_name: String[];
  } */

  /*   interface SourceItem {
    name: String;
    transportation_name: String;
    content: String;
  } */

  const sourceBody = [
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

  const tableSimple: TableSource = {
    // A list of heading labels.
    head: ["Haltestelle", "Zugname", "Meldung"],
    // The data visibly shown in your table body UI.
    body: tableMapperValues(sourceBody, [
      "name",
      "transportation_name",
      "content",
    ]),
    // Optional: The data returned when interactive is enabled and a row is clicked.
    meta: tableMapperValues(sourceBody, ["Haltestelle", "Zugname", "Meldung"]),
  };
</script>

<Accordion />

<div class="px-4 py-4">
  <hr class="pb-2" />
  <h2 class="px-4 py-4">Hier könnten Ihre Verspätungs Infos stehen</h2>
  <Table source={tableSimple} />
</div>
