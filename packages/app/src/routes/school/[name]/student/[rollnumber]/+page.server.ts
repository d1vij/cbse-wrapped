import { error } from "@sveltejs/kit";
import { selectFirst } from "radashi";
import * as v from "valibot";
import { NonZeroIntSchema } from "$lib/schemas/UnitsSchema.js";

const ParamsSchema = v.object({
    rollnumber: v.pipe(v.string(), v.toNumber(), NonZeroIntSchema),
});
export async function load({ params, parent }) {
    const result = v.safeParse(ParamsSchema, params);
    if (!result.success) {
        error(422, `Invalid rollnumber format: ${params.rollnumber}`);
    }

    const { results } = await parent();
    const student = selectFirst(
        results.students,
        (s) => s,
        (s) => s.roll_number === result.output.rollnumber,
    );
    if (student === undefined) {
        error(404, `No student found with rollnumber: ${params.rollnumber}`);
    }
    return {
        student,
        results,
    };
}
