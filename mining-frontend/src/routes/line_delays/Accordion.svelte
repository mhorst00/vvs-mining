<script lang="ts">
  import { lineDelaySource, type LineDelay } from "../../lib/stores";
  import {
    Accordion,
    AccordionItem,
    InputChip,
    ListBox,
    ListBoxItem,
    tooltip,
  } from "@skeletonlabs/skeleton";
  import { _load, _load_date, _load_timeframe } from "./+page";
  import FormDate from "./FormDate.svelte";
  import FormTimeframe from "./FormTimeframe.svelte";
  let chosenTrain: String[] = [];
  let chosenTimeSetting: string = "lines";
  async function applyFilter() {
    let newDelays: LineDelay[] = [];
    lineDelaySource.subscribe((value) => {
      newDelays = value;
    });
    if (chosenTimeSetting === "lines") {
      const newValue = await _load();
      newDelays = await newValue.delays;
    }
    if (chosenTimeSetting === "lines/date") {
      const newValue = await _load_date(
        document.getElementById("line_delay_date").value
      );
      newDelays = await newValue.delays;
    }
    if (chosenTimeSetting === "lines/timeframe") {
      const lower =
        document.getElementById("line_delay_dates_first").value +
        " " +
        document.getElementById("line_delay_time_first").value;
      const upper =
        document.getElementById("line_delay_dates_second").value +
        " " +
        document.getElementById("line_delay_time_second").value;
      const newValue = await _load_timeframe(lower, upper);

      newDelays = await newValue.delays;
    }

    if (chosenTrain.length != 0) {
      newDelays = newDelays.filter((elem) => chosenTrain.includes(elem.line));
    }
    lineDelaySource.set(newDelays);
  }
</script>

<Accordion class="py-4">
  <AccordionItem closed>
    <svelte:fragment slot="summary"><h3>Filter</h3></svelte:fragment>
    <svelte:fragment slot="content">
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
