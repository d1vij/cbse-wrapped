/**
 * NOTE: run this script using the `bun run orchestrator:compile`
 * command or directly using `bun`instead of transpiling it first
 * since the bunup dist folder resolution is broken and im too
 * lazy to fix it rn.
 */
import path from "node:path";
import { SchoolResultSchema } from "@cbse-wrapped/app/schemas";
import { $ } from "bun";
import chalk from "chalk";
import * as v from "valibot";
import { dataDir, schools } from "../index";

const compilerPackageDir = path.join(import.meta.dir, "..", "..", "..", "result-compiler");

for (const school of schools) {
    const schoolIn = path.resolve(dataDir, "scraped", `${school}.json`);
    const schoolOut = path.resolve(dataDir, "results", `${school}.json`);

    await $`cd ${compilerPackageDir} \
    && uv run scripts/cli.py compile ${schoolIn} ${schoolOut}`.nothrow();

    // validate the pydantic schema with the valibot schema
    // at compile time to make sure both of them are in sync
    // this wont matter much for runtime since anyhow we're
    // validating the json on server during prerendering,
    // but this will drastically improve dev HMR for very big
    // results. also honestly there's no point in validating
    // on the app since no mutation will happen post result compilation
    const results = v.safeParse(SchoolResultSchema, await Bun.file(schoolOut).json());
    if (results.success) {
        console.log(chalk.green(`Result compilation and Validation successfull for ${school}`));
    } else {
        console.log(chalk.red("Result compilation and Validation failed with errors:"));
        console.log(v.summarize(results.issues));
    }
}
