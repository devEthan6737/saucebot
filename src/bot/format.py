from datetime import date

# one inventory row as a line of text
def item_line (row):
    line = f"- {row['productName']}: {row['productQuantity']:g} {row['productUnit']}"
    expires = row["productExpiresAt"]

    if expires is None:
        return line
    if expires < date.today().isoformat():
        return f"{line} (caducado el {expires})"
    return f"{line} (caduca el {expires})"
