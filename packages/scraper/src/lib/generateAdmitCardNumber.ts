export type GenerateAdmitCardNumberProps = {
    fathers_name: string;
    mothers_name: string;
    roll_number: string;
    school_number: string;
    centre_number: string;
};

/**
 * Algorithm:
 * Admit card number is of format FMRRSSCC
 * Where the characters represent
 * => F: 2nd last letter of father's name. If name is `RAJESH KUMAR` then L is `A` from KUMAR
 * => M: last letter of mothers's name. If name is `RANI KUMARI` then L is `I` from KUMARI
 * => RR: last 2 digits of roll number. If roll number is 12345678 then RR is 78
 * => SS: first 2 digits of school number. If school number is 81293 then SS is 81
 * => CC: middle 2 digits of center number. If center number is 923147 then CC is 31
 *
 *  Then the Student's Admit Card number will be AI788131
 *
 * (sad that the original post explaining the algorithm on r/JEENEETards got deleted)
 */
export function generateAdmitCardNumber({
    centre_number,
    fathers_name,
    mothers_name,
    roll_number,
    school_number,
}: GenerateAdmitCardNumberProps): string {
    if (centre_number.length === 0 || centre_number.length % 2 !== 0) {
        throw new Error(`Center number (${centre_number} should be even digits long.`);
    }

    const F = fathers_name.at(-2);
    const M = mothers_name.at(-1);
    const rr = roll_number.slice(-2);
    const ss = school_number.slice(0, 2);

    const half = centre_number.length / 2 - 1;
    const cc = centre_number.slice(half, half + 2);

    // error if any part is missing or empty
    const falsey = [F, M, rr, ss, cc].filter((s) => !s || s.length === 0);
    if (falsey.length > 0) {
        throw new Error(
            `Some values are falsey: \nFathers Name: ${fathers_name} | ${F}Mothers Name: ${mothers_name} | ${M}\nRoll Number: ${roll_number} | ${rr}\nSchool Number: ${school_number} | ${ss}\nCenter Number: ${centre_number} | ${cc}`,
        );
    }

    return ((F as string) + (M as string) + rr + ss + cc).toUpperCase();
}
