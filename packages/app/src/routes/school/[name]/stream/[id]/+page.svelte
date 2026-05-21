<script lang="ts">
import hyphen from "hyphen/en";
import { round, title } from "radashi";
import { resolve } from "$app/paths";
import ContentList from "$lib/components/ContentList.svelte";

const { data, params } = $props();
const { results, stream, students_ranked, subjects } = $derived(data);
</script>

<div class="space-y-5">
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

    <ContentList
        items={[
            ["Total Students", stream.students_total],
            ["Students Passed", stream.students_passed],
            ["Average Percentage", round(stream.percentage_mean, 2)],
            ["Median Percentage", round(stream.percentage_median, 2)],
            ["Maximum Percentage", round(stream.percentage_max, 2)],
            ["Minimum Percentage", round(stream.percentage_min, 2)],
        ]}
    />

    <h2 class="font-heading text-heading text-4xl">Subjects</h2>
    <ul class="list-decimal list-inside">
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

    <h2 class="font-heading text-heading text-4xl">Students Ranked</h2>
    <ul class="space-y-6">
        {#each students_ranked as student, idx (student.roll_number)}
            <li class="student-item">
                <a
                    href={resolve("/school/[name]/student/[rollnumber]", {
                        name: params.name,
                        rollnumber: student.roll_number.toString(),
                    })}
                    class="block"
                >
                    <h5 class="rollnumber">
                        <span class="rank">#{idx + 1}</span>
                        <span>
                            {student.roll_number}
                        </span>
                    </h5>
                    {title(student.name_candidate.toLocaleLowerCase())}
                </a>
            </li>
        {/each}
    </ul>
</div>

<style lang="postcss">
    @reference "tailwindcss";
    .student-item {
        position: relative;
        display: block;

        background-color: var(--color-surface);
        @apply border p-2 border-dashed;
        border-color: var(--color-muted);

        &:nth-child(1) .rank {
            background-color: #f0b820;
        }
        &:nth-child(2) .rank {
            background-color: #d4c4a8;
        }
        &:nth-child(3) .rank {
            background-color: #e08840;
        }
    }

    .rollnumber {
        position: absolute;

        @apply -top-3 text-sm  left-3 flex justify-between right-3;
        span {
            background-color: var(--color-background);
            border-color: var(--color-muted);
            @apply px-1  border border-dashed;
        }
    }
</style>
