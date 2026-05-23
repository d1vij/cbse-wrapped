<script lang="ts">
    import { vibrateOnClick } from "@d1vij/shit-i-always-use/svelte";
    import { ChevronRight, MoveUpRight } from "@lucide/svelte";
    import { counting, round, select, sort, title } from "radashi";
    import { resolve } from "$app/paths";
    import ContentList from "$lib/components/ContentList.svelte";
    import StudentsRanked from "$lib/components/StudentsRanked.svelte";
    import StudentDistribution from "$lib/components/Visuals/StudentDistribution.svelte";

    const { data, params } = $props();
    const {
        school_name,
        school_number,
        centre_number,
        date_of_results,
        students,
        streams,
        students_without_result,
        percentage_mean,
        percentage_median,
        percentage_max,
        percentage_min,
        subjects_available,
    } = $derived(data.results);

    const rankedStudents = $derived(
        sort(
            select(students, (s) => s),
            // rank all streams corresponds to the school rank
            (s) => s.rank_all_streams,
        ),
    );
    const passedStudents = $derived(counting(students, (s) => (s.cleared_all_subjects ? "passed" : "failed")).passed);
</script>

<svelte:head>
    <title>{title(params.name)} · CBSE Wrapped</title>
</svelte:head>

<div class="pb-15">
    <h1
        class="font-heading text-heading text-5xl wrap-break-word hyphens-auto font-bold block mb-4"
    >
        {title(school_name.toLocaleLowerCase())}
    </h1>

    <ul class="space-y-2 grid grid-cols-[1fr_auto] w-full">
        <ContentList
            items={[
                ["School Number", school_number.toString()],
                ["Centre Number", centre_number.toString()],
                ["Date of Results", date_of_results],
                ["Subjects Offered", Object.keys(subjects_available).length],
                ["Total Students", students.length],
                ["Students Passed", passedStudents],
            ]}
        />

        <StudentDistribution {students} />

        <ContentList
            items={[
                ["Average Percentage", `${round(percentage_mean, 2)}%`],
                ["Median Percentage", `${round(percentage_median, 2)}%`],
                ["Maximum Percentage", `${round(percentage_max, 2)}%`],
                ["Minimum Percentage", `${round(percentage_min, 2)}%`],
            ]}
        />
    </ul>
    <h2 class="font-heading text-heading text-4xl mb-2 mt-4">Streams</h2>
    <ul class="space-y-4 mb-6">
        {#each Object.values(streams) as stream (stream.stream_id)}
            <li>
                <a
                    class="block group bg-surface p-2 border border-muted border-dashed hover:shadow-xs transition-all ease-out duration-200"
                    href={resolve("/school/[name]/stream/[id]", {
                        id: stream.stream_id,
                        name: params.name,
                    })}
                    {@attach vibrateOnClick(100)}
                >
                    <span class="flex justify-between items-center">
                        <h3 class="text-subtle">
                            {stream.primary_stream} + {stream.secondary_stream}
                        </h3>
                        <div class="p-0.5 border border-muted border-dashed bg-background">
                            <ChevronRight
                                class="size-4 stroke-muted group-hover:translate-x-1 group-active:translate-x-1 transition-all"
                            />
                        </div>
                    </span>
                </a>
            </li>
        {/each}
    </ul>

    <StudentsRanked students={rankedStudents} schoolName={params.name} rank_by="rank_all_streams" />
    

    
</div>

<style lang="postcss">
    @reference "tailwindcss";
</style>
