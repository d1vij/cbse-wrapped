import * as v from "valibot";
export const NonZeroIntSchema = v.pipe(v.number(), v.integer(), v.minValue(0));
export const NonZeroFloatSchema = v.pipe(v.number(), v.minValue(0));
export type NonZeroInt = v.InferInput<typeof NonZeroIntSchema>;
