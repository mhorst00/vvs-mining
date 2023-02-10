<script lang="ts">
  import {
    Accordion,
    AccordionItem,
    InputChip,
    Table,
    tableMapperValues,
    tooltip,
    type TableSource,
  } from "@skeletonlabs/skeleton";
  import stops from "../haltestellen.json";
  let chosenStation: String[] = [];
  let chosenTrain: String[] = [];
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

<Accordion class="py-4">
  <AccordionItem closed>
    <svelte:fragment slot="summary"><h3>Filter</h3></svelte:fragment>
    <svelte:fragment slot="content">
      <!-- Choose Stop -->
      <AccordionItem>
        <svelte:fragment slot="lead"><h5>Haltestelle</h5></svelte:fragment>
        <svelte:fragment slot="summary"
          >Ein oder mehrere Haltestellen auswählen</svelte:fragment
        >
        <svelte:fragment slot="content">
          <div
            use:tooltip={{
              content:
                "Nur gültige Haltestellen mit korrekter Groß-/Kleinschreibung",
              position: "bottom",
            }}
          >
            <InputChip
              list="stopsDatalist"
              bind:value={chosenStation}
              name="chips"
              whitelist={stops}
              allowUpperCase={true}
            />
          </div>
        </svelte:fragment>
      </AccordionItem>
      <!-- Choose Train name -->
      <AccordionItem>
        <svelte:fragment slot="lead"><h5>Zugname</h5></svelte:fragment>
        <svelte:fragment slot="summary"
          >Ein oder mehrere Züge auswählen</svelte:fragment
        >
        <svelte:fragment slot="content">
          <div
            use:tooltip={{
              content: "Auf korrekte Groß-/Kleinschreibung achten",
              position: "bottom",
            }}
          >
            <InputChip
              bind:value={chosenTrain}
              name="chips"
              allowUpperCase={true}
            />
          </div>
        </svelte:fragment>
      </AccordionItem>
    </svelte:fragment>
  </AccordionItem>
</Accordion>

<div class="px-4 py-4">
  <hr class="pb-2" />
  <h2 class="px-4 py-4">Hier könnten Ihre Verspätungs Infos stehen</h2>
  <Table source={tableSimple} />
</div>
