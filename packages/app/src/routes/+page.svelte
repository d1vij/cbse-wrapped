<script lang="ts">
    import { vibrateOnClick } from "@d1vij/shit-i-always-use/svelte";
    import { ChevronRight } from "@lucide/svelte";
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
    <nav class="">
        {#snippet TheBetterUXWalaButtonToOtherPageCuzPplCantSeemToUnderstandSwigglyLinks(title: string, href: string)}
            <li>
                <a href={href}
                    class="block bg-surface border border-dashed p-2 border-muted group"

                    {@attach vibrateOnClick(100)}
                >
                    <span class="flex justify-between items-center">
                        <span>
                            {title}
                        </span>
                        <div class="p-0.5 border border-muted border-dashed bg-background">
                            <ChevronRight
                                class="size-4 stroke-muted group-hover:translate-x-1 group-active:translate-x-1 transition-all"
                            />
                        </div>
                    </span>
            </a>
            </li>
        {/snippet}
        <ol class="space-y-3">
            {@render TheBetterUXWalaButtonToOtherPageCuzPplCantSeemToUnderstandSwigglyLinks("DAV Pune", resolve("/school/[name]", { name: "dav" }))}
            {@render TheBetterUXWalaButtonToOtherPageCuzPplCantSeemToUnderstandSwigglyLinks("Orchid Pune", resolve("/school/[name]", { name: "orchid" }))}
        </ol>
    </nav>
</div>

<style lang="postcss">
    @reference "tailwindcss";
</style>
