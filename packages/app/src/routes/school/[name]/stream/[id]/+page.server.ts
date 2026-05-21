import { error } from "@sveltejs/kit";
import { select, sort } from "radashi";
import * as v from "valibot";
import { getStudentsWithStream } from "$lib/utils/getStudentsWithStream.js";
export async function load({ params, parent }) {
    const { results } = await parent();
    const result = v.safeParse(
        v.object({
            id: v.picklist(
                Object.keys(
                    results.streams,
                ) as (keyof typeof results.streams)[],
            ),
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
    const _streamStudents = getStudentsWithStream(
        stream.stream_id,
        results.students,
    );

    const studentsRanked = sort(
        select(
            results.students,
            (s) => ({
                name_candidate: s.name_candidate,
                roll_number: s.roll_number,
                // rank_same_stream would correspond to the rank in "THIS" stream
                rank: s.rank_same_stream,
            }),
            (s) => s.stream_id === stream.stream_id,
        ),
        (s) => s.rank,
    );

    return {
        stream,
        subjects,
        students_ranked: studentsRanked,
    };
}
