<script lang="ts">
    import { vibrateOnClick } from "@d1vij/shit-i-always-use/svelte";
    import { resolve } from "$app/paths";
</script>

{#snippet Link(title: string, href: string, external: boolean = false)}
    <a
        class="underline decoration-primary decoration-wavy decoration-2"
        {href}
        target={external ? "_blank" : "_self"}
        {@attach vibrateOnClick(50)}>{title}</a
    >
{/snippet}

<div class="space-y-4 p-8">
    <h1 class="font-heading text-5xl font-black tracking-wide text-heading">CBSE Wrapped</h1>

    <div
        class={[
            "mt-10",
            "prose-xl prose-stone prose-h1:text-5xl prose-hr:border-dashed",
            "prose-headings:font-heading prose-headings:text-heading prose-headings:font-semibold prose-ol:list-decimal prose-ul:list-disc",
            "prose-a:underline prose-a:decoration-wavy prose-a:decoration-accent",
            "prose-pre:overflow-x-scroll prose-pre:scrollbar-none prose-pre:text-sm",
        ]}
    >
        <h2 id="disclaimer">Disclaimer</h2>
        <p>
            The student names used in this project are fictitious and have been used for
            illustrative purposes only. Any resemblance to the names or results of actual students,
            past or present, is entirely coincidental.
        </p>
        <hr />
        <p>
            This project demonstrates a <b>hypothetical</b> senario wherein, I reverse engineered DigiLocker's
            results API to scrape the CBSE 2026 results, processed it through a data cleaning and analysis
            pipeline, and compiled it to create this report.
        </p>
        <p>
            The report includes an overall school performance summary, a breakdown by stream, and
            individual student overviews. Because some students are missing, the overall analysis
            may not be fully accurate, but it still provides a reliable indication of the school's
            performance.
        </p>
        <p>
            I recommend reading more about this project {@render Link(
                "here",
                resolve("/the-blog-part"),
            )}. This project is also fully {@render Link(
                "open source",
                "https://github.com/d1vij/cbse-wrapped",
                true,
            )}.
        </p>
        <p>
            For any questions, suggestions, or requests for redaction, send a mail to {@render Link(
                "leenukhs@gmail.com",
                "mailto:leenukhs@gmail.com",
            )}.
        </p>
    </div>

    <h2 class="font-heading text-3xl text-heading" id="scrapped-schools">Schools</h2>
    <nav class="gap-2">
        <ol class="navlist">
            <li>
                {@render Link("DAV Pune", resolve("/school/[name]", { name: "dav" }))}
            </li>
            <li>
                {@render Link("Orchid Pune", resolve("/school/[name]", { name: "orchid" }))}
            </li>
        </ol>
    </nav>
</div>

<style lang="postcss">
    @reference "tailwindcss";

    .navlist {
        @apply list-inside list-decimal;
    }
</style>
