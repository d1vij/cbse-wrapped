<script lang="ts">
import { resolve } from "$app/paths";
import { page } from "$app/state";
</script>

<div class="p-8">
    <h1 class="font-heading text-3xl font-semibold text-heading">
        Error: {page.status}
    </h1>

    <p class="">
        {page.error?.message}
    </p>

    <a
        class="bg-primary px-4 py-1 mt-5 inline-block rounded hover:bg-accent active:bg-accent select-none cursor-pointer"
        href={resolve("/")}
    >
        Back to Home
    </a>
</div>
