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
                entry: ["src/index.ts", "scripts/compile.ts", "scripts/scrape.ts"],
            },
        },
    ],
    {
        format: ["esm"],
        dts: {
            inferTypes: true,
        },
    },
);
