<script lang="ts">
  import {
    Accordion,
    AccordionItem,
    InputChip,
    tooltip,
  } from "@skeletonlabs/skeleton";
  import stops from "../haltestellen.json";
  import { _load } from "./+page";
  import { incidentSource, type IncidentItem } from "$lib/stores";

  let chosenStation: string[] = [];
  let chosenTrain: string[] = [];
  let timeInput: string = "";

  async function applyFilter() {
    if (timeInput === "" || chosenTrain.length != 1) {
      //TODO change to better method
      window.alert("Bitte notwendige Filter setzen");
      return;
    }
    let newDelayInfos: IncidentItem[] = [];
    incidentSource.subscribe((value) => {
      newDelayInfos = value;
    });
    const newValue = await _load(timeInput, chosenTrain[0]);
    newDelayInfos = await newValue.incidents;
    if (chosenStation.length != 0) {
      newDelayInfos = newDelayInfos.filter((elem) =>
        chosenStation.includes(elem.station)
      );
    }
    incidentSource.set(newDelayInfos);
  }
</script>

<Accordion class="py-4">
  <AccordionItem open>
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
        <svelte:fragment slot="lead"><h5>Linie</h5></svelte:fragment>
        <svelte:fragment slot="summary"
          >Eine Linie auswählen (Erforderlich)</svelte:fragment
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
              minlength={1}
              max={1}
            />
          </div>
        </svelte:fragment>
      </AccordionItem>
      <!-- choose Date: -->
      <AccordionItem>
        <svelte:fragment slot="lead"><h5>Zeitfenster</h5></svelte:fragment>
        <svelte:fragment slot="summary"
          >Ein Datum eingeben (Erforderlich)</svelte:fragment
        >
        <svelte:fragment slot="content">
          <div class="input-group input-group-divider md:max-w-lg">
            <input class="input" type="date" bind:value={timeInput} required />
          </div>
        </svelte:fragment>
      </AccordionItem>
      <button class="btn variant-filled-primary ml-2" on:click={applyFilter}
        >Filter anwenden</button
      >
    </svelte:fragment>
  </AccordionItem>
</Accordion>
