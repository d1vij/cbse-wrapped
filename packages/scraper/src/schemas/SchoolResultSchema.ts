import * as v from "valibot";
import { CBSEResultResponseSchema } from "~/schemas/CBSEResultSchema";
import { FailedResultFetchSchema } from "~/schemas/FailedResultFetchSchema";

export const SchoolResultSchema = v.object({
    success: v.array(CBSEResultResponseSchema),
    failed: v.array(FailedResultFetchSchema),
});

export type SchoolResult = v.InferInput<typeof SchoolResultSchema>;
