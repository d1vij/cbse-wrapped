import type { StreamId, Student } from "$lib/schemas";

export function getStudentsWithStream(
    streamId: StreamId,
    students: Student[],
): Student[] {
    return students.filter((s) => s.stream_id === streamId);
}
