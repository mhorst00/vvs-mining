<script lang="ts">
  import { Table, Paginator } from "@skeletonlabs/skeleton";
  export let sourceHeaders: any;

  export let sourceBody: any;

  let page = {
    offset: 0,
    limit: 10,
    size: sourceBody.length,
    amounts: [5, 10, 20, 25],
  };

  $: page = { ...page, size: sourceBody.length };

  $: sourceBodySliced = sourceBody.slice(
    page.offset * page.limit,
    page.offset * page.limit + page.limit
  );
</script>

<section class="card variant-glass p-4 space-y-4">
  <Table
    source={{
      head: sourceHeaders,
      body: sourceBodySliced,
    }}
  />
  <Paginator bind:settings={page} />
</section>
