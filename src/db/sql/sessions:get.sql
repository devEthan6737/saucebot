SELECT * FROM cooking_sessions WHERE token = ? AND expiresAt > datetime('now');
