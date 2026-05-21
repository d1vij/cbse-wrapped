<script lang="ts">
type Props = {
    items: [string, string][];
};
const { items } = $props();
</script>

<ul class="space-y-2 grid grid-cols-[1fr_auto] justify-between w-full">
    {#each items as [label, content], idx (idx)}
        <li class="">
            <p class="text-subtle block text-sm text-wrap hyphens-auto">
                {label}
            </p>
            <p class="text-lg block">{content}</p>
        </li>
    {/each}
</ul>
