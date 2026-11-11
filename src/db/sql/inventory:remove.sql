UPDATE inventory SET productQuantity = productQuantity - ?
    WHERE userId = ? AND productName = ? AND productUnit = ?;
