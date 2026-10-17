-- Run on an existing LingoFill database before starting the updated application.
-- Existing accounts receive the previous UI defaults; no account data is removed.
BEGIN;

ALTER TABLE public.account_users
    ADD COLUMN IF NOT EXISTS exercise_level varchar(2) DEFAULT 'A1' NOT NULL
        CONSTRAINT account_users_exercise_level_check CHECK (exercise_level IN ('A1', 'A2', 'B1', 'B2')),
    ADD COLUMN IF NOT EXISTS exercise_sentence_count smallint DEFAULT 10 NOT NULL
        CONSTRAINT account_users_exercise_sentence_count_check CHECK (exercise_sentence_count IN (5, 10, 15, 20, 30)),
    ADD COLUMN IF NOT EXISTS exercise_blank_count varchar(3) DEFAULT '1' NOT NULL
        CONSTRAINT account_users_exercise_blank_count_check CHECK (exercise_blank_count IN ('1', '1-2', '2-3'));

COMMENT ON COLUMN public.account_users.exercise_level IS 'Last selected exercise CEFR level: A1, A2, B1 or B2.';
COMMENT ON COLUMN public.account_users.exercise_sentence_count IS 'Last selected exercise sentence count: 5, 10, 15, 20 or 30.';
COMMENT ON COLUMN public.account_users.exercise_blank_count IS 'Last selected blanks-per-sentence option: 1, 1-2 or 2-3.';

COMMIT;
