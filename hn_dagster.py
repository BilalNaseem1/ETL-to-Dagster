# DAGSTER VERSION OF THE ETL SCRIPT

from hackernews import extract, transform, load
from dagster import asset, RetryPolicy, FreshnessPolicy, IOManager

class HackerNewsIOManager(IOManager):
    def load_input(self, context, length):
        raise NotImplementedError()

    def handle_output(self, context, md_content):
        load(md_content)


@asset
def hackernews_data():
    return extract()

@asset(
    retry_policy=RetryPolicy(max_retries=5, delay=5),
    freshness_policy=FreshnessPolicy(maximum_lag_minutes=30)
)
def hackernews_wordcloud(hackernews_data):
    # raise RuntimeError("fake failure")
    # input = extract()
    output = transform(hackernews_data)
    # load(output)


