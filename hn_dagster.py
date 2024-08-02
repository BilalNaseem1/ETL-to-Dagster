# DAGSTER VERSION OF THE ETL SCRIPT

from hackernews import extract, transform, load
from dagster import asset

@asset
def hackernews_wordcloud():
    input = extract()
    output = transform(input)
    load(output)