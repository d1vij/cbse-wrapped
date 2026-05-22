import { error } from "@sveltejs/kit";
import { select, sort } from "radashi";
import * as v from "valibot";
import { getStudentsWithStream } from "$lib/utils/getStudentsWithStream.js";
export async function load({ params, parent }) {
    const { results } = await parent();
    const result = v.safeParse(
        v.object({
            id: v.picklist(Object.keys(results.streams) as (keyof typeof results.streams)[]),
        }),
        params,
    );

    if (!result.success) {
        error(404, `No stream found with id ${params.id}`);
    }

    results.subjects_available;
    const stream = results.streams[result.output.id];

    const subjects = stream.subjects.map((subId) => ({
        subId: subId,
        subName: results.subjects_available[subId],
    }));
    const _streamStudents = getStudentsWithStream(stream.stream_id, results.students);

    const studentsRanked = sort(
        select(
            results.students,
            (s) => s,
            (s) => s.stream_id === stream.stream_id,
        ),

        // rank_same_stream would correspond to the rank in "THIS" stream
        (s) => s.rank_same_stream,
    );

    return {
        stream,
        subjects,
        students_ranked: studentsRanked,
    };
}
