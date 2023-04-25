<script>
  import "@skeletonlabs/skeleton/themes/theme-skeleton.css";
  import "@skeletonlabs/skeleton/styles/all.css";
  import "../app.postcss";
  import { AppShell, AppBar, LightSwitch } from "@skeletonlabs/skeleton";
  import { Drawer, drawerStore } from "@skeletonlabs/skeleton";
  import Navbar from "./Navbar.svelte";
  function openDrawer() {
    drawerStore.open({});
  }
</script>

<Drawer><Navbar /></Drawer>
<!-- App Shell -->
<AppShell slotSidebarLeft="bg-surface-500/5 w-0 lg:w-64 p-4">
  <svelte:fragment slot="sidebarLeft">
    <!-- Insert the list: -->
    <Navbar />
    <!-- --- -->
  </svelte:fragment>

  <svelte:fragment slot="header">
    <!-- App Bar -->
    <AppBar>
      <svelte:fragment slot="lead">
        <div class="flex items-center">
          <button class="lg:hidden btn btn-sm mr-4" on:click={openDrawer}>
            <span>
              <svg viewBox="0 0 100 80" class="fill-token w-4 h-4">
                <rect width="100" height="20" />
                <rect y="30" width="100" height="20" />
                <rect y="60" width="100" height="20" />
              </svg>
            </span>
          </button>
          <strong class="lg:pl-4 text-xl uppercase"
            >VVS-Verspätungsdashboard</strong
          >
        </div>
      </svelte:fragment>
      <svelte:fragment slot="trail"
        ><div class="pr-4"><LightSwitch /></div></svelte:fragment
      >
    </AppBar>
  </svelte:fragment>
  <!-- Page Route Content -->
  <slot />
</AppShell>
