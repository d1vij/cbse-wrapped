export function generate(
    fathersName: string,
    mothersName: string,
    studentRollNumber: string,
    schoolNumber: string,
    centerNumber: string,
) {
    const F = fathersName.at(-2);
    const M = mothersName.at(-1);
    const RR = studentRollNumber.slice(-2);
    const SS = schoolNumber.slice(0, 2);

    const half = centerNumber.length / 2 - 1;
    const CC = centerNumber.slice(half, half + 2);

    return ((F as string) + (M as string) + RR + SS + CC).toUpperCase();
}
