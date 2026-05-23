import { sveltekit } from "@sveltejs/kit/vite";
import tailwindcss from "@tailwindcss/vite";
import { visualizer } from "rollup-plugin-visualizer";
import { defineConfig } from "vite";

export default defineConfig({
    server: {
        host: true,
        allowedHosts: true,
    },
    plugins: [tailwindcss(), sveltekit(), visualizer()],
});
