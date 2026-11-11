INSERT INTO cooking_sessions (token, userId, recipe, expiresAt)
    VALUES (?, ?, ?, datetime('now', ?));
