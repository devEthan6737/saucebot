INSERT INTO inventory (
    userId, productName, productQuantity, productUnit, productExpiresAt
) VALUES (?, ?, ?, ?, ?)
ON CONFLICT (userId, productName, productUnit) DO UPDATE SET
    productQuantity = productQuantity + excluded.productQuantity,
    productExpiresAt = COALESCE(excluded.productExpiresAt, productExpiresAt);
