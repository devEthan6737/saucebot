CREATE TABLE IF NOT EXISTS inventory (
    inventoryId INTEGER PRIMARY KEY,
    userId INTEGER NOT NULL,
    
    productName TEXT NOT NULL,
    productQuantity REAL NOT NULL,
    productUnit TEXT NOT NULL,
    productExpiresAt TEXT,
    productMinQuantity REAL,

    UNIQUE (userId, productName, productUnit)
);