<script lang="ts">
  import {
    Accordion,
    AccordionItem,
    InputChip,
    tooltip,
  } from "@skeletonlabs/skeleton";
  import stops from "../haltestellen.json";
  
  let chosenStation: String[] = [];
  let chosenTrain: String[] = [];
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
      <!-- choose Date: -->
      <AccordionItem>
        <svelte:fragment slot="lead"><h5>Zeitfenster</h5></svelte:fragment>
        <svelte:fragment slot="summary"
          >Ein Datum oder ein Zeitfenster eingeben</svelte:fragment
        >
        <svelte:fragment slot="content">
          <div class="input-group input-group-divider grid-cols-2 md:max-w-lg">
            <input class="input" type="date" />
            <button class="variant-filled-secondary"
              >Informationen anzeigen</button
            >
          </div>
        </svelte:fragment>
      </AccordionItem>
      <button class="btn variant-filled-primary ml-2">Filter anwenden</button>
    </svelte:fragment>
  </AccordionItem>
</Accordion>
