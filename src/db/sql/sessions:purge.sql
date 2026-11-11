DELETE FROM cooking_sessions WHERE expiresAt <= datetime('now');
