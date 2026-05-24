import * as v from "valibot";
import { NonZeroIntSchema } from "./UnitsSchema";

export const RedactedStudentsSchema = v.array(NonZeroIntSchema);
export type RedactedStudents = v.InferInput<typeof RedactedStudentsSchema>;
