--
-- PostgreSQL database dump
--

\restrict FcRcX1TvO0LOFeLmlHMDbthwa6XGMlPgaBUxVQyWVlZAZOhmrZnSYQZA7W2r9mu

-- Dumped from database version 17.6
-- Dumped by pg_dump version 17.6

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: set_updated_at(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.set_updated_at() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$;


--
-- Name: FUNCTION set_updated_at(); Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON FUNCTION public.set_updated_at() IS 'Reusable trigger function that refreshes updated_at whenever a row is updated.';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: account_users; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.account_users (
    id bigint NOT NULL,
    email character varying(254) NOT NULL,
    nickname character varying(150) NOT NULL,
    first_name character varying(150) NOT NULL,
    last_name character varying(150) NOT NULL,
    telephone character varying(30),
    preferred_interface_language_id bigint NOT NULL,
    default_learning_language_id bigint,
    password character varying(128) NOT NULL,
    is_active boolean DEFAULT true NOT NULL,
    is_staff boolean DEFAULT false NOT NULL,
    is_superuser boolean DEFAULT false NOT NULL,
    last_login timestamp with time zone,
    last_activity_at timestamp with time zone,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);


--
-- Name: TABLE account_users; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.account_users IS 'Application users and their authentication, profile and language-preference data.';


--
-- Name: COLUMN account_users.id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.account_users.id IS 'Internal numeric identifier for the user.';


--
-- Name: COLUMN account_users.email; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.account_users.email IS 'Unique e-mail address used as the primary Django authentication identifier.';


--
-- Name: COLUMN account_users.nickname; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.account_users.nickname IS 'Unique public or login nickname associated with the user.';


--
-- Name: COLUMN account_users.first_name; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.account_users.first_name IS 'User first name.';


--
-- Name: COLUMN account_users.last_name; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.account_users.last_name IS 'User last name.';


--
-- Name: COLUMN account_users.telephone; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.account_users.telephone IS 'Optional telephone number supplied by the user.';


--
-- Name: COLUMN account_users.preferred_interface_language_id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.account_users.preferred_interface_language_id IS 'Preferred interface language selected by the user; used as the initial/default UI language without restricting access to the other supported interface languages.';


--
-- Name: COLUMN account_users.default_learning_language_id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.account_users.default_learning_language_id IS 'Persistent default exercise language. It is initially NULL and is resolved from the languages selected during registration; users remain free to use any supported learning language afterward.';


--
-- Name: COLUMN account_users.password; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.account_users.password IS 'Django-compatible hashed password value; never stores the plain-text password.';


--
-- Name: COLUMN account_users.is_active; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.account_users.is_active IS 'Indicates whether the account is enabled for authentication.';


--
-- Name: COLUMN account_users.is_staff; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.account_users.is_staff IS 'Indicates whether the user may access Django staff/admin functionality when otherwise authorized.';


--
-- Name: COLUMN account_users.is_superuser; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.account_users.is_superuser IS 'Indicates whether the user has Django superuser privileges.';


--
-- Name: COLUMN account_users.last_login; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.account_users.last_login IS 'Timestamp of the most recent successful Django login.';


--
-- Name: COLUMN account_users.last_activity_at; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.account_users.last_activity_at IS 'Optional timestamp used by the application to track the user''s latest activity.';


--
-- Name: COLUMN account_users.created_at; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.account_users.created_at IS 'Timestamp when the user account was created.';


--
-- Name: COLUMN account_users.updated_at; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.account_users.updated_at IS 'Timestamp when the user account record was last modified.';


--
-- Name: account_users_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.account_users ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.account_users_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.auth_group (
    id integer NOT NULL,
    name character varying(150) NOT NULL
);


--
-- Name: TABLE auth_group; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.auth_group IS 'Django authentication groups used to organize collections of permissions.';


--
-- Name: COLUMN auth_group.id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.auth_group.id IS 'Primary key identifying the authentication group.';


--
-- Name: COLUMN auth_group.name; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.auth_group.name IS 'Unique, human-readable name of the authentication group.';


--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.auth_group ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_group_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.auth_group_permissions (
    id bigint NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


--
-- Name: TABLE auth_group_permissions; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.auth_group_permissions IS 'Django many-to-many association assigning permissions to authentication groups; each group and permission pair is unique.';


--
-- Name: COLUMN auth_group_permissions.id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.auth_group_permissions.id IS 'Primary key identifying the group-permission association.';


--
-- Name: COLUMN auth_group_permissions.group_id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.auth_group_permissions.group_id IS 'Foreign key to the authentication group in auth_group.';


--
-- Name: COLUMN auth_group_permissions.permission_id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.auth_group_permissions.permission_id IS 'Foreign key to the permission assigned to the group in auth_permission.';


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.auth_group_permissions ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_group_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


--
-- Name: TABLE auth_permission; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.auth_permission IS 'Django permission definitions associated with model content types, including default add, change, delete and view permissions and any custom permissions.';


--
-- Name: COLUMN auth_permission.id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.auth_permission.id IS 'Primary key identifying the permission.';


--
-- Name: COLUMN auth_permission.name; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.auth_permission.name IS 'Human-readable description of the permission.';


--
-- Name: COLUMN auth_permission.content_type_id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.auth_permission.content_type_id IS 'Foreign key to the model content type in django_content_type; together with codename, uniquely identifies the permission.';


--
-- Name: COLUMN auth_permission.codename; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.auth_permission.codename IS 'Machine-readable permission code, such as change_exercises; referenced by Django as app_label.codename.';


--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.auth_permission ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_permission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id bigint NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


--
-- Name: TABLE django_admin_log; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.django_admin_log IS 'Django admin history of object additions, changes and deletions performed through the admin interface; this is not a complete application audit log.';


--
-- Name: COLUMN django_admin_log.id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.django_admin_log.id IS 'Primary key identifying the admin log entry.';


--
-- Name: COLUMN django_admin_log.action_time; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.django_admin_log.action_time IS 'Date and time when the admin action was logged.';


--
-- Name: COLUMN django_admin_log.object_id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.django_admin_log.object_id IS 'Primary key of the affected object stored as text; nullable and not a foreign key to that object.';


--
-- Name: COLUMN django_admin_log.object_repr; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.django_admin_log.object_repr IS 'Text representation of the affected object captured when the action was logged, limited to 200 characters.';


--
-- Name: COLUMN django_admin_log.action_flag; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.django_admin_log.action_flag IS 'Django admin action code: 1 for addition, 2 for change and 3 for deletion.';


--
-- Name: COLUMN django_admin_log.change_message; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.django_admin_log.change_message IS 'Description of the admin action, stored as plain text or a JSON-encoded description of changes.';


--
-- Name: COLUMN django_admin_log.content_type_id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.django_admin_log.content_type_id IS 'Nullable foreign key to the affected model content type in django_content_type.';


--
-- Name: COLUMN django_admin_log.user_id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.django_admin_log.user_id IS 'Foreign key to the LingoFill account in account_users that performed the admin action.';


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.django_admin_log ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_admin_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


--
-- Name: TABLE django_content_type; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.django_content_type IS 'Django registry identifying installed models by application label and model name; used by permissions and generic relationships.';


--
-- Name: COLUMN django_content_type.id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.django_content_type.id IS 'Primary key identifying the model content type.';


--
-- Name: COLUMN django_content_type.app_label; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.django_content_type.app_label IS 'Django application label owning the model; together with model, uniquely identifies the content type.';


--
-- Name: COLUMN django_content_type.model; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.django_content_type.model IS 'Lowercase Django model name; this is not necessarily the database table name.';


--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.django_content_type ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_content_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.django_migrations (
    id bigint NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


--
-- Name: TABLE django_migrations; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.django_migrations IS 'Django migration recorder tracking migrations marked as applied; records do not contain migration SQL or independently prove the current database structure.';


--
-- Name: COLUMN django_migrations.id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.django_migrations.id IS 'Primary key identifying the migration record.';


--
-- Name: COLUMN django_migrations.app; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.django_migrations.app IS 'Django application label to which the recorded migration belongs.';


--
-- Name: COLUMN django_migrations.name; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.django_migrations.name IS 'Migration name without the Python file extension, such as 0001_initial.';


--
-- Name: COLUMN django_migrations.applied; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.django_migrations.applied IS 'Date and time when Django recorded the migration as applied.';


--
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.django_migrations ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_migrations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


--
-- Name: TABLE django_session; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.django_session IS 'Server-side session storage for Django database-backed sessions, including authentication session state; expired records require periodic cleanup.';


--
-- Name: COLUMN django_session.session_key; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.django_session.session_key IS 'Primary key identifying the server-side session, normally referenced by the browser session cookie.';


--
-- Name: COLUMN django_session.session_data; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.django_session.session_data IS 'Encoded and signed serialized session data; signing protects integrity but does not provide encryption.';


--
-- Name: COLUMN django_session.expire_date; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.django_session.expire_date IS 'Date and time after which the session is no longer valid; expiry does not automatically delete the row.';


--
-- Name: exercise_items; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.exercise_items (
    id bigint NOT NULL,
    exercise_id bigint NOT NULL,
    "position" integer NOT NULL,
    sentence_template text NOT NULL,
    correct_answers jsonb NOT NULL,
    submitted_answers jsonb,
    explanation text,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT chk_exercise_items_position CHECK (("position" > 0))
);


--
-- Name: TABLE exercise_items; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.exercise_items IS 'Stores the individual sentences or questions belonging to an exercise, including accepted answers, submitted answers, and optional AI-generated explanations for incorrect answers.';


--
-- Name: COLUMN exercise_items.id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.exercise_items.id IS 'Primary key that uniquely identifies an individual exercise item.';


--
-- Name: COLUMN exercise_items.exercise_id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.exercise_items.exercise_id IS 'References the parent exercise to which this item belongs.';


--
-- Name: COLUMN exercise_items."position"; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.exercise_items."position" IS 'One-based position of the item within its parent exercise. The value must be greater than zero and unique within each exercise.';


--
-- Name: COLUMN exercise_items.sentence_template; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.exercise_items.sentence_template IS 'Sentence or exercise text presented to the user, including placeholders or blanks that must be completed.';


--
-- Name: COLUMN exercise_items.correct_answers; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.exercise_items.correct_answers IS 'JSONB document containing the accepted correct answer or answers for this exercise item.';


--
-- Name: COLUMN exercise_items.submitted_answers; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.exercise_items.submitted_answers IS 'JSONB document containing the answer or answers submitted by the user. NULL until an answer has been submitted.';


--
-- Name: COLUMN exercise_items.explanation; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.exercise_items.explanation IS 'Optional AI-generated explanation describing why the submitted answer was incorrect. NULL after submission indicates that the answer was correct.';


--
-- Name: COLUMN exercise_items.created_at; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.exercise_items.created_at IS 'Timestamp indicating when the exercise item record was created.';


--
-- Name: COLUMN exercise_items.updated_at; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.exercise_items.updated_at IS 'Timestamp of the most recent modification. Automatically maintained by the set_updated_at trigger function.';


--
-- Name: CONSTRAINT chk_exercise_items_position ON exercise_items; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON CONSTRAINT chk_exercise_items_position ON public.exercise_items IS 'Ensures that exercise item positions begin at 1 and cannot contain zero or negative values.';


--
-- Name: exercise_items_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.exercise_items_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: exercise_items_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.exercise_items_id_seq OWNED BY public.exercise_items.id;


--
-- Name: SEQUENCE exercise_items_id_seq; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON SEQUENCE public.exercise_items_id_seq IS 'Sequence automatically used to generate primary-key values for exercise_items.id.';


--
-- Name: exercises; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.exercises (
    id bigint NOT NULL,
    user_id bigint NOT NULL,
    learning_language_id bigint NOT NULL,
    source character varying(20) NOT NULL,
    title character varying(255),
    generation_settings jsonb,
    ai_prompt text,
    advanced_options jsonb,
    started_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    completed_at timestamp with time zone,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT chk_exercises_source CHECK (((source)::text = ANY ((ARRAY['manual'::character varying, 'ai'::character varying])::text[])))
);


--
-- Name: TABLE exercises; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.exercises IS 'Stores exercises created by registered users, including manually created exercises and AI-generated exercises.';


--
-- Name: COLUMN exercises.id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.exercises.id IS 'Primary key that uniquely identifies an exercise.';


--
-- Name: COLUMN exercises.user_id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.exercises.user_id IS 'References the account_users record of the user who owns and completes the exercise.';


--
-- Name: COLUMN exercises.learning_language_id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.exercises.learning_language_id IS 'References the language being practiced in this exercise.';


--
-- Name: COLUMN exercises.source; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.exercises.source IS 'Identifies how the exercise was created. Supported values are manual and ai.';


--
-- Name: COLUMN exercises.title; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.exercises.title IS 'Optional human-readable title assigned to the exercise.';


--
-- Name: COLUMN exercises.generation_settings; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.exercises.generation_settings IS 'Optional JSONB document containing general settings or metadata used during AI exercise generation. Normally NULL for manually created exercises.';


--
-- Name: COLUMN exercises.ai_prompt; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.exercises.ai_prompt IS 'Optional text containing the user-defined AI goal entered through the ai_goal textarea when generating an exercise.';


--
-- Name: COLUMN exercises.advanced_options; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.exercises.advanced_options IS 'Optional JSON document containing user-defined advanced AI generation options, such as verbs, subjects, tenses, topics, expressions, and other configurable generation parameters.';


--
-- Name: COLUMN exercises.started_at; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.exercises.started_at IS 'Timestamp indicating when the user started working on the exercise.';


--
-- Name: COLUMN exercises.completed_at; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.exercises.completed_at IS 'Timestamp indicating when the exercise was completed. NULL while the exercise has not yet been completed.';


--
-- Name: COLUMN exercises.created_at; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.exercises.created_at IS 'Timestamp indicating when the exercise record was created.';


--
-- Name: COLUMN exercises.updated_at; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.exercises.updated_at IS 'Timestamp of the most recent modification. Automatically maintained by the set_updated_at trigger function.';


--
-- Name: CONSTRAINT chk_exercises_source ON exercises; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON CONSTRAINT chk_exercises_source ON public.exercises IS 'Ensures that exercise source contains only one of the supported values: manual or ai.';


--
-- Name: exercises_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.exercises_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: exercises_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.exercises_id_seq OWNED BY public.exercises.id;


--
-- Name: SEQUENCE exercises_id_seq; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON SEQUENCE public.exercises_id_seq IS 'Sequence automatically used to generate primary-key values for exercises.id.';


--
-- Name: languages; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.languages (
    id bigint NOT NULL,
    code character varying(10) NOT NULL,
    name character varying(100) NOT NULL,
    original_name character varying(100) NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);


--
-- Name: TABLE languages; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.languages IS 'Catalog of the eight languages currently supported by LingoFill for both the interface and language-learning exercises.';


--
-- Name: COLUMN languages.id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.languages.id IS 'Internal numeric identifier for the language.';


--
-- Name: COLUMN languages.code; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.languages.code IS 'Short application language code, such as en, es, de, ja, hi, ro, it or pt.';


--
-- Name: COLUMN languages.name; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.languages.name IS 'Language name in English, used as a stable descriptive value.';


--
-- Name: COLUMN languages.original_name; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.languages.original_name IS 'Language name written in the language itself, used in user-facing selectors.';


--
-- Name: COLUMN languages.created_at; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.languages.created_at IS 'Timestamp when the language record was created.';


--
-- Name: COLUMN languages.updated_at; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.languages.updated_at IS 'Timestamp when the language record was last modified.';


--
-- Name: languages_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.languages ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.languages_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: users_learning_languages; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.users_learning_languages (
    id bigint NOT NULL,
    user_id bigint NOT NULL,
    language_id bigint NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);


--
-- Name: TABLE users_learning_languages; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.users_learning_languages IS 'Languages a user selected as learning interests during registration. These values provide profile/default information and do not restrict the languages available in exercises.';


--
-- Name: COLUMN users_learning_languages.id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.users_learning_languages.id IS 'Internal numeric identifier for the user-language association.';


--
-- Name: COLUMN users_learning_languages.user_id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.users_learning_languages.user_id IS 'User who selected the learning language.';


--
-- Name: COLUMN users_learning_languages.language_id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.users_learning_languages.language_id IS 'Language selected by the user as a language they are learning.';


--
-- Name: COLUMN users_learning_languages.created_at; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.users_learning_languages.created_at IS 'Timestamp when the user-language association was created.';


--
-- Name: COLUMN users_learning_languages.updated_at; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.users_learning_languages.updated_at IS 'Timestamp when the user-language association was last modified.';


--
-- Name: users_learning_languages_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.users_learning_languages ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.users_learning_languages_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: exercise_items id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.exercise_items ALTER COLUMN id SET DEFAULT nextval('public.exercise_items_id_seq'::regclass);


--
-- Name: exercises id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.exercises ALTER COLUMN id SET DEFAULT nextval('public.exercises_id_seq'::regclass);


--
-- Name: account_users account_users_email_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.account_users
    ADD CONSTRAINT account_users_email_key UNIQUE (email);


--
-- Name: account_users account_users_nickname_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.account_users
    ADD CONSTRAINT account_users_nickname_key UNIQUE (nickname);


--
-- Name: account_users account_users_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.account_users
    ADD CONSTRAINT account_users_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions auth_group_permissions_group_id_permission_id_0cd325b0_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_permission auth_permission_content_type_id_codename_01ab375a_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq UNIQUE (content_type_id, codename);


--
-- Name: auth_permission auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: django_admin_log django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_content_type django_content_type_app_label_model_76bd3d3b_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model);


--
-- Name: django_content_type django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_migrations django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- Name: django_session django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: exercise_items exercise_items_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.exercise_items
    ADD CONSTRAINT exercise_items_pkey PRIMARY KEY (id);


--
-- Name: CONSTRAINT exercise_items_pkey ON exercise_items; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON CONSTRAINT exercise_items_pkey ON public.exercise_items IS 'Primary key constraint that guarantees a unique identifier for every exercise item.';


--
-- Name: exercises exercises_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.exercises
    ADD CONSTRAINT exercises_pkey PRIMARY KEY (id);


--
-- Name: CONSTRAINT exercises_pkey ON exercises; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON CONSTRAINT exercises_pkey ON public.exercises IS 'Primary key constraint that guarantees a unique identifier for every exercise.';


--
-- Name: languages languages_code_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.languages
    ADD CONSTRAINT languages_code_key UNIQUE (code);


--
-- Name: languages languages_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.languages
    ADD CONSTRAINT languages_name_key UNIQUE (name);


--
-- Name: languages languages_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.languages
    ADD CONSTRAINT languages_pkey PRIMARY KEY (id);


--
-- Name: exercise_items uq_exercise_item_position; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.exercise_items
    ADD CONSTRAINT uq_exercise_item_position UNIQUE (exercise_id, "position");


--
-- Name: CONSTRAINT uq_exercise_item_position ON exercise_items; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON CONSTRAINT uq_exercise_item_position ON public.exercise_items IS 'Ensures that the same position number cannot occur more than once within a single exercise.';


--
-- Name: users_learning_languages uq_users_learning_languages; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users_learning_languages
    ADD CONSTRAINT uq_users_learning_languages UNIQUE (user_id, language_id);


--
-- Name: users_learning_languages users_learning_languages_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users_learning_languages
    ADD CONSTRAINT users_learning_languages_pkey PRIMARY KEY (id);


--
-- Name: auth_group_name_a6ea08ec_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_group_name_a6ea08ec_like ON public.auth_group USING btree (name varchar_pattern_ops);


--
-- Name: auth_group_permissions_group_id_b120cbf9; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_group_permissions_group_id_b120cbf9 ON public.auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_permission_id_84c5c92e; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_group_permissions_permission_id_84c5c92e ON public.auth_group_permissions USING btree (permission_id);


--
-- Name: auth_permission_content_type_id_2f476e4b; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_permission_content_type_id_2f476e4b ON public.auth_permission USING btree (content_type_id);


--
-- Name: django_admin_log_content_type_id_c4bce8eb; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX django_admin_log_content_type_id_c4bce8eb ON public.django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_user_id_c564eba6; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX django_admin_log_user_id_c564eba6 ON public.django_admin_log USING btree (user_id);


--
-- Name: django_session_expire_date_a5c62663; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX django_session_expire_date_a5c62663 ON public.django_session USING btree (expire_date);


--
-- Name: django_session_session_key_c0390e0f_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX django_session_session_key_c0390e0f_like ON public.django_session USING btree (session_key varchar_pattern_ops);


--
-- Name: INDEX exercise_items_pkey; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON INDEX public.exercise_items_pkey IS 'Unique B-tree index automatically created by PostgreSQL to support the primary key of exercise_items.';


--
-- Name: INDEX exercises_pkey; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON INDEX public.exercises_pkey IS 'Unique B-tree index automatically created by PostgreSQL to support the primary key of exercises.';


--
-- Name: idx_account_users_default_learning_language_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_account_users_default_learning_language_id ON public.account_users USING btree (default_learning_language_id);


--
-- Name: INDEX idx_account_users_default_learning_language_id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON INDEX public.idx_account_users_default_learning_language_id IS 'Speeds up lookups and joins by the user''s persistent default learning language.';


--
-- Name: idx_account_users_preferred_interface_language_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_account_users_preferred_interface_language_id ON public.account_users USING btree (preferred_interface_language_id);


--
-- Name: INDEX idx_account_users_preferred_interface_language_id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON INDEX public.idx_account_users_preferred_interface_language_id IS 'Speeds up lookups and joins by preferred interface language.';


--
-- Name: idx_exercises_created_at; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_exercises_created_at ON public.exercises USING btree (created_at);


--
-- Name: INDEX idx_exercises_created_at; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON INDEX public.idx_exercises_created_at IS 'Improves chronological exercise-history queries and ordering by creation date.';


--
-- Name: idx_exercises_learning_language_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_exercises_learning_language_id ON public.exercises USING btree (learning_language_id);


--
-- Name: INDEX idx_exercises_learning_language_id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON INDEX public.idx_exercises_learning_language_id IS 'Improves queries that retrieve or filter exercises by learning language.';


--
-- Name: idx_exercises_source; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_exercises_source ON public.exercises USING btree (source);


--
-- Name: INDEX idx_exercises_source; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON INDEX public.idx_exercises_source IS 'Improves queries that filter exercises according to whether they were created manually or with AI.';


--
-- Name: idx_exercises_user_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_exercises_user_id ON public.exercises USING btree (user_id);


--
-- Name: INDEX idx_exercises_user_id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON INDEX public.idx_exercises_user_id IS 'Improves queries that retrieve exercises belonging to a specific user.';


--
-- Name: idx_users_learning_languages_language_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_users_learning_languages_language_id ON public.users_learning_languages USING btree (language_id);


--
-- Name: INDEX idx_users_learning_languages_language_id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON INDEX public.idx_users_learning_languages_language_id IS 'Speeds up retrieval of users associated with a learning language.';


--
-- Name: idx_users_learning_languages_user_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_users_learning_languages_user_id ON public.users_learning_languages USING btree (user_id);


--
-- Name: INDEX idx_users_learning_languages_user_id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON INDEX public.idx_users_learning_languages_user_id IS 'Speeds up retrieval of all learning languages selected by a user.';


--
-- Name: INDEX uq_exercise_item_position; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON INDEX public.uq_exercise_item_position IS 'Unique B-tree index automatically created for the unique combination of exercise_id and position. It also supports efficient ordered retrieval of items belonging to an exercise.';


--
-- Name: account_users trg_account_users_updated_at; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_account_users_updated_at BEFORE UPDATE ON public.account_users FOR EACH ROW EXECUTE FUNCTION public.set_updated_at();


--
-- Name: TRIGGER trg_account_users_updated_at ON account_users; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TRIGGER trg_account_users_updated_at ON public.account_users IS 'Automatically refreshes account_users.updated_at before each update.';


--
-- Name: exercise_items trg_exercise_items_set_updated_at; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_exercise_items_set_updated_at BEFORE UPDATE ON public.exercise_items FOR EACH ROW EXECUTE FUNCTION public.set_updated_at();


--
-- Name: TRIGGER trg_exercise_items_set_updated_at ON exercise_items; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TRIGGER trg_exercise_items_set_updated_at ON public.exercise_items IS 'Automatically updates exercise_items.updated_at whenever an exercise item record is modified.';


--
-- Name: exercises trg_exercises_set_updated_at; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_exercises_set_updated_at BEFORE UPDATE ON public.exercises FOR EACH ROW EXECUTE FUNCTION public.set_updated_at();


--
-- Name: TRIGGER trg_exercises_set_updated_at ON exercises; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TRIGGER trg_exercises_set_updated_at ON public.exercises IS 'Automatically updates exercises.updated_at whenever an exercises record is modified.';


--
-- Name: languages trg_languages_updated_at; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_languages_updated_at BEFORE UPDATE ON public.languages FOR EACH ROW EXECUTE FUNCTION public.set_updated_at();


--
-- Name: TRIGGER trg_languages_updated_at ON languages; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TRIGGER trg_languages_updated_at ON public.languages IS 'Automatically refreshes languages.updated_at before each update.';


--
-- Name: users_learning_languages trg_users_learning_languages_updated_at; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_users_learning_languages_updated_at BEFORE UPDATE ON public.users_learning_languages FOR EACH ROW EXECUTE FUNCTION public.set_updated_at();


--
-- Name: TRIGGER trg_users_learning_languages_updated_at ON users_learning_languages; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TRIGGER trg_users_learning_languages_updated_at ON public.users_learning_languages IS 'Automatically refreshes users_learning_languages.updated_at before each update.';


--
-- Name: auth_group_permissions auth_group_permissio_permission_id_84c5c92e_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissions_group_id_b120cbf9_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_permission auth_permission_content_type_id_2f476e4b_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_content_type_id_c4bce8eb_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: account_users fk_account_users_default_learning_language_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.account_users
    ADD CONSTRAINT fk_account_users_default_learning_language_id FOREIGN KEY (default_learning_language_id) REFERENCES public.languages(id) ON DELETE SET NULL;


--
-- Name: account_users fk_account_users_preferred_interface_language_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.account_users
    ADD CONSTRAINT fk_account_users_preferred_interface_language_id FOREIGN KEY (preferred_interface_language_id) REFERENCES public.languages(id) ON DELETE RESTRICT;


--
-- Name: exercise_items fk_exercise_items_exercise; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.exercise_items
    ADD CONSTRAINT fk_exercise_items_exercise FOREIGN KEY (exercise_id) REFERENCES public.exercises(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: CONSTRAINT fk_exercise_items_exercise ON exercise_items; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON CONSTRAINT fk_exercise_items_exercise ON public.exercise_items IS 'Foreign key linking an exercise item to its parent exercise. Exercise ID changes cascade and deleting the parent exercise deletes all associated items.';


--
-- Name: exercises fk_exercises_learning_language; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.exercises
    ADD CONSTRAINT fk_exercises_learning_language FOREIGN KEY (learning_language_id) REFERENCES public.languages(id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: CONSTRAINT fk_exercises_learning_language ON exercises; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON CONSTRAINT fk_exercises_learning_language ON public.exercises IS 'Foreign key linking an exercise to its learning language. Language ID changes cascade while deletion is restricted when the language is referenced.';


--
-- Name: exercises fk_exercises_user; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.exercises
    ADD CONSTRAINT fk_exercises_user FOREIGN KEY (user_id) REFERENCES public.account_users(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: CONSTRAINT fk_exercises_user ON exercises; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON CONSTRAINT fk_exercises_user ON public.exercises IS 'Foreign key linking an exercise to its owner in account_users. User ID changes cascade and deletion of the user deletes their exercises.';


--
-- Name: users_learning_languages fk_users_learning_languages_language; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users_learning_languages
    ADD CONSTRAINT fk_users_learning_languages_language FOREIGN KEY (language_id) REFERENCES public.languages(id) ON DELETE CASCADE;


--
-- Name: users_learning_languages fk_users_learning_languages_user; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users_learning_languages
    ADD CONSTRAINT fk_users_learning_languages_user FOREIGN KEY (user_id) REFERENCES public.account_users(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

\unrestrict FcRcX1TvO0LOFeLmlHMDbthwa6XGMlPgaBUxVQyWVlZAZOhmrZnSYQZA7W2r9mu

