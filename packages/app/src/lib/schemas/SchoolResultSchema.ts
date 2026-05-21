import * as v from "valibot";
import { StreamIdSchema, StreamSchema } from "$lib/schemas/StreamSchema";
import { StudentSchema } from "$lib/schemas/StudentSchema";
import { SubjectIdSchema } from "$lib/schemas/SubjectSchema";
import { NonZeroFloatSchema, NonZeroIntSchema } from "$lib/schemas/UnitsSchema";

export const SchoolResultSchema = v.strictObject({
    school_number: NonZeroIntSchema,
    centre_number: NonZeroIntSchema,
    school_name: v.string(),
    date_of_results: v.string(),
    subjects_available: v.record(SubjectIdSchema, v.string()),
    streams: v.record(StreamIdSchema, StreamSchema),
    students: v.array(StudentSchema),
    students_without_result: v.number(),
    percentage_mean: NonZeroFloatSchema,
    percentage_median: NonZeroFloatSchema,
    percentage_max: NonZeroFloatSchema,
    percentage_min: NonZeroFloatSchema,
});
export type SchoolResult = v.InferInput<typeof SchoolResultSchema>;
