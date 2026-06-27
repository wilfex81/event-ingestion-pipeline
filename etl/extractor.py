import json

# Load the outer JSON file - Get a list of records
# Parse the payload field in each record: Converts it from a string to an actual dict

def extract_payload(filepath):
    with open(filepath, 'r') as f:
        data = json.load(f)

    # Iterate over each record and parse the payload field
    # Since the payload is a JSON string, we need to convert it to a Python dictionary using json.loads()
    # Mutate the record in place keeping the rest of the record intact
    for record in data:
        record['Payload'] = json.loads(record['Payload'])

    return data
    

