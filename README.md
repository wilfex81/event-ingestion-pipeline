# Event Ingestion Pipeline

Flatten event payloads into analytics-ready tables via ETL pipelines.

## Task

Some event data comes as JSON and needs transformation into structured tables. Convert `case.json` into 3 CSV files using the programming language of your choice.

## Output files and rules

### `CuratedOfferOptions.csv`

- `CurationProvider`: in quotes
- `OfferId`: in quotes
- `DealerId`: in quotes
- `UniqueOptionId`: in quotes
- `OptionId`: in quotes
- `IsMobileDealer`: without quotes
- `IsOpen`: without quotes
- `Eta`: in quotes
- `ChamaScore`: without quotes
- `ProductBrand`: in quotes
- `IsWinner`: without quotes
- `MinimumPrice`: without quotes
- `MaximumPrice`: without quotes
- `DynamicPrice`: without quotes
- `FinalPrice`: without quotes
- `DefeatPrimaryReason`: in quotes
- `DefeatReasons`: in quotes
- `EnqueuedTimeSP`: `DD/MM/YYYY` (converted to Brazilian timezone - UTC-3)

### `DynamicPriceOption.csv`

- `Provider`: in quotes
- `OfferId`: in quotes
- `UniqueOptionId`: in quotes
- `BestPrice`: without quotes
- `EnqueuedTimeSP`: `DD/MM/YYYY` (converted to Brazilian timezone - UTC-3)

### `DynamicPriceRange.csv`

- `Provider`: in quotes
- `OfferId`: in quotes
- `MinGlobal`: without quotes
- `MinRecommended`: without quotes
- `MaxRecommended`: without quotes
- `DifferenceMinRecommendMinTheory`: without quotes
- `EnqueuedTimeSP`: `DD/MM/YYYY` (converted to Brazilian timezone - UTC-3)

## Data description

You are given one file, `case.json`. Below is an example of a single record from this file:

```json
{
  "EnqueuedTimeUtc": "2021-09-05 08:04:08 UTC",
  "EventName": "DynamicPrice_Result",
  "Payload": "{\"provider\":\"ApplyDynamicPriceRange\",\"offerId\":\"a6611d55-9624-4381-8cdd-323ee3689241\",\"algorithmOutput\":{\"min_global\":85.0,\"min_recommended\":87.2,\"max_recommended\":97.65,\"differenceMinRecommendMinTheory\":2.2}}"
}
```

## Processing Steps

The pipeline operates in three stages:

### Extraction

The input is a JSON file where each record represents an app event. The tricky part is that the `Payload` field — which contains the actual event data — arrives as a JSON-encoded string inside the outer JSON, so it needs to be parsed twice. We handle this by running `json.loads()` on the Payload field of each record after loading the file.

### Transformation

Three things happen in the transformation step:

1. **Routing**: Each record is routed to the right output table based on the `EventName` field.

2. **Flattening nested structures**: For example, the `CuratedOffer_Result` event contains a list of options where each option needs to become its own row, and the `DynamicPrice_Result` event has a nested `algorithmOutput` object that needs to be brought up to the top level.

3. **Data type handling**: We handle two data type issues:
   - **Timezone conversion**: Converting from UTC to UTC-3 for São Paulo, where a naive conversion would give the wrong date for early morning events.
   - **Boolean conversion**: Python booleans are converted to integers so they are compatible with SQL and pandas and satisfy the no-quotes requirement in the output.

### Loading

Three CSV files are written using `csv.QUOTE_NONNUMERIC`, which automatically quotes string fields and leaves numeric fields unquoted — matching the output specification without any manual field-by-field logic.

## Practicalities

Make sure the solution reflects the transformation logic clearly; structure matters more than the final CSV files.