from datetime import datetime, timedelta

def convert_time(utc_string):
    # Parse the UTC string into a datetime object
    dt = datetime.strptime(utc_string, "%Y-%m-%d %H:%M:%S UTC")

    # Subtract 3 hours to convert UTC to São Paulo (UTC-3)
    dt_sp = dt - timedelta(hours=3)

    # Return only the date formatted as DD/MM/YYYY
    return dt_sp.strftime("%d/%m/%Y")


def transform(records):
    # Three buckets: One per output csv
    curated_offer_options = []
    dynamic_price_options = []
    dynamic_price_ranges = []

    for record in records:
        event = record['EventName']
        payload = record['Payload']
        enqueued_time_sp = convert_time(record['EnqueuedTimeUtc'])

        # Route each record to the right bucket based on EventName
        if event == 'CuratedOffer_Result':
            # This event has an 'options' list: each item becomes its own row
            # This is the "explode" pattern in ETL: one record to many rows
            for option in payload['options']:
                curated_offer_options.append({
                    'CurationProvider': payload['curationProvider'],
                    'OfferId': payload['offerId'],
                    'DealerId': option['dealerId'],
                    'UniqueOptionId': option['uniqueOptionId'],
                    'OptionId': option['optionId'],
                    'IsMobileDealer': int(option['isMobileDealer']),
                    'IsOpen': int(option['isOpen']),
                    'Eta': option['eta'],
                    'ChamaScore': option['chamaScore'],
                    'ProductBrand': option['productBrand'],
                    'IsWinner': int(option['isWinner']),
                    'MinimumPrice': option['minimumPrice'],
                    'MaximumPrice': option['maximumPrice'],
                    'DynamicPrice': option['dynamicPrice'],
                    'FinalPrice': option['finalPrice'],
                    'DefeatPrimaryReason': option['defeatPrimaryReason'],
                    'DefeatReasons': option['defeatReasons'],
                    'EnqueuedTimeSP': enqueued_time_sp
                })

        elif event == 'DynamicPrice_Option':
            # Flat payload: one record maps directly to one row
            dynamic_price_options.append({
                'Provider': payload['provider'],
                'OfferId': payload['offerId'],
                'UniqueOptionId': payload['uniqueOptionId'],
                'BestPrice': payload['bestPrice'],
                'EnqueuedTimeSP': enqueued_time_sp
            })

        elif event == 'DynamicPrice_Result':
            # Payload has a nested dict (algorithmOutput): we flatten it
            # Flattening means pulling nested keys up to the top level row
            algo = payload['algorithmOutput']
            dynamic_price_ranges.append({
                'Provider': payload['provider'],
                'OfferId': payload['offerId'],
                'MinGlobal': algo['min_global'],
                'MinRecommended': algo['min_recommended'],
                'MaxRecommended': algo['max_recommended'],
                'DifferenceMinRecommendMinTheory': algo['differenceMinRecommendMinTheory'],
                'EnqueuedTimeSP': enqueued_time_sp
            })

    return curated_offer_options, dynamic_price_options, dynamic_price_ranges