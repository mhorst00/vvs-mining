<script lang="ts">
  import {
    Accordion,
    AccordionItem,
    InputChip,
    ListBox,
    ListBoxItem,
  } from "@skeletonlabs/skeleton";
  import stops from "../haltestellen.json";
  import FormDate, { date } from "./FormDate.svelte";
  import FormTimeframe, { lower, upper } from "./FormTimeframe.svelte";
  import { _load, _load_date, _load_timeframe, _load_prime } from "./+page";
  import { stationDelaySource, type StationDelay } from "$lib/stores";
  let chosenStation: String[] = [];
  let chosenTrain: String[] = [];
  let chosenTimeSetting: string = "lines";
  async function applyFilter() {
    let newDelays: StationDelay[] = [];
    stationDelaySource.subscribe((value) => {
      newDelays = value;
    });
    if (chosenTimeSetting === "lines") {
      const newValue = await _load();
      newDelays = await newValue.delays;
    }
    if (chosenTimeSetting === "lines/date") {
      const newValue = await _load_date(date);
      newDelays = await newValue.delays;
    }
    if (chosenTimeSetting === "lines/timeframe") {
      const newValue = await _load_timeframe(lower, upper);

      newDelays = await newValue.delays;
    }
    if (chosenTimeSetting === "lines/prime") {
      const newValue = await _load_prime();
      newDelays = await newValue.delays;
    }
    if (chosenStation.length != 0) {
      newDelays = newDelays.filter((elem) => chosenStation.includes(elem.name));
    }
    if (chosenTrain.length != 0) {
      newDelays = newDelays.filter((elem) => chosenTrain.includes(elem.line));
    }
    stationDelaySource.set(newDelays);
  }
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
          <InputChip
            list="stopsDatalist"
            bind:value={chosenStation}
            name="chips"
            whitelist={stops}
            allowUpperCase={true}
            autocomplete="whitelist"
          />
        </svelte:fragment>
      </AccordionItem>
      <!-- Choose Train name -->
      <AccordionItem>
        <svelte:fragment slot="lead"><h5>Zugname</h5></svelte:fragment>
        <svelte:fragment slot="summary"
          >Ein oder mehrere Züge auswählen</svelte:fragment
        >
        <svelte:fragment slot="content">
          <InputChip
            bind:value={chosenTrain}
            name="chips"
            allowUpperCase={true}
          />
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
              class="md:max-w-lg"
              bind:group={chosenTimeSetting}
              name="lines"
              value="lines">Alle Verspätungen anzeigen</ListBoxItem
            >
            <ListBoxItem
              class="md:max-w-lg"
              bind:group={chosenTimeSetting}
              name="lines/date"
              value="lines/date"
              >Alle Verspätungen an einem Tag anzeigen</ListBoxItem
            >
            <ListBoxItem
              class="md:max-w-lg"
              bind:group={chosenTimeSetting}
              name="lines/timeframe"
              value="lines/timeframe"
              >Alle Verspätungen in einem Zeitraum anzeigen</ListBoxItem
            >
            <ListBoxItem
              class="md:max-w-xl"
              bind:group={chosenTimeSetting}
              name="lines/prime"
              value="lines/prime"
              >Verspätungen zu Hauptzeiten (Mo-Fr: 06:00-09:00, 16:00-19:00)
              anzeigen</ListBoxItem
            >
          </ListBox>
          {#if chosenTimeSetting == "lines/date"}
            <FormDate />
          {:else if chosenTimeSetting == "lines/timeframe"}
            <FormTimeframe />
          {/if}
        </svelte:fragment>
      </AccordionItem>
      <button class="btn variant-filled-primary ml-2" on:click={applyFilter}
        >Filter anwenden</button
      >
    </svelte:fragment>
  </AccordionItem>
</Accordion>
