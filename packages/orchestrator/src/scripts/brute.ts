import path from "node:path";
import { bruteForceParentsName, SchoolRecordSchema, SchoolResultSchema, type Student } from "@cbse-wrapped/scraper";
import { identity, select, selectFirst } from "radashi";
import * as v from "valibot";
import { dataDir } from "../index";

const dataJson = Bun.file(path.join(dataDir, "student-data", "dav.json"));
const schoolRecord = v.parse(SchoolRecordSchema, await dataJson.json());
const failedRollnumbers = select(
    v.parse(SchoolResultSchema, await Bun.file(path.join(dataDir, "scraped", "dav.json")).json()).failed,
    (f) => f.roll_number,
);
for (const rollnumber of failedRollnumbers) {
    try {
        const studentRecord = selectFirst(schoolRecord.students, identity, (s) => s.roll_number === rollnumber) as
            | Student
            | undefined;
        if (!studentRecord) throw new Error(`Cannot find record for student with rollnumber ${rollnumber}`);
        console.log(`trying ${studentRecord.name}`);
        const admitCardNumber = await bruteForceParentsName({
            roll_number: rollnumber,
            centre_number: schoolRecord.centre_number,
            school_number: schoolRecord.school_number,
            known_father: studentRecord.known_father,
            known_mother: studentRecord.known_mother,
        });

        if (admitCardNumber !== null) {
            console.log(`Found admit card number ${admitCardNumber} for ${studentRecord.name}`);
            studentRecord.admit_card_number = admitCardNumber;
        }
    } catch (e) {
        console.error(`Failed for ${rollnumber}:`, e);
    }
}

await dataJson.write(JSON.stringify(schoolRecord));
