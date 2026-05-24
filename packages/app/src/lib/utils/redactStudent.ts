import redactedStudentsRaw from "@cbse-wrapped/data/redacted.json";
import { title } from "radashi";
import * as v from "valibot";
import type { NonZeroInt } from "$lib/schemas";
import { RedactedStudentsSchema } from "$lib/schemas/RedactedSchema";

const redactedStudents = v.parse(RedactedStudentsSchema, redactedStudentsRaw);

/**
 * Redact any student's name, and yes Fuck You.
 * Searching up for name in ranked list still works.
 *
 * No need to use `title` when using this.
 */
export function fuckYou(rollnumber: NonZeroInt, name: string, transform: "as-is" | undefined = undefined): string {
    return redactedStudents.includes(rollnumber)
        ? "REDACTED"
        : transform === "as-is"
          ? name
          : title(name.toLocaleLowerCase());
}
