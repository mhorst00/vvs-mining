<script lang="ts">
  import { Table, Paginator } from "@skeletonlabs/skeleton";
  import type { PaginationSettings } from "@skeletonlabs/skeleton/components/Paginator/types";
  export let sourceHeaders: any;

  export let sourceBody: any;

  $: sourceBodySliced = sourceBody.slice(
    page.offset * page.limit,
    page.offset * page.limit + page.limit
  );

  function onPageChange(e: CustomEvent): void {
    console.log("event:page", e.detail);
  }

  function onAmountChange(e: CustomEvent): void {
    console.log("event:amount", e.detail);
  }


  let amounts = [5, 10, 25, sourceBody.length].sort((x, y) => {
    if (x > y) {
      return 1;
    }
    if (x < y) {
      return -1;
    }
    return 0;
  });
  console.log(amounts);
  let page = {
    offset: 0,
    limit: 10,
    size: sourceBody.length,
    amounts: amounts,
  } as PaginationSettings;
</script>

<section class="card variant-glass p-4 space-y-4">
  <Table
    source={{
      head: sourceHeaders,
      body: sourceBodySliced,
    }}
  />
  <Paginator
    bind:settings={page}
    on:page={onPageChange}
    on:amount={onAmountChange}
  />
</section>
