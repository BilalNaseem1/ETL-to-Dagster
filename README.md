1. We're going to create an ETL script that extracts a bunch of data from the hackernews api - top 500 haclernews stories
2. Creates a wordcloud
3. puts the wordcloud into a markdown document
4. Saves the markdown document to disk

### Why Orchestration?
1. If we want to iterate different parts of the pipeline, without running it everytime - `cache expensive operations`
2. The pipeline can fail - api response
3. Store somewhere else
4. No Schedule

`pip install dagster dagit`

`dagit -f hn_dagster.py`

### Retry policies
We can introduce retry policies to account for api failure

```python
from dagster import RetryPolicy

@asset(
    retry_policy=RetryPolicy(
        max_retries=5,
        delay=5 # seconds
        )
    )
```

### Scheduling
- The asset should be `x` minutes or less lagged from reality.
- Dagster will run automatically every x minutes.

```python
from dagster import FreshnessPolicy

@asset(
    FreshnessPolicy(
        maximum_lag_minutes=30,

    )
)
```

### cache expensive operations
- We can break the entire pipeline into multiple different assets
```python
@asset
def hackernews_source_data():
    return extract()
``` 

https://dagster.io/blog/declarative-scheduling