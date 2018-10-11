import json
from pathlib import Path

review_data = Path("yelp-review-example.json")

with review_data.open() as data:
    for line in data:
        review_json = json.loads(line)
        test = "break"
