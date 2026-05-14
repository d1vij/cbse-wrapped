import { defineWorkspace } from "bunup";

export default defineWorkspace(
    [
        {
            name: "data",
            root: "packages/data",
            config: {
                entry: ["src/index.ts"],
            },
        },

        {
            name: "scraper",
            root: "packages/scraper",

            config: {
                entry: ["src/index.ts", "src/schemas/index.ts"],
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
