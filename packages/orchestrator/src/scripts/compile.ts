import path from "node:path";
import { $ } from "bun";
import { dataDir } from "~/index";

const compilerPackageDir = path.join(
    import.meta.dir,
    "..",
    "..",
    "..",
    "result-compiler",
);

const davIn = path.resolve(dataDir, "scraped", "dav.json");
const davOut = path.resolve(dataDir, "results", "dav.json");

await $`cd ${compilerPackageDir} \
    && uv run scripts/cli.py compile ${davIn} ${davOut}`.nothrow();
