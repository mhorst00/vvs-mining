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
  let types: string[] = ["stopInfo", "lineInfo"];
  let chosenStation: String[] = [];
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
      <!-- Choose type -->
      <AccordionItem>
        <svelte:fragment slot="lead"><h5>Typ</h5></svelte:fragment>
        <svelte:fragment slot="summary"
          >Ein oder mehrere Haltestellen auswählen</svelte:fragment
        >
        <svelte:fragment slot="content">
          <div>
            <ListBox multiple>
              <div class="grid grid-cols-2 gap-4 md:max-w-sm">
                <div>
                  <ListBoxItem
                    class="bg-primary-500"
                    bind:group={types}
                    name="stopInfo"
                    value="stopInfo">stopInfo</ListBoxItem
                  >
                </div>
                <div>
                  <ListBoxItem
                    bind:group={types}
                    name="lineInfo"
                    value="lineInfo">lineInfo</ListBoxItem
                  >
                </div>
              </div>
            </ListBox>
          </div>
        </svelte:fragment>
      </AccordionItem>
    </svelte:fragment>
  </AccordionItem>
</Accordion>
