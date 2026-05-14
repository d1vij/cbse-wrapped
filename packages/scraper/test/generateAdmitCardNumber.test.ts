import { expect, test } from "bun:test";
import { generateAdmitCardNumber } from "~/lib";

test("Generating Known admit cards", () => {
    expect(
        generateAdmitCardNumber({
            fathers_name: "verma",
            mothers_name: "verma",
            roll_number: "72826245",
            school_number: "30672",
            centre_number: "242277",
        }),
    ).toBe("MA453022");
});
