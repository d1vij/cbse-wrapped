import * as v from "valibot";

export const StudentSchema = v.object({
    name: v.string(),
    roll_number: v.string(),
    name_mother: v.optional(v.string()),
    name_father: v.optional(v.string()),
    admit_card_number: v.optional(v.string()),
    known_father: v.optional(v.string()),
    known_mother: v.optional(v.string()),
});

export type Student = v.InferInput<typeof StudentSchema>;

export const SchoolRecordSchema = v.object({
    school_number: v.string(),
    centre_number: v.string(),
    students: v.array(StudentSchema),
});

export type SchoolRecord = v.InferInput<typeof SchoolRecordSchema>;
