FROM postgres:17.11-bookworm

# The official entrypoint runs these files only when the data directory is empty.
COPY --chmod=0644 database/schema.sql /docker-entrypoint-initdb.d/10-schema.sql
COPY --chmod=0644 database/seed_languages.sql /docker-entrypoint-initdb.d/20-seed-languages.sql

HEALTHCHECK --interval=2s --timeout=5s --start-period=20s --retries=15 \
    CMD pg_isready -h 127.0.0.1 -U "$POSTGRES_USER" -d "$POSTGRES_DB" || exit 1
