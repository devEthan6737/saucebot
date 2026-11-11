SELECT * FROM inventory
    WHERE userId = ?
        AND productMinQuantity IS NOT NULL
        AND productQuantity <= productMinQuantity
    ORDER BY productName;
