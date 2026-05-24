import chalk from "chalk";
import { fork, parallel } from "radashi";
import * as v from "valibot";

import { fetchResults, generateAdmitCardNumber } from "~/lib";
import { MARKER } from "~/lib/utils";

import type { CBSEResultResponse } from "~/schemas/CBSEResultSchema";
import type { FailedResultFetch } from "~/schemas/FailedResultFetchSchema";

import { type SchoolRecord, SchoolRecordSchema, type Student } from "~/schemas/SchoolRecordsSchema";
import { type SchoolResult, SchoolResultSchema } from "~/schemas/SchoolResultSchema";

/**
 * Fetches the result for a single student.
 * @param student {@link Student}
 * @param commonData Object containing `school_number` and `centre_number` corresponding to the student
 * @returns Promise of {@link CBSEResultResponse} if the result was found or {@link FailedResultFetch} otherwise.
 */
async function fetchStudent(
    student: Student,
    commonData: {
        school_number: string;
        centre_number: string;
    },
): Promise<CBSEResultResponse | FailedResultFetch> {
    let admitnumber: string;
    try {
        admitnumber = generateAdmitCardNumber({
            ...commonData,
            // use the parent's name if provided, or else fallback to the student's name
            // since we only require the letters from the surname for generating the
            // admit card number. passing parent's name is useful for the students
            // who's parent's surnames are different.
            fathers_name: student.name_father ?? student.name,
            mothers_name: student.name_mother ?? student.name,
            roll_number: student.roll_number,
        });
    } catch (e: unknown) {
        if (e instanceof Error) {
            console.log(`${MARKER} Error in generating admit card number. Error: ${e.message}`);
        } else throw e;

        return {
            status: "failed",
            student_name: student.name,
            roll_number: student.roll_number,
        } satisfies FailedResultFetch;
    }

    try {
        const results = await fetchResults({
            admitnumber,
            rollnumber: student.roll_number,
        });
        return results;
    } catch (e: unknown) {
        if (e instanceof Error) {
            console.log(`${MARKER} Error in fetching resuls. Error: ${e}`);

            return {
                status: "failed",
                student_name: student.name,
                roll_number: student.roll_number,
            } satisfies FailedResultFetch;
        }

        throw e;
    }
}

/**
 * Fetches result for a single school. A school represents an {@link SchoolRecordSchema} wherein all the {@link Student} have same `school_number` and `centre_number`
 * @param data SchoolRecord
 * @returns Promise<SchoolResult>
 */
export async function fetchForSchool(data: SchoolRecord): Promise<SchoolResult> {
    // fetching 10 parallel requests is pretty fast even for 100+ students
    // without getting ratelimited whatsoever. so increasing it might not be beneficial per se
    const results = await parallel<Student, FailedResultFetch | CBSEResultResponse>(10, data.students, (student) => {
        console.log(`${MARKER} Fetching result for ${student.name}`);
        return fetchStudent(student, {
            centre_number: data.centre_number,
            school_number: data.school_number,
        });
    });

    const [failed, successful] = fork(results, (r) => r.status === "failed");

    console.log(
        `${MARKER} Scraped (${chalk.green(successful.length)} + ${chalk.red(failed.length)})/${data.students.length} results.`,
    );

    return v.parse(SchoolResultSchema, {
        success: successful,
        failed: failed,
    });
}
