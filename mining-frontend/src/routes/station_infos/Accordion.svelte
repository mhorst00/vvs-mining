<script lang="ts">
  import { stopInfoSource, type StopInfo } from "$lib/stores";
  import {
    Accordion,
    AccordionItem,
    InputChip,
    ListBox,
    ListBoxItem,
  } from "@skeletonlabs/skeleton";
  import stops from "../haltestellen.json";
  import { _load, _load_date, _load_timeframe } from "./+page";
  import FormDate, { date } from "./FormDate.svelte";
  import FormTimeframe, { lower, upper } from "./FormTimeframe.svelte";

  let chosenStation: String[] = [];
  let chosenTimeSetting: number = 0; // 0 = standard, 1 = date, 2 = timeframe

  async function applyFilter() {
    let newStopInfos: StopInfo[] = [];
    stopInfoSource.subscribe((value) => {
      newStopInfos = value;
    });

    if (chosenTimeSetting == 0) {
      const newValue = await _load();
      newStopInfos = await newValue.infos;
    }
    if (chosenTimeSetting == 1) {
      const newValue = await _load_date(date);
      newStopInfos = await newValue.infos;
    }
    if (chosenTimeSetting == 2) {
      const newValue = await _load_timeframe(lower, upper);

      newStopInfos = await newValue.infos;
    }

    if (chosenStation.length != 0) {
      newStopInfos = newStopInfos.filter((elem) =>
        chosenStation.includes(elem.station)
      );
    }
    stopInfoSource.set(newStopInfos);
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
          <InputChip
            list="stopsDatalist"
            bind:value={chosenStation}
            name="chips"
            whitelist={stops}
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
              value="0">Alle Infos anzeigen</ListBoxItem
            >
            <ListBoxItem
              class="md:max-w-lg"
              bind:group={chosenTimeSetting}
              name="lines/date"
              value="1">Alle Infos an einem Tag anzeigen</ListBoxItem
            >
            <ListBoxItem
              class="md:max-w-lg"
              bind:group={chosenTimeSetting}
              name="lines/timeframe"
              value="2">Alle Infos in einem Zeitraum anzeigen</ListBoxItem
            >
          </ListBox>
          {#if chosenTimeSetting == 1}
            <FormDate />
          {:else if chosenTimeSetting == 2}
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
