import * as v from "valibot";
import { NonZeroFloatSchema, NonZeroIntSchema } from "$lib/schemas/UnitsSchema";

export const GradeSchema = v.picklist(["A1", "A2", "B1", "B2", "C1", "C2", "D1", "D2", "E"]);

export const SubjectIdSchema = v.pipe(
    v.string(),
    v.length(3),
    v.regex(/\d{3}/, "Subject Id must be 3 digits long string"),
);

export const PrimarySubjectSchema = v.strictObject({
    subject_id: SubjectIdSchema,
    passed: v.boolean(),
    grade: GradeSchema,

    marks_theory: NonZeroIntSchema,
    marks_practicals: NonZeroIntSchema,
    marks_total: NonZeroIntSchema,
    marks_total_words: v.string(),

    percentage: NonZeroFloatSchema,
    percentile_all_streams: NonZeroFloatSchema,
    rank_same_stream: NonZeroIntSchema,
    rank_all_streams: NonZeroIntSchema,
});

export const SecondarySubjectSchema = v.strictObject({
    subject_id: SubjectIdSchema,
    grade: GradeSchema,
});
