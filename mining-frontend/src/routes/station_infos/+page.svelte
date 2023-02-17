<script lang="ts">
  import Accordion from "./Accordion.svelte";
  import TableWithPaginator from "../TableWithPaginator.svelte";
  const source = [
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
  let sourceBody: string[][] = source.map(
    (x: { name: string; type: string; urltext: string; content: string }) => [
      x.name,
      x.type,
      x.urltext,
      x.content,
    ]
  );
  let sourceHeaders: string[] = [
    "Haltestelle",
    "Typ",
    "Kurzmeldung",
    "Vollständige Meldung",
  ];
</script>

<Accordion />

<div class="px-4 py-4">
  <hr class="pb-2" />
  <h2 class="px-4 py-4">Hier könnten Ihre Haltestellen Infos stehen</h2>
  <TableWithPaginator {sourceHeaders} {sourceBody} />
</div>
