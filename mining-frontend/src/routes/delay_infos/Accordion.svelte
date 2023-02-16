<script lang="ts">
  import {
    Accordion,
    AccordionItem,
    InputChip,
    ListBox,
    ListBoxItem,
    tooltip,
  } from "@skeletonlabs/skeleton";
  import stops from "../haltestellen.json";
  import FormDate from "./FormDate.svelte";
  import FormTimeframe from "./FormTimeframe.svelte";
  let chosenStation: String[] = [];
  let chosenTrain: String[] = [];
  let chosenTimeSetting: string = "lines";
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
      <!-- choose time or timeframe: -->
      <AccordionItem>
        <svelte:fragment slot="lead"><h5>Zeitfenster</h5></svelte:fragment>
        <svelte:fragment slot="summary"
          >Ein Datum oder ein Zeitfenster eingeben</svelte:fragment
        >
        <svelte:fragment slot="content">
          <ListBox>
            <ListBoxItem
              bind:group={chosenTimeSetting}
              name="lines"
              value="lines">Alle Verspätungen anzeigen</ListBoxItem
            >
            <ListBoxItem
              bind:group={chosenTimeSetting}
              name="lines/date"
              value="lines/date"
              >Alle Verspätungen an einem Tag anzeigen</ListBoxItem
            >
            <ListBoxItem
              bind:group={chosenTimeSetting}
              name="lines/timeframe"
              value="lines/timeframe"
              >Alle Verspätungen in einem Zeitraum anzeigen</ListBoxItem
            >
          </ListBox>
          {#if chosenTimeSetting == "lines/date"}
            <FormDate />
          {:else if chosenTimeSetting == "lines/timeframe"}
            <FormTimeframe />
          {:else}{/if}
        </svelte:fragment>
      </AccordionItem>
    </svelte:fragment>
  </AccordionItem>
</Accordion>
