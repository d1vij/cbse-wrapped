<script lang="ts">
import { MoveUpRight } from "@lucide/svelte";
import hyphen from "hyphen/en";
import { title } from "radashi";
import { resolve } from "$app/paths";
import ContentList from "$lib/components/ContentList.svelte";

const { data, params } = $props();
const {
    school_name,
    school_number,
    centre_number,
    date_of_results,
    students,
    streams,
    students_without_result,
} = $derived(data.results);
</script>

<div class="space-y-5">
    <h1
        class="font-heading text-heading text-5xl wrap-break-word hyphens-auto font-bold"
    >
        {title(school_name.toLocaleLowerCase())}
    </h1>

    <ContentList
        items={[
            ["School Number", school_number.toString()],
            ["Centre Number", centre_number.toString()],
            ["Date of Results", date_of_results],
            [
                "Total Students  (+ w/o Results)",
                `${students.length} (+ ${students_without_result})`,
            ],
        ]}
    />

    <h2 class="font-heading text-heading text-4xl">Streams Offered</h2>
    <ul class="space-y-2">
        {#each Object.values(streams) as stream (stream.stream_id)}
            <li>
                <a
                    class="block group bg-surface p-2 border border-muted border-dashed hover:shadow-xs transition-all ease-out duration-200"
                    href={resolve("/school/[name]/stream/[id]", {
                        id: stream.stream_id,
                        name: params.name,
                    })}
                >
                    <span class="flex justify-between items-center">
                        <h3 class="text-subtle">
                            {stream.primary_stream} + {stream.secondary_stream}
                        </h3>
                        <div class={["bg-muted p-1 rounded-lg"]}>
                            <MoveUpRight
                                class={[
                                    "size-4 stroke-background transition-all ease-out",
                                    "group-hover:-translate-y-0.5 group-hover:translate-x-0.5 group-hover:scale-102",
                                ]}
                            />
                        </div>
                    </span>
                </a>
            </li>
        {/each}
    </ul>
</div>

<style lang="postcss">
    @reference "tailwindcss";
</style>
