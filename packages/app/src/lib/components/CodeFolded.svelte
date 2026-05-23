<script lang="ts">
    import { dedent } from "radashi";
    import type { BundledLanguage } from "shiki";
    import { codeToHtml } from "shiki";

    type Props = {
        code: string;
        lang: BundledLanguage;
    };

    const { code, lang }: Props = $props();

    // svelte-ignore state_referenced_locally
    const highlighted = await codeToHtml(dedent(code), {
        lang,
        theme: "gruvbox-light-medium",
    });

    let isOpen = $state(false);
</script>

<div class="relative bg-background">
    <div class={[!isOpen && "max-h-70 overflow-clip"]}>
        {@html highlighted}
    </div>
    {#if !isOpen}
        <button
            class={["text-lg cursor-pointer", "block bg-[#fbf1c7] w-full mt-0.5 px-1 text-lg"]}
            onclick={() => (isOpen = true)}>Expand</button
        >
    {/if}
</div>
