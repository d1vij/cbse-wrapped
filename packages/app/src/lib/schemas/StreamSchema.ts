import * as v from "valibot";
import { SubjectIdSchema } from "$lib/schemas/SubjectSchema";
import { NonZeroFloatSchema } from "$lib/schemas/UnitsSchema";

export const StreamIdSchema = v.pipe(v.string(), v.uuid());
export type StreamId = v.InferInput<typeof StreamIdSchema>;

export const StreamSchema = v.strictObject({
    stream_id: StreamIdSchema,
    primary_stream: v.string(),
    secondary_stream: v.string(),
    subjects: v.array(SubjectIdSchema),

    students_total: v.number(),
    students_passed: v.number(),

    percentage_mean: NonZeroFloatSchema,
    percentage_median: NonZeroFloatSchema,
    percentage_max: NonZeroFloatSchema,
    percentage_min: NonZeroFloatSchema,
});
