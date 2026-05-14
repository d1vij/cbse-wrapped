import * as v from "valibot";

/**
 * Object containing meta for the student's who's fetching failed
 */
export const FailedResultFetchSchema = v.object({
    status: v.literal("failed"),
    student_name: v.string(),
    roll_number: v.string(),
});

export type FailedResultFetch = v.InferInput<typeof FailedResultFetchSchema>;
