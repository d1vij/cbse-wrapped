<script lang="ts">
import { ChevronLeft } from "@lucide/svelte";
import { resolve } from "$app/paths";

const { children } = $props();
</script>

<a
    class="ml-8 mt-4 block text-base bg-heading border-muted w-fit p-2 px-2 group"
    href={".."}
>
    <ChevronLeft
        class="size-4 stroke-background group-hover:-translate-x-1 group-active:-translate-x-1 transition-all pointer-events-none"
    />
</a>

<div class="p-8 pt-4">
    {@render children()}
</div>
