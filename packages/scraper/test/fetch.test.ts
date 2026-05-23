import { describe, expect, test } from "bun:test";
import path from "node:path";
import { generateAdmitCardNumber } from "~/lib";
import { fetchResults } from "~/lib/fetchResults";

test("Known Fetching", async () => {
    const rollnumber = "15623245";
    const admitnumber = "MA453022";

    const results = await fetchResults({
        admitnumber,
        rollnumber,
    });

    await Bun.write(path.join(__dirname, `../dist/scraped/${rollnumber}.json`), JSON.stringify(results, null, 4));

    expect(results).toBeObject();
}, 15_000);

describe("Unknown Fetching", () => {
    test("First", async () => {
        const rollnumber = "15623244";
        const admitnumber = generateAdmitCardNumber({
            fathers_name: "jee",
            mothers_name: "jee",
            centre_number: "822285",
            school_number: "30058",
            roll_number: rollnumber,
        });

        const results = await fetchResults({
            admitnumber,
            rollnumber,
        });

        await Bun.write(path.join(__dirname, `../dist/scraped/${rollnumber}.json`), JSON.stringify(results, null, 4));

        expect(results).toBeObject();
    }, 15_000);

    test("Second", async () => {
        const rollnumber = "15623263";
        const admitnumber = generateAdmitCardNumber({
            fathers_name: "inde",
            mothers_name: "inde",
            centre_number: "822285",
            school_number: "30058",
            roll_number: rollnumber,
        });

        const results = await fetchResults({
            admitnumber,
            rollnumber,
        });

        await Bun.write(path.join(__dirname, `../dist/scraped/${rollnumber}.json`), JSON.stringify(results, null, 4));

        expect(results).toBeObject();
    }, 15_000);
});
