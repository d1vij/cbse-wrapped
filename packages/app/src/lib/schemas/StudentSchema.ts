import * as v from "valibot";
import { StreamIdSchema } from "$lib/schemas/StreamSchema";
import { PrimarySubjectSchema, SecondarySubjectSchema } from "$lib/schemas/SubjectSchema";
import { NonZeroFloatSchema, NonZeroIntSchema } from "$lib/schemas/UnitsSchema";

export const StudentSchema = v.strictObject({
    roll_number: NonZeroIntSchema,
    name_candidate: v.string(),
    name_father: v.string(),
    name_mother: v.string(),
    sex: v.picklist(["M", "F"]),
    catagory: v.union([v.string(), v.literal(false)]),
    candidate_type: v.picklist(["private", "regular"]),
    stream_id: StreamIdSchema,
    total_primary_subjects: NonZeroIntSchema,
    primary_subjects: v.strictObject({
        sub_1: PrimarySubjectSchema,
        sub_2: PrimarySubjectSchema,
        sub_3: PrimarySubjectSchema,
        sub_4: PrimarySubjectSchema,
        sub_5: PrimarySubjectSchema,
        sub_6: v.union([v.null(), PrimarySubjectSchema]),
    }),

    secondary_subjects: v.array(SecondarySubjectSchema),
    cleared_all_subjects: v.boolean(),
    result_status: v.picklist(["pass", "compartment"]),
    compartment_subject_codes: v.string(),
    total_marks: NonZeroIntSchema,

    percentage: NonZeroFloatSchema,
    percentile_same_stream: NonZeroFloatSchema,
    percentile_all_streams: NonZeroFloatSchema,
    rank_all_streams: NonZeroIntSchema,
    rank_same_stream: NonZeroIntSchema,
});

export type Student = v.InferInput<typeof StudentSchema>;
