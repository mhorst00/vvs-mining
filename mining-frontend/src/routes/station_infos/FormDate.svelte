<script lang="ts" context="module">
  export let date: String = "2022-12-07";
</script>

<div class="input-group input-group-divider md:max-w-lg">
  <input class="input" type="date" bind:value={date} />
</div>
