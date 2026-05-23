<script lang="ts">
    import { vibrateOnClick } from "@d1vij/shit-i-always-use/svelte";
    import uFuzzy from "@leeoniya/ufuzzy";
    import { ChevronRight } from "@lucide/svelte";
    import { select, similarity, title } from "radashi";
    import { IsFocusWithin } from "runed";
    import { resolve } from "$app/paths";
    import type { Student } from "$lib/schemas";

    type Props = {
        students: Student[];
        schoolName: string;
        rank_by: "rank_all_streams" | "rank_same_stream";
    };

    const { students, schoolName, rank_by }: Props = $props();

    // extract the names to act as reference for fuzzy searching
    let names = $derived(select(students, (s) => s.name_candidate));

    let inputElm = $state<HTMLInputElement | null>(null);
    let focused = new IsFocusWithin(() => inputElm);
    let query = $state("");
    const uf = new uFuzzy();
    const filtered = $derived.by(() => {
        if (query.length < 2) return students;
        const [indexes] = uf.search(names, query);
        return indexes?.map((i) => students[i]) || [];
    });
</script>

<h2 class="block mb-2 font-heading text-heading text-4xl">Students Ranked</h2>

<div class={["relative", "min-h-[20dvh]"]}>
    <label
        class="block w-full mb-8 sticky top-0 z-20 bg-background backdrop-blur pt-4"
    >
        <input
            bind:this={inputElm}
            bind:value={query}
            type="text"
            class="block w-full border border-muted/50 focus-within:border-muted focus:outline-none p-2 placeholder:text-subtle/40"
            placeholder="Search Name"
            spellcheck="false"
        />

        {#if query.length}
            <span class="block text-xs text-label">
                Found: {filtered.length}
            </span>
        {/if}
    </label>

    <ul class={["space-y-6"]}>
        {#each filtered as student (student.roll_number)}
            <li
                class={[
                    "student-item",
                    student[rank_by] === 1 && "first",
                    student[rank_by] === 2 && "second",
                    student[rank_by] === 3 && "third",
                ]}
            >
                <a
                    href={resolve("/school/[name]/student/[rollnumber]", {
                        name: schoolName,
                        rollnumber: student.roll_number.toString(),
                    })}
                    class="block group"
                    {@attach vibrateOnClick(100)}
                >
                    <h5 class="rollnumber">
                        <span class="rank">#{student[rank_by]}</span>
                        <span>
                            {student.roll_number}
                        </span>
                    </h5>
                    <span class="flex justify-between items-center">
                        <span>
                            {#if student.name_candidate === "DIVIJ VERMA"}
                                Divij Verma (that's me)
                            {:else}
                                {title(
                                    student.name_candidate.toLocaleLowerCase(),
                                )}
                            {/if}
                        </span>
                        <div
                            class="p-0.5 border border-muted border-dashed bg-background"
                        >
                            <ChevronRight
                                class="size-4 stroke-muted group-hover:translate-x-1 group-active:translate-x-1 transition-all"
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
    .student-item {
        position: relative;
        display: block;

        background-color: var(--color-surface);
        @apply border p-2 border-dashed;
        border-color: var(--color-muted);

        &.first .rank {
            background-color: #f0b820;
        }
        &.second .rank {
            background-color: #d4c4a8;
        }
        &.third .rank {
            background-color: #e08840;
        }
    }

    .rollnumber {
        position: absolute;

        @apply -top-3 text-sm  left-3 flex gap-1 right-3;
        span {
            background-color: var(--color-background);
            border-color: var(--color-muted);
            @apply px-1  border border-dashed;
        }
    }
</style>
