<script lang="ts">
    import { counting } from "radashi";
    import type { Student } from "$lib/schemas";

    type Props = {
        students: Student[];
    };

    const { students }: Props = $props();

    let { M: countBoys, F: countGirls } = $derived(counting(students, (s) => s.sex));
    let percentBoys = $derived((countBoys * 100) / students.length);
    let percentGirls = $derived(100 - percentBoys);
</script>

<li class="col-span-full">
    <p class="text-subtle block text-sm text-wrap mb-1">Student Distribution</p>

    <div
        class="relative h-6 w-full flex overflow-clip text-sm font-medium text-label"
    >
        <div
            class="bg-[#A3C3D9] h-full grid place-items-center"
            style:width={`${percentBoys}%`}
        >
            {countBoys}
        </div>
        <div
            class="bg-[#E0A3A9] h-full grid place-items-center"
            style:width={`${percentGirls}%`}
        >
            {countGirls}
        </div>
    </div>
</li>
