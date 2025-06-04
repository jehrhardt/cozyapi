use tauri_plugin_sql::{Migration, MigrationKind};

pub(crate) fn migrations() -> Vec<Migration> {
    vec![Migration {
        version: 1,
        description: "create_endpoints_table",
        sql: "create table endpoints (
            id text primary key,
            name text not null unique,
            method text not null,
            path text not null,
            created_at text not null,
            updated_at text not null
        );",
        kind: MigrationKind::Up,
    }]
}
