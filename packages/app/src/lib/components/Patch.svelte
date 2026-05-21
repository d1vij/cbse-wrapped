<script lang="ts">
import type { Snippet } from "svelte";
import type { ClassValue } from "svelte/elements";

const props: { children: Snippet; class?: ClassValue } = $props();
</script>

<div class={["patch", "p-6", props.class]}>
    {@render props.children()}
</div>

<style lang="postcss">
    @reference "tailwindcss";
    .patch {
        position: relative;
        @apply w-fit rounded-2xl shadow-sm;
        background-color: var(--color-primary);
        &::after {
            content: "";
            pointer-events: none;
            position: absolute;
            border-color: var(--color-background);
            @apply inset-2 rounded-xl border-2 border-dashed;
        }
    }
</style>
