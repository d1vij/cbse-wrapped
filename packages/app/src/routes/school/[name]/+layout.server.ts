import { error } from "@sveltejs/kit";
import * as v from "valibot";
import type { SchoolResult } from "$lib/schemas/SchoolResultSchema.js";

const schoolResults = {
    dav: import("@cbse-wrapped/data/results/dav.json"),
    orchid: import("@cbse-wrapped/data/results/orchid.json"),
} as const;

const ParamsSchema = v.object({
    name: v.picklist(Object.keys(schoolResults) as (keyof typeof schoolResults)[]),
});

export async function load({ params }) {
    const paramsResult = v.safeParse(ParamsSchema, params);
    if (!paramsResult.success) {
        error(404, `No school found with name ${params.name}`);
    }

    const results = (await schoolResults[paramsResult.output.name]).default;
    return {
        results: results as SchoolResult, // we're gonna trust the compile fn in orchestrator
    };
}
