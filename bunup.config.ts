import { defineWorkspace } from "bunup";

export default defineWorkspace(
    [
        {
            name: "app",
            root: "packages/app",

            config: {
                outDir: "dist/schemas",
                entry: ["src/lib/schemas/index.ts"],
            },
        },
        {
            name: "scraper",
            root: "packages/scraper",

            config: {
                entry: ["src/index.ts", "src/schemas/index.ts"],
            },
        },
        // {
        //     name: "orchestrator",
        //     root: "packages/orchestrator",

        //     config: {
        //         outDir: "dist",
        //         entry: [
        //             "src/index.ts",
        //             "src/scripts/compile.ts",
        //             "src/scripts/scrape.ts",
        //         ],
        //     },
        // },
    ],
    {
        format: ["esm"],
        target: "bun",
        sourcemap: "linked",
        clean: true,
        dts: {
            inferTypes: true,
        },
    },
);
