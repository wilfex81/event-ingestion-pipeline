from etl.extractor import extract_payload
from etl.transformer import transform
from etl.loader import write_csv

def main():
    # Step 1: Extract: load JSON and parse all Payload strings into dicts
    records = extract_payload('data/case.json')

    # Step 2: Transform: route records and flatten into CSV-ready row dicts
    curated, options, ranges = transform(records)

    # Step 3: Load: write each bucket to its CSV file
    write_csv('output/CuratedOfferOptions.csv', curated, [])
    write_csv('output/DynamicPriceOption.csv', options, [])
    write_csv('output/DynamicPriceRange.csv', ranges, [])

if __name__ == '__main__':
    main()