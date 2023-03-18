<script lang="ts" context="module">
    let dates_first: String = "2022-12-07";
    let dates_second: String = "2022-12-07";
    let times_first: String = "10:00";
    let times_second: String = "17:00";
  
    const lower = `${dates_first} ${times_first}`;
    const upper = `${dates_second} ${times_second}`;
  
    export { lower, upper };
  </script>
  
  <div class=" grid grid-cols-2 md:max-w-lg gap-3">
    <input class="input" type="date" bind:value={dates_first} />
    <input class="input" type="time" bind:value={times_first} />
  
    <input class="input" type="date" bind:value={dates_second} />
    <input class="input" type="time" bind:value={times_second} />
  </div>
  