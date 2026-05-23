<script lang="ts">
    import hyphen from "hyphen/en";
    import { round, title } from "radashi";
    import ContentList from "$lib/components/ContentList.svelte";
    import StudentsRanked from "$lib/components/StudentsRanked.svelte";
    import StudentDistribution from "$lib/components/Visuals/StudentDistribution.svelte";

    const { data, params } = $props();
    const { results, stream, students_ranked, subjects } = $derived(data);
</script>


<svelte:head>
    <title>{stream.primary_stream} + {stream.secondary_stream} at {params.name} · CBSE Wrapped</title>
</svelte:head>

<div class="pb-15">
    <span class="text-xs leading-tight font-heading text-subtle"
        >{title(results.school_name.toLocaleLowerCase())}</span
    >
    <h1
        class="font-heading text-heading text-5xl wrap-break-word hyphens-auto font-bold"
    >
        {await hyphen.hyphenate(
            `${stream.primary_stream} + ${stream.secondary_stream}`,
        )}
    </h1>

    <ul class="space-y-2 grid grid-cols-[1fr_auto] w-full mt-5">
        <ContentList
            items={[
                ["Total Students", stream.students_total],
                ["Students Passed", stream.students_passed],
            ]}
        />

        <StudentDistribution students={students_ranked} />
        <ContentList
            items={[
                ["Average Percentage", `${round(stream.percentage_mean, 2)}%`],
                ["Median Percentage", `${round(stream.percentage_median, 2)}%`],
                ["Maximum Percentage", `${round(stream.percentage_max, 2)}%`],
                ["Minimum Percentage", `${round(stream.percentage_min, 2)}%`],
            ]}
        />
    </ul>

    <h2 class="font-heading text-heading text-4xl">Subjects</h2>
    <ul class="mt-2 mb-7 list-decimal list-inside">
        {#each subjects as { subId, subName }, idx (subId)}
            <li class="flex justify-between w-full">
                <span class="">
                    {title(subName.toLocaleLowerCase())}
                </span>
                <span>
                    ({subId})
                </span>
            </li>
        {/each}
    </ul>

    <StudentsRanked
        schoolName={params.name}
        students={students_ranked}
        rank_by="rank_same_stream"
    />
</div>
