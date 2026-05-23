<script lang="ts">
    import { vibrateOnClick } from "@d1vij/shit-i-always-use/svelte";
    import { ChevronLeft } from "@lucide/svelte";

    const { children } = $props();
</script>

<!--
    NOTE: Navigating back from /students/[rollnumber] resolves to /school/[name] 
    instead to /school/[name]/stream/[id] due to how the route is structured, and 
    it is NOT broken.
-->
<a
    class="ml-8 mt-4 block text-base bg-heading border-muted w-fit p-2 px-2 group"
    href={".."}
    {@attach vibrateOnClick(100)}
>
    <ChevronLeft
        class="size-4 stroke-background group-hover:-translate-x-1 group-active:-translate-x-1 transition-all pointer-events-none"
    />
</a>

<div class="p-8 pt-4">
    {@render children()}
</div>
