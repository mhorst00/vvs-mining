<script lang="ts">
  import {
    Table,
    tableMapperValues,
    type TableSource,
  } from "@skeletonlabs/skeleton";
  import Accordion from "./Accordion.svelte";
  const sourceBody = [
    {
      name: "Altbach",
      type: "stopInfo",
      urltext: "Aufzug Außer Betrieb",
      content:
        "Am Bahnhof Altbach ist der Aufzug zu Gleis 3/4 bis auf Weiteres außer Betrieb.",
    },
    {
      name: "Universität",
      type: "stopInfo",
      urltext: "Aufzug Außer Betrieb",
      content:
        "Am Bahnhof Universität ist der Aufzug zu Gleis 2 (S-Bahn) bis auf Weiteres außer Betrieb.",
    },
  ];

  const tableSimple: TableSource = {
    // A list of heading labels.
    head: ["Haltestelle", "Typ", "Kurzmeldung", "Vollständige Meldung"],
    // The data visibly shown in your table body UI.
    body: tableMapperValues(sourceBody, ["name", "type", "urltext", "content"]),
    // Optional: The data returned when interactive is enabled and a row is clicked.
    meta: tableMapperValues(sourceBody, [
      "Haltestelle",
      "Typ",
      "Kurzmeldung",
      "Vollständige Meldung",
    ]),
  };
</script>

<Accordion />

<div class="px-4 py-4">
  <hr class="pb-2" />
  <h2 class="px-4 py-4">Hier könnten Ihre Haltestellen Infos stehen</h2>
  <Table source={tableSimple} interactive={true} />
</div>
