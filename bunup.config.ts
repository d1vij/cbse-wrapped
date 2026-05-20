import { defineWorkspace } from "bunup";

export default defineWorkspace(
    [
        {
            name: "scraper",
            root: "packages/scraper",

            config: {
                entry: ["src/index.ts", "src/schemas/index.ts"],
            },
        },
        {
            name: "orchestrator",
            root: "packages/orchestrator",

            config: {
                outDir: "dist",
                entry: [
                    "src/index.ts",
                    "src/scripts/compile.ts",
                    "src/scripts/scrape.ts",
                ],
            },
        },
    ],
    {
        format: ["esm"],
        target: "bun",
        dts: {
            inferTypes: true,
        },
    },
);
