import csv

def write_csv(filepath, rows, string_fields):
    if not rows:
        print(f"No data to write for {filepath}")
        return

    with open(filepath, 'w', newline='') as f:
        # csv.QUOTE_NONNUMERIC quotes all string fields automatically
        # and leaves numeric fields (int, float) without quotes
        # But it works based on Python type, so our string_fields must actually be strings
        # and numeric fields must actually be int or float, not strings
        writer = csv.DictWriter(f, fieldnames=rows[0].keys(), quoting=csv.QUOTE_NONNUMERIC)
        writer.writeheader()
        writer.writerows(rows)
    
    print(f"Written: {filepath}")