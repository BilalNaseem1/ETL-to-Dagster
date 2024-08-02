1. We're going to create an ETL script that extracts a bunch of data from the hackernews api - top 500 haclernews stories
2. Creates a wordcloud
3. puts the wordcloud into a markdown document
4. Saves the markdown document to disk

### Why Orchestration?
1. If we want to iterate different parts of the pipeline, without running it everytime - `cache expensive operations`
2. The pipeline can fail - api response
3. Store somewhere else
4. No Schedule

`pip install matplotlib pandas requests wordcloud tqdm`
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
- Dagster has `Declaritive Scheduling` i.e. specify what tasks need to be done rather than how to do them. 
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

- we can iterate over less expensive operations as many times, and expensive ones can run as per schedule

### Loading - IO Manager
- It can be useful to test different storage environments
- IO manager abstracts away all of the storage logic in our code
- IO manager saves assets to disk, and then load them from disk

```python
from dagster import IOManager

class HackerNewsIOManager(IOManager):
    def load_input(self, context, length):
        raise NotImplementedError()

    def handle_output(self, context, md_content):
        load(md_content)
```

*write about IOManager