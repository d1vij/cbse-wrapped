<script lang="ts">
import x from "@cbse-wrapped/data/results/dav.json";
import s from "@cbse-wrapped/data/streams.json";
import { title } from "radashi";
import { resolve } from "$app/paths";
import Patch from "$lib/components/Patch.svelte";
</script>

{#snippet Link(title: string, href: string, external: boolean = false)}
    <a
        class="underline decoration-primary decoration-wavy decoration-2"
        {href}
        target={external ? "_blank" : "_self"}>{title}</a
    >
{/snippet}

{#snippet Italic(content: string)}
    <span class="italic">{content}</span>
{/snippet}

<div class="space-y-4 p-8">
    <h1 class="font-heading text-5xl font-black tracking-wide text-heading">CBSE Wrapped</h1>

    <div class={["mt-6 space-y-4 px-2 leading-snug"]}>
        <p>
            I exploited Digilocker's own endpoint, and used it scrape the results. Then cleaned,
            analyzed and compiled them to generate a report on CBSE 2026's Results.
        </p>
        <p>
            It only requires the list of student names and {@render Italic(
                "just one student's rollnumber"
            )} to scrape & generate results of the whole school. (A massive oversighting done by CBSE)
        </p>
        <p>
            This project is {@render Link(
                "open source",
                "https://github.com/d1vij/cbse-wrapped",
                true
            )}.
        </p>
    </div>

    <h2 class="font-heading text-3xl text-heading" id="scrapped-schools">
        Some schools that I have scraped
    </h2>
    <nav class="gap-2">
        <ol class="navlist">
            <li>
                {@render Link("DAV Pune", resolve("/school/[name]", { name: "dav" }))}
            </li>
            <!-- <li>
                {@render Link("Orchid Pune", resolve("/school/[name]", { name: "orchid" }))}
            </li> -->
        </ol>
    </nav>
</div>

<style lang="postcss">
    @reference "tailwindcss";

    .navlist {
        @apply list-inside list-decimal;
    }
</style>
