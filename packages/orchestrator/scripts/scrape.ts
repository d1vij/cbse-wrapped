import path from "node:path";
import fs from "node:fs/promises";
import { fetchForSchool, SchoolRecordSchema } from "@cbse-wrapped/scraper";
import * as v from "valibot";
import { dataDir } from "~/index";

const studentDataDir = path.join(dataDir, "student-data");
const scrapedDataDir = path.join(dataDir, "scraped");

if ((await fs.exists(path.join(dataDir, "student-data"))) === false) {
    throw new Error(`student-data directory doesnt exist at ${dataDir}`);
}
const davIn = path.join(studentDataDir, "dav.json");
const davOut = path.join(scrapedDataDir, "dav.json");

const studentInfo = v.parse(SchoolRecordSchema, await Bun.file(davIn).json());
const scraped = await fetchForSchool(studentInfo);

const json = JSON.stringify(scraped);
await Bun.file(davOut).write(json);
