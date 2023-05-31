<script lang="ts">
  import { Bar, Pie } from "svelte-chartjs";
  import type { ChartData } from "chart.js";
  import {
    Chart,
    Title,
    Tooltip,
    Legend,
    ArcElement,
    CategoryScale,
    LinearScale,
    BarElement,
  } from "chart.js";

  export let data: any;
  Chart.register(
    Title,
    Tooltip,
    Legend,
    ArcElement,
    BarElement,
    CategoryScale,
    LinearScale
  );
  const sourceChartAll: ChartData<"pie", number[]> = {
    labels: ["Pünktlich", "Verspätet"],
    datasets: [
      {
        data: [92, 8],
        backgroundColor: ["#F7464A", "#46BFBD"],
        hoverBackgroundColor: ["#FF5A5E", "#5AD3D1"],
      },
    ],
  };
  const sourceChartPrime: ChartData<"pie", number[]> = {
    labels: ["Pünktlich", "Verspätet"],
    datasets: [
      {
        data: [67, 33],
        backgroundColor: ["#F7464A", "#46BFBD"],
        hoverBackgroundColor: ["#FF5A5E", "#5AD3D1"],
      },
    ],
  };

  const optionsAll = {
    plugins: {
      title: {
        display: true,
        text: "Verspätung ab 3 Minuten im gesamten Datensatz",
      },
    },
    responsive: true,
  };

  const optionsPrime = {
    plugins: {
      title: {
        display: true,
        text: "Verspätung ab 3 Minuten zu Hautpverkehrszeiten",
      },
    },
    responsive: true,
  };

  const optionsLines = {
    plugins: {
      title: {
        display: true,
        text: "Verspätung der S-Bahn-Linien",
      },
    },
    responsive: true,
  };

  const filteredLines = data.delays.filter(
    (x: { line: string; avg_delay: number }) => x.line.includes("S")
  );
  const sourceChartLines = {
    datasets: [
      {
        data: filteredLines.map(
          (x: { line: string; avg_delay: number }) => x.avg_delay
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
    labels: filteredLines.map(
      (x: { line: string; avg_delay: number }) => x.line
    ),
  };
</script>

<div class="container h-full mx-auto center items-center">
  <div class="grid grid-cols-2 m-10 gap-8">
    <div class="col-span-2">
      <div class="text-center">
        <h1 class="font-bold">Hallo beim VVS-Verspätungsdashboard!</h1>
      </div>
    </div>
    <div>
      <Pie data={sourceChartAll} options={optionsAll} />
    </div>
    <div>
      <Pie data={sourceChartPrime} options={optionsPrime} />
    </div>
    <div class="col-span-2">
      <Bar data={sourceChartLines} options={optionsLines} />
    </div>
  </div>
</div>
