<script lang="ts">
type Props = {
    items: [string, string][];
};
const { items } = $props();
</script>

{#each items as [label, content], idx (idx)}
    <li class="block">
        <p class="text-subtle block text-sm text-wrap">
            {label}
        </p>
        <p class="block">{content}</p>
    </li>
{/each}
