<script lang="ts">
  import TableWithPaginator from "../TableWithPaginator.svelte";
  import Accordion from "./Accordion.svelte";
  import { Bar } from "svelte-chartjs";
  import {
    Chart,
    Title,
    Tooltip,
    Legend,
    BarElement,
    CategoryScale,
    LinearScale,
  } from "chart.js";
  import { RadioGroup, RadioItem } from "@skeletonlabs/skeleton";

  Chart.register(
    Title,
    Tooltip,
    Legend,
    BarElement,
    CategoryScale,
    LinearScale
  );

  export let data;
  let displayTable = false;

  let sourceHeaders = ["Haltestelle", "Linie", "Durchschnittliche Verspätung"];
  let sourceBody: string[][] = data.delays.map(
    (x: { name: string; line: string; avg_delay: number }) => [
      x.name,
      x.line,
      x.avg_delay.toString(),
    ]
  );

  let chart_data = {
    datasets: [
      {
        data: data.delays.map(
          (x: { name: string; line: string; avg_delay: number }) => x.avg_delay
        ),
        label: "Verspätung in Sekunden",
        backgroundColor: [
          "rgba(255, 134,159,0.4)",
          "rgba(98,  182, 239,0.4)",
          "rgba(255, 218, 128,0.4)",
          "rgba(113, 205, 205,0.4)",
          "rgba(170, 128, 252,0.4)",
          "rgba(255, 177, 101,0.4)",
        ],
        borderWidth: 2,
        borderColor: [
          "rgba(255, 134, 159, 1)",
          "rgba(98,  182, 239, 1)",
          "rgba(255, 218, 128, 1)",
          "rgba(113, 205, 205, 1)",
          "rgba(170, 128, 252, 1)",
          "rgba(255, 177, 101, 1)",
        ],
      },
    ],
    labels: data.delays.map(
      (x: { name: string; line: string; avg_delay: number }) =>
        `${x.name} ${x.line}`
    ),
  };
</script>

<Accordion />
<RadioGroup
  active="variant-filled-primary"
  hover="hover:variant-soft-primary"
  class="m-2"
>
  <RadioItem bind:group={displayTable} name="diagramm" value={false}
    >Diagramm</RadioItem
  >
  <RadioItem bind:group={displayTable} name="tabelle" value={true}
    >Tabelle</RadioItem
  >
</RadioGroup>
{#if displayTable}
  <TableWithPaginator {sourceHeaders} {sourceBody} />
{:else}
  <Bar data={chart_data} options={{ responsive: true }} />
{/if}
