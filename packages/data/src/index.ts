import path from "node:path";

import { fetchForSchool } from "@cbse-wrapped/scraper";

export async function generateData() {
    const DataDir = path.join(__dirname, "../");
    console.log(`DataDir: ${DataDir}`);

    const davIn = Bun.file(path.join(DataDir, "student-data", "dav.json"));
    const davOut = Bun.file(path.join(DataDir, "results", "dav.json"));
    await fetchForSchool(davIn, davOut);

    const orchidIn = Bun.file(
        path.join(DataDir, "student-data", "orchid.json"),
    );
    const orchidOut = Bun.file(path.join(DataDir, "results", "orchid.json"));
    await fetchForSchool(orchidIn, orchidOut);
}

if (import.meta.main) {
    await generateData();
}
