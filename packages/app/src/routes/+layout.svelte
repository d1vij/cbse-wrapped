<script lang="ts">
    import "./layout.css";
    import favicon from "$lib/assets/favicon.svg";

    let { children } = $props();
</script>

<svelte:head
    ><link rel="icon" href={favicon} />

    <title>CBSE Wrapped</title>
</svelte:head>

<div class="w-[min(100%,--spacing(120))] md:py-10 mx-auto">
    {@render children()}
</div>
<!-- <div class="flex min-h-dvh w-dvw flex-col justify-between">
    <footer
        class="flex h-10 w-full items-center justify-center bg-subtle font-mono text-xs font-semibold text-muted"
    >
        <span
            >Created by @<a
                href="https://github.com/d1vij"
                class="underline decoration-wavy"
                target="_blank">d1vij</a
            > | Divij Verma</span
        >
    </footer>
</div> -->
