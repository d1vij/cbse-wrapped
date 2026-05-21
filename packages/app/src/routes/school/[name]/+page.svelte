<script lang="ts">
import { ChevronRight, MoveUpRight } from "@lucide/svelte";
import hyphen from "hyphen/en";
import { select, sort, title } from "radashi";
import { resolve } from "$app/paths";
import ContentList from "$lib/components/ContentList.svelte";
import StudentsRanked from "$lib/components/StudentsRanked.svelte";

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

const rankedStudents = $derived(
    sort(
        select(students, (s) => ({
            name_candidate: s.name_candidate,
            roll_number: s.roll_number,
            rank: s.rank_all_streams,
        })),
        (s) => s.rank,
    ),
);
</script>

<div class="space-y-5 pb-12">
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
                        <ChevronRight
                            class="size-4 stroke-muted group-hover:translate-x-1 group-active:translate-x-1 transition-all"
                        />
                    </span>
                </a>
            </li>
        {/each}
    </ul>


    <StudentsRanked students={rankedStudents} schoolName={params.name} />
</div>

<style lang="postcss">
    @reference "tailwindcss";
</style>
