CREATE TABLE IF NOT EXISTS cooking_sessions (
    token TEXT PRIMARY KEY,
    userId INTEGER NOT NULL,
    recipe TEXT NOT NULL,
    expiresAt TEXT NOT NULL
);
