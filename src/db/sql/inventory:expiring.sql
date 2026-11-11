SELECT * FROM inventory
    WHERE userId = ?
        AND productExpiresAt IS NOT NULL
        AND productExpiresAt <= date('now', ?)
    ORDER BY productExpiresAt, productName;
