## Database Design Decisions

### Why 3 tables instead of 1
- log_entries: raw data, append-only, never updated
- processed_files: operational metadata, one row per file run
- hourly_summaries: pre-aggregated for fast trend queries

### Why timestamp_hour is pre-computed
Avoids substr() on 100k rows at query time.
Trades a small amount of storage for significant query speed.

### Why a summary table instead of GROUP BY every time
At 100k rows, a GROUP BY hour scan takes ~200ms.
Reading 24 rows from hourly_summaries takes ~1ms.
This pattern is called a materialized view — standard in
production analytics (used by Datadog, Mixpanel, etc).

### Indexes chosen
Composite index on (level, timestamp) because our most
frequent query always filters by both together.
Single index on timestamp_hour for GROUP BY performance.

### What I'd change at scale
- Switch SQLite → PostgreSQL for concurrent writes
- Replace hourly_summaries with a real materialized view
- Add partitioning on timestamp for multi-year datasets