/**
 * NOTE: run this script using the `bun run orchestrator:compile`
 * command or directly using `bun`instead of transpiling it first
 * since the bunup dist folder resolution is broken and im too
 * lazy to fix it rn.
 */
import fs from "node:fs/promises";
import path from "node:path";
import { fetchForSchool, SchoolRecordSchema } from "@cbse-wrapped/scraper";
import chalk from "chalk";
import * as v from "valibot";
import { dataDir, schools } from "../index";

const studentDataDir = path.join(dataDir, "student-data");
const scrapedDataDir = path.join(dataDir, "scraped");

if ((await fs.exists(path.join(dataDir, "student-data"))) === false) {
    throw new Error(`student-data directory doesnt exist at ${dataDir}`);
}

for (const school of schools) {
    const schoolIn = path.join(studentDataDir, `${school}.json`);
    const schoolOut = path.join(scrapedDataDir, `${school}.json`);
    const studentInfo = v.parse(
        SchoolRecordSchema,
        await Bun.file(schoolIn).json(),
    );
    const scraped = await fetchForSchool(studentInfo);
    const json = JSON.stringify(scraped);
    await Bun.file(schoolOut).write(json);
    console.log(chalk.green(`Scraped successfully for ${school}`));
}
