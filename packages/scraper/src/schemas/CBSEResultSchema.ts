import * as v from "valibot";

/**
 * CBSE 9-point grade scale
 */
export const GradeSchema = v.picklist([
    "A1",
    "A2",
    "B1",
    "B2",
    "C1",
    "C2",
    "D1",
    "D2",
    "E",
]);
export type Grade = v.InferOutput<typeof GradeSchema>;

/**
 * Grade or empty for unused optional subjects
 */
export const GradeOrEmptySchema = v.union([GradeSchema, v.literal("")]);
export type GradeOrEmpty = v.InferOutput<typeof GradeOrEmptySchema>;

/**
 * Subject result flag
 * "P"  = Pass
 * "RT" = Result withheld
 * ""   = Unused subject slot
 */
export const SubjectPassFlagSchema = v.picklist(["P", "RT", ""]);
export type SubjectPassFlag = v.InferOutput<typeof SubjectPassFlagSchema>;

/**
 * Reusable yes/no flag
 */
export const YNFlagSchema = v.picklist(["Y", "N"]);
export type YNFlag = v.InferOutput<typeof YNFlagSchema>;

/**
 * Normalized DigiLocker CBSE result schema
 */
export const CBSEResultSchema = v.object({
    /** Admission ID */
    ADMN_ID: v.string(),

    /** Student name */
    CNAME: v.string(),

    /** Father name */
    FNAME: v.string(),

    /** Mother name */
    MNAME: v.string(),

    /**
     * Student gender
     */
    SEX: v.picklist(["M", "F"]),

    /** Class / standard */
    CLASS: v.string(),

    /** Academic session */
    SESSION: v.pipe(v.string(), v.regex(/^\d{4}-\d{4}$/)),

    /** Exam month */
    MONTH: v.string(),

    /** Supplementary exam month, usually empty */
    MONTH_L: v.string(),

    /** Result declaration date */
    DOD: v.pipe(v.string(), v.regex(/^\d{2}\/\d{2}\/\d{4}$/)),

    /** Exam year */
    YEAR: v.pipe(v.string(), v.regex(/^\d{4}$/)),

    /**
     * Issuing organization
     */
    ORGID: v.literal("CBSE"),

    /** Exam center code */
    CENT: v.string(),

    /** School code */
    SCH: v.string(),

    /** School name */
    SCH_NAME: v.string(),

    /**
     * Student type
     * "X" = Private
     * "E" = Regular
     */
    REG: v.picklist(["X", "E"]),

    /**
     * Whether the result is publicly published
     */
    PUBLISHED: YNFlagSchema,

    /** Record version */
    VERSION: v.string(),

    /** Last updated timestamp */
    MODIFIED_ON: v.pipe(
        v.string(),
        v.transform((v) => (v.endsWith("Z") ? v : `${v}Z`)),
        v.isoTimestamp(),
    ),

    // ── Identifiers ──────────────────────────────────────────────────────────

    /** Roll number */
    RROLL: v.pipe(v.string(), v.regex(/^\d+$/)),

    /** Roll + year composite key */
    RROLL_YEAR: v.pipe(v.string(), v.regex(/^\d+_\d{4}$/)),

    /** DigiLocker document URI */
    URI: v.string(),

    /** Internal storage key */
    SK: v.string(),

    /** Internal GSI partition key */
    GSI_PK: v.string(),

    /** Internal GSI sort key */
    GSI_SK: v.string(),

    /**
     * Main result status
     * "PASS" = Cleared all subjects
     * "COMP" = Compartment
     */
    RES: v.picklist(["PASS", "COMP"]),

    /**
     * Secondary result label
     * Empty for compartment cases
     */
    RESULT: v.picklist(["PASS", ""]),

    /**
     * Compartment subject codes
     */
    COMPTT: v.string(),

    /** Total marks */
    TMRK: v.pipe(v.string(), v.regex(/^\d+$/)),

    /** Category code or empty for General */
    CAT: v.string(),

    /** Registered under NCHMCT stream */
    IS_NCHMCT: YNFlagSchema,

    NCHMCT_1: v.string(),
    NCHMCT_2: v.string(),

    /** Registered under NSE */
    IS_NSE: YNFlagSchema,

    NSE_1: v.string(),
    NSE_2: v.string(),

    /** Has a skill subject */
    IS_SKILL: YNFlagSchema,

    SKILL_1: v.string(),
    SKILL_2: v.string(),

    /**
     * Subject names and codes
     * Empty string means subject not taken
     */
    SNAME1: v.string(),
    SUB1: v.string(),

    SNAME2: v.string(),
    SUB2: v.string(),

    SNAME3: v.string(),
    SUB3: v.string(),

    SNAME4: v.string(),
    SUB4: v.string(),

    SNAME5: v.string(),
    SUB5: v.string(),

    SNAME6: v.string(),
    SUB6: v.string(),

    /**
     * Per-subject pass flags
     */
    PF1: SubjectPassFlagSchema,
    PF2: SubjectPassFlagSchema,
    PF3: SubjectPassFlagSchema,
    PF4: SubjectPassFlagSchema,
    PF5: SubjectPassFlagSchema,
    PF6: SubjectPassFlagSchema,

    /**
     * Per-subject grades
     * Slot 6 may be empty
     */
    GR1: GradeSchema,
    GR2: GradeSchema,
    GR3: GradeSchema,
    GR4: GradeSchema,
    GR5: GradeSchema,
    GR6: GradeOrEmptySchema,

    /**
     * Marks:
     * MRKxy
     * x = subject index (1–6)
     * y = 1 theory, 2 practical, 3 total
     */
    MRK11: v.string(),
    MRK12: v.string(),
    MRK13: v.string(),
    MRK13_WRDS: v.string(),

    MRK21: v.string(),
    MRK22: v.string(),
    MRK23: v.string(),
    MRK23_WRDS: v.string(),

    MRK31: v.string(),
    MRK32: v.string(),
    MRK33: v.string(),
    MRK33_WRDS: v.string(),

    MRK41: v.string(),
    MRK42: v.string(),
    MRK43: v.string(),
    MRK43_WRDS: v.string(),

    MRK51: v.string(),
    MRK52: v.string(),
    MRK53: v.string(),
    MRK53_WRDS: v.string(),

    MRK61: v.string(),
    MRK62: v.string(),
    MRK63: v.string(),
    MRK63_WRDS: v.string(),

    /**
     * Internal/co-scholastic subjects
     */
    ISNAME1: v.string(),
    ISNAME2: v.string(),
    ISNAME3: v.string(),

    ISUB1: v.string(),
    ISUB2: v.string(),
    ISUB3: v.string(),

    /**
     * Internal subject grades
     */
    IGR1: GradeSchema,
    IGR2: GradeSchema,
    IGR3: GradeSchema,
});

export type CBSEResult = v.InferOutput<typeof CBSEResultSchema>;

/**
 * When the response is an error
 */
export const ErrorResponseSchema = v.object({
    status: v.literal(400),
    request_id: v.pipe(v.string(), v.uuid()),
    error_code: v.string(),
    message: v.string(),
});
export type ErrorResponse = v.InferInput<typeof ErrorResponseSchema>;

export const CBSEResultResponseSchema = v.object({
    data: CBSEResultSchema,

    /** API processing time in seconds */
    duration_sec: v.number(),

    /** Request UUID */
    request_id: v.pipe(v.string(), v.uuid()),

    /** HTTP status code */
    status: v.literal(200),
});

/**
 * When the response is successful
 */
export type CBSEResultResponse = v.InferInput<typeof CBSEResultResponseSchema>;

/**
 * Union of failed and succesfull responses.
 */
export const SuccessOrFailedResponseSchema = v.union([
    CBSEResultResponseSchema,
    ErrorResponseSchema,
]);
export type SuccessOrFailedResponse = v.InferOutput<
    typeof SuccessOrFailedResponseSchema
>;
