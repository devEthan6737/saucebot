DELETE FROM inventory WHERE userId = ? AND productQuantity <= 0 AND productMinQuantity IS NULL;
