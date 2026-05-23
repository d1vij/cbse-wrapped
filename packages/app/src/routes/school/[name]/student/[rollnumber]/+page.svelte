<script lang="ts">
    import { generateAdmitCardNumber } from "@cbse-wrapped/scraper";
    import { round, select, title } from "radashi";
    import { resolve } from "$app/paths";
    import { page } from "$app/state";
    import ContentList from "$lib/components/ContentList.svelte";
    import Patch from "$lib/components/Patch.svelte";

    const { data, params } = $props();
    const { results, student } = $derived(data);
    const {
        name_candidate,
        roll_number,
        sex,
        name_father,
        name_mother,
        percentage,
        cleared_all_subjects,
        rank_all_streams,
        percentile_all_streams,
        percentile_same_stream,
        rank_same_stream,
        primary_subjects,
        compartment_subject_codes,
        total_primary_subjects,
        secondary_subjects,
    } = $derived(student);

    let stream = $derived(results.streams[student.stream_id]);

    function titleCase(str: string) {
        return title(str.toLocaleLowerCase());
    }

    const ordinal = new Intl.PluralRules("en", { type: "ordinal" });
    const suffixes = {
        one: "st",
        two: "nd",
        few: "rd",
        other: "th",
    } as Record<Intl.LDMLPluralRule, string>;
    function resolveTh(n: number): string {
        return suffixes[ordinal.select(n)];
    }

    const failedSubjects = $derived.by(() => {
        if (compartment_subject_codes.length === 3)
            return titleCase(results.subjects_available[compartment_subject_codes]);
        return `subjects with codes ${compartment_subject_codes}`;
    });
</script>

<svelte:head>
    <title>{titleCase(name_candidate)} of {params.name} · CBSE Wrapped</title>
</svelte:head>

<div class="mb-4">
    <h1 class="font-heading text-heading text-5xl wrap-break-word hyphens-auto font-bold block">
        {titleCase(name_candidate)}
    </h1>
    <h2 class={["block text-start text-sm text-label w-fit"]}>
        <span class={["px-1", sex === "F" ? "bg-[#E0A3A9] " : " bg-[#A3C3D9]"]}>
            {roll_number} <span class="select-none">|</span>
            {generateAdmitCardNumber({
                centre_number: results.centre_number.toString(),
                fathers_name: name_father,
                mothers_name: name_mother,
                roll_number: roll_number.toString(),
                school_number: results.school_number.toString(),
            })}
        </span>
        <span>
            ({stream.primary_stream} + {stream.secondary_stream})
        </span>
    </h2>
</div>

<!-- too corny ?? -->
<!-- <p>
    {sex === "M" ? "son" : "daughter"} of {titleCase(name_father)} and {titleCase(
        name_mother,
    )}, studied in {titleCase(results.school_name)} as a {titleCase(
        candidate_type,
    )} student in stream {stream.primary_stream}
    with {stream.secondary_stream} as the optional subject.
</p> -->

<div class="space-y-5">
    <p>
        Out of {total_primary_subjects === 5 ? "five" : "six"} total subjects,
        {sex === "M" ? "he" : "she"}
        {#if cleared_all_subjects}
            has passed in all {sex === "M" ? "his" : "her"} subjects
        {:else}
            has passed in all but {failedSubjects},
        {/if}

        with a gross percentage of {round(percentage, 2)}% across all subjects, which ranks {sex ===
        "M"
            ? "him"
            : "her"}
        {rank_all_streams}{resolveTh(rank_all_streams)}, in the whole school with a percentile of {round(
            percentile_all_streams,
            2,
        )} and
        {rank_same_stream}{resolveTh(rank_same_stream)} with {round(percentile_same_stream, 2)} percentile
        within {sex === "M" ? "his" : "her"}
        <a
            href={resolve("/school/[name]/stream/[id]", {
                name: page.params.name || "",
                id: stream.stream_id,
            })}
            class="underline decoration-wavy decoration-2 decoration-accent">stream</a
        >.
    </p>
</div>

<h2 class="font-heading text-heading text-4xl mb-3 mt-4">Subjects</h2>
<ol class="space-y-5 list-decimal list-inside">
    {#each Object.values(primary_subjects).filter((s) => s !== null) as subject (subject.subject_id)}
        <li class="block">
            <h2 class="font-heading text-heading text-2xl mb-2 list-item">
                {titleCase(results.subjects_available[subject.subject_id])}
            </h2>
            <div class="bg-surface p-2">
                <div class="size-full border-2 border-background border-dashed p-2">
                    <ul class="grid grid-cols-[1fr_auto] px-2">
                        <ContentList
                            items={[
                                ["Marks Theory", subject.marks_theory],
                                ["Marks Practicals", subject.marks_practicals],
                                ["Grade", subject.grade],
                                ["School Percentile", round(subject.percentile_all_streams, 2)],
                                [
                                    "School Rank",
                                    `${subject.rank_all_streams}${resolveTh(subject.rank_all_streams)}`,
                                ],
                                [
                                    "Stream Rank",
                                    `${subject.rank_same_stream}${resolveTh(subject.rank_same_stream)}`,
                                ],
                            ]}
                        />
                    </ul>
                </div>
            </div>
        </li>
    {/each}
</ol>

<h2 class="font-heading text-heading text-4xl mb-3 mt-4">Secondary Subjects</h2>

<div class="bg-surface p-2">
    <div class="size-full border-2 border-background border-dashed p-3">
        <ul class="px-2">
            {#each secondary_subjects as { grade, subject_id } (subject_id)}
                <li>
                    <p class="text-subtle block text-sm text-wrap">
                        {titleCase(results.subjects_available[subject_id])}
                    </p>
                    <p class="block">{grade}</p>
                </li>
            {/each}
        </ul>
    </div>
</div>

<div class="mb-12"></div>
