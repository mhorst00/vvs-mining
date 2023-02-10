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
  let chosen: String[] = [];
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

<Accordion class="py-4">
  <AccordionItem closed>
    <svelte:fragment slot="summary"><h3>Filter</h3></svelte:fragment>
    <svelte:fragment slot="content"
      ><AccordionItem>
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
              style="background-color: red;"
              bind:value={chosen}
              name="chips"
              whitelist={stops}
              allowUpperCase={true}
            />
          </div>
        </svelte:fragment>
      </AccordionItem></svelte:fragment
    >
  </AccordionItem>
</Accordion>

<div class="px-4 py-4">
  <hr class="pb-2" />
  <h2 class="px-4 py-4">Hier könnten Ihre Haltestellen Infos stehen</h2>
  <Table source={tableSimple} />

  <!--   <div class="input-chip textarea cursor-pointer p-2 rounded-container-token">
    <div class="h-0 overflow-hidden"><select name="chips" multiple="" /></div>
    <div class="input-chip-interface space-y-4">
      <form>
        <input
          list="stopsDatalist"
          type="text"
          placeholder="Enter values..."
          class="input-chip-field unstyled bg-transparent border-0 !ring-0 p-0 w-full"
        />
      </form>
    </div>
  </div> -->

  <!--   <datalist id="stopsDatalist">
    {#each stops as stop}
      <option value={stop} />
    {/each}
  </datalist> -->
</div>
