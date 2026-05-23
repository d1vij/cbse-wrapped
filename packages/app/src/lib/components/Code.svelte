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
</script>

{@html highlighted}
