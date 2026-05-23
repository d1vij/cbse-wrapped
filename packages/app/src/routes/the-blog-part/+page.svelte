<script lang="ts">
    import { vibrateOnClick } from "@d1vij/shit-i-always-use/svelte";
    import { ChevronLeft } from "@lucide/svelte";
    import { resolve } from "$app/paths";
    import Code from "$lib/components/Code.svelte";
    import CodeFolded from "$lib/components/CodeFolded.svelte";
    import admGenFn from "./admGenFn?raw";
    import divjiCleaned from "./divij-cleaned.json?raw";
    import divijResult from "./divij-raw.json?raw";
    import resultCurl from "./resultCurl.sh?raw";
    import resultCurlClean from "./resultCurlClean.sh?raw";
</script>

<svelte:head>
    <title>The Blog Part · CBSE Wrapped</title>
</svelte:head>

{#snippet BackButton()}
    <a
        class="block text-base bg-heading border-muted w-fit p-2 px-2 group"
        href={resolve("/")}
        {@attach vibrateOnClick(100)}
    >
        <ChevronLeft
            class="size-4 stroke-background group-hover:-translate-x-1 group-active:-translate-x-1 transition-all pointer-events-none"
        />
    </a>
{/snippet}

<div
    class={[
        "p-8 prose-xl prose-stone prose-h1:text-5xl",
        "prose-headings:font-heading prose-headings:text-heading prose-headings:font-semibold prose-ol:list-decimal prose-ul:list-disc",
        "prose-a:underline prose-a:decoration-wavy prose-a:decoration-accent",
        "prose-pre:overflow-x-scroll prose-pre:scrollbar-none prose-pre:text-sm",
    ]}
>
    <h1 class="">CBSE Wrapped</h1>

    {@render BackButton()}
    <p><a href="#disclaimer">Read the disclaimer first. </a></p>

    <section>
        <h2>Background</h2>
        <p>
            On the day of results, I found this (since deleted) post on reddit which explained the <i
                >algorithm</i
            >
            behind how Admit Card Numbers are generated, since the algorithm was pretty trivial, I created
            a
            <a href="https://d1vij.github.io/cbse-2026-admit-card-number-generator/" target="_blank"
                >simple site</a
            > to generate them provided some basic information about the student (and also that it gave
            me a reason to learn Vue, but whatever).
        </p>
        <p>What basic information you may ask ?? Well, it only takes</p>
        <ol>
            <li>Father's Name</li>
            <li>Mothers's Name</li>
            <li>Student's Rollnumber</li>
            <li>School Number</li>
            <li>and Center Number</li>
        </ol>
        <p>to generate the admit card number and thereby view the results of any student.</p>

        <h2>Generating the Admit Card Numbers</h2>
        <p>The admit card is composed of 8 characters.</p>
        <ul>
            <li>
                <p>
                    The first character is the 2<sup>nd</sup> last letter of Father's Full Name.
                </p>
            </li>
            <li>
                <p>The second character is the last letter of Mother's Full Name.</p>
            </li>
            <li>
                <p>The third and fourth characters are the last 2 digits of the roll number.</p>
            </li>
            <li>
                <p>The next two characters are the first 2 digits of the school number.</p>
            </li>

            <li>
                <p>The last two characters are the middle 2 digits of the centre number.</p>
            </li>
        </ul>
        <p></p>

        <!-- <div class="text-center">
                <span class="text-lg font-black font-mono flex justify-center items-center">
                    <span class="text-rose-400">F</span>
                    <span class="text-sky-400">M</span>
                    <span class="text-yellow-400">RR</span>
                    <span class="text-emerald-400">SS</span>
                    <span class="text-mauve-400">CC</span>
                </span>
            </div> -->
        <Code lang="ts" code={admGenFn} />

        <p>
            If the student was from my school (which they are), I would already have the school
            number and centre number. Getting their rollnumbers was also trivial since they are just
            sequential. The sole challenge was getting hand the name of parents, but if you notice
            carefully, the <i>"last n letter of parent's name"</i> was to be extracted from a union
            of <i>name</i> and
            <i>surname</i> both.
        </p>
        <p>
            This meant that in theory I could use just the student's full name, or infact just the
            surname in order to bypass this restriction, which I did, and it worked for the 90% of
            students, for whom, both the parents had the same surname as the student itself.
        </p>
    </section>

    <section>
        <h2>Scraping the results</h2>
        <p>
            Then I realised that if I can view the results of <i>any student</i> I could potentially
            view the results of <i>all the students</i>. And what is the easist way to view all the
            results ?? To Scrape them !!
        </p>

        <p>
            So I started poking around in the Network Panel of Devtools on the digilocker's result
            website to see how the result is requested from the backend.
        </p>

        <Code code={resultCurl} lang="sh" />

        <p>on stripping down to bare essentials</p>

        <Code code={resultCurlClean} lang="sh" />

        <p>
            and what can we notice here ?? An absence of any auth headers or cookies (well obviously
            since the rollnumbers and admit card numbers act as auth info, but again whatever).
        </p>

        <p>
            Taking the advantage of this very primitive API request model, I <a
                href="https://github.com/d1vij/cbse-wrapped/blob/main/packages/scraper/src/scrape/school.ts"
                target="_blank">wrote a simple script</a
            >
            which scrapes the result of all school students when fed in with student name and rollnumbers,
            and combines it down into a single response JSON.
        </p>

        <p>
            Fetching results for some students failed because of the difference in parent's surnames
            and they were thereby discarded.
        </p>
    </section>

    <section>
        <h2>Cleaning and Compiling the Results</h2>

        <p>
            The Digilocker's API returns result as a raw JSON object which is then rendered on their
            website. But this JSON was pretty vague to do any meaningful analysis on, so I fed it
            through a data cleaning pipeline which complied down the results into much more semantic
            structure.
        </p>

        <p>
            You can find annotations for every field of the response <a
                href="https://github.com/d1vij/cbse-wrapped/blob/main/packages/scraper/src/schemas/CBSEResultSchema.ts"
                target="_blank">here</a
            >.
        </p>

        <p>So something like this,</p>
        <CodeFolded code={divijResult} lang="json" />
        <p>got compiled into:</p>
        <CodeFolded code={divjiCleaned} lang="json" />

        <p>
            I further extracted out <i>common subject groups</i> to form streams and then extrapolated
            streams for each student. Then I calculated subject wise and the aggregate percentage, to
            rank the students by stream and across the whole school.
        </p>

        <p>
            You can see a compiled result <a
                target="_blank"
                href="https://github.com/d1vij/cbse-wrapped/blob/main/packages/data/data/results/dav.json"
                >here</a
            >.
        </p>
    </section>

    <section>
        <h2>The Architecture <sup class="align-super text-xs">(the fun section)</sup></h2>
        <p>
            The whole project is a <i
                >polyglot <sup>(a fancy way saying I used multiple languages)</sup></i
            > monorepo with the following packages
        </p>
        <ol>
            <li><i>scraper</i>: Typescript based result scraper</li>
            <li><i>result-compiler</i>: Python based result cleaner and compiling pipeline</li>
            <li><i>app</i>: A SvelteKit based frontend</li>
            <li><i>orchestrator</i>: Scripts to coordinate between the different</li>
            <li>
                <i>data</i>: A centralized package to store all the intermediate and processed data
            </li>
        </ol>

        <section>
            <h3>Scraper</h3>
            <p>
                Written in Typescript and runs in the Bun runtime, contains simple but extensible
                scraping functions.
            </p>
            <p>
                Currently I only use the student's name and rollnumber (along with school's common
                info) to scrape the results, but it can be easily extended to consume parent's
                information,<i>if anyone fancies that</i>.
            </p>

            <p>All JSON which goes in and out from here gets validated using valibot schemas.</p>

            <p>
                This package only exports the functions required to do the scraping, but the actual
                scraping and saving part is done within the <i>orchestrator</i> package.
            </p>
        </section>

        <section>
            <h3>Result Compiler</h3>
            <p>
                Core pipeline written in Python and analysis done using Pandas, it is responsible
                for all cleaning and data transformations, and is easily extensible to add new
                analysis parameters.
            </p>

            <p>
                I decided on doing most of computations and analysis once, during build time, using
                the frontend as a mere <i>view layer</i> for the results.
            </p>
            <p>
                All transformation, validation and serialization of data in this step is controlled
                via Pydantic Models.
            </p>

            <p>
                This package again exposes a CLI which is used by the <i>orchestrator</i> package to compile
                the scraped results.
            </p>
        </section>

        <section>
            <h4>App</h4>
            <p>
                A SvelteKit based app which consumes the generated results. Prerenders all routes on
                build time and is hosted on github pages.
            </p>
        </section>

        <section>
            <h4>Orchestrator</h4>
            <p>The final piece which coordinates between all other packages.</p>
        </section>
    </section>

    <section id="disclaimer">
        <h2>The section with Disclaimer</h2>
        <p>
            Yes <b>I am aware</b> that this project exposes student's results, but this project is
            <i>only made for educational and learning purposes</i>. And the fact that <b>I</b> was
            able to extract the results means <b>anyone</b> could easily brute force<span
                class="font-black text-rose-500 text-xl">*</span
            > their way into scraping all the results.
        </p>

        <p>
            <span class="font-black text-xl text-rose-500">*</span>(another thing that I noticed was
            that digilocker's API doesnt seem to have any kind of rate limiting. Although I only ran
            10 requests in parallel at once, but doing more should be possible without any issues.)
        </p>

        <p>
            Also each and every line of this project is <i>handwritten</i>, and LLMs were only used
            in OCR extraction data from photos of student records.
        </p>
    </section>

    <hr />

    <p>
        Thank you for reading till end <span class="text-sm">❤️</span>
    </p>

    {@render BackButton()}
</div>
