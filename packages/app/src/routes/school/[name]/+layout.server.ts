import { error } from "@sveltejs/kit";
import * as v from "valibot";
import {
    type SchoolResult,
    SchoolResultSchema,
} from "$lib/schemas/SchoolResultSchema.js";

const results = {
    dav: import("@cbse-wrapped/data/results/dav.json"),
} as const;

const ParamsSchema = v.object({
    name: v.picklist(Object.keys(results) as (keyof typeof results)[]),
});

export async function load({ params }) {
    const paramsResult = v.safeParse(ParamsSchema, params);
    if (!paramsResult.success) {
        error(404, `No school found with name ${params.name}`);
    }

    const resultJson = (await results[paramsResult.output.name]).default;
    const resultJsonResult = v.safeParse(SchoolResultSchema, resultJson, {
        abortEarly: true,
    });

    if (!resultJsonResult.success) {
        for (const issue of resultJsonResult.issues) {
            console.log(issue.message);
        }
        error(422, `Errors in validating result json`);
    }
    return {
        results: resultJsonResult.output as SchoolResult,
    };
}
