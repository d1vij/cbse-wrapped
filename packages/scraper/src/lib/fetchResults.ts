import chalk from "chalk";
import * as v from "valibot";
import { MARKER } from "~/lib/utils";

import { type CBSEResultResponse, SuccessOrFailedResponseSchema } from "~/schemas/CBSEResultSchema";

/**
 * Props which {@link fetchResults} takes
 */
export type FetchResultsProps = {
    rollnumber: string;
    admitnumber: string;
};

/**
 * Fetches result from digilocker using its internal api.
 * Takes in student's Admit Card number and Roll Number.
 * @param FetchResultProps containing student's admit card number and rollnumber
 * @returns Promise<{@link CBSEResult}>
 */
export async function fetchResults({ admitnumber, rollnumber }: FetchResultsProps): Promise<CBSEResultResponse> {
    // thats why api endpoints should be behind some authetication
    // fetch copied as is from digilocker's site
    const response = await fetch("https://results.digilocker.gov.in/api/cbse/hscer/results", {
        method: "POST",
        headers: {
            accept: "*/*",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "x-requested-with": "XMLHttpRequest",
            cookie: "Path=/",
            Referer: "https://results.digilocker.gov.in/CBSE12th2026resultXIInruew.html",
        },

        // since we are generating the rollnumber and admit card number it can be inserted as is
        // but ideally this should be encoded into url params
        body: `rroll=${rollnumber}&year=2026&admn_id=${admitnumber}`,
    });

    const json = await response.json();
    const results = v.safeParse(SuccessOrFailedResponseSchema, json);
    if (!results.success) {
        console.log(json);
        throw new Error(
            `${MARKER} Error in Result Parsing.\n${chalk.yellow("Issues")}:\n${JSON.stringify(results.issues, null, 4)}`,
        );
    }

    const parsed = results.output;
    if (parsed.status === 400) {
        throw new Error(
            `${MARKER} Error fetching results for ${rollnumber} | ${admitnumber}.\n Error: ${chalk.yellow(json.error_code)} | ${json.message}`,
        );
    }

    return parsed;
}
