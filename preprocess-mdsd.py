import re
import random
from pathlib import Path
from tqdm import tqdm
import mdsd


parsed_data  = []
test_percent = 0.1 # percent of reviews to be put in test file instead of train file
train_file   = "fasttext-mdsd-train.txt"
test_file    = "fasttext-mdsd-test.txt"

"""Some of the MDSD files with various sizes for testing

1.4G sorted_data/books/all.review
198M sorted_data/dvd/all.review
7.0M sorted_data/apparel/all.review
315K sorted_data/musical_instruments/all.review
"""
mdsd_files = (
"sorted_data/books.all.review00",
"sorted_data/books.all.review01",
"sorted_data/books.all.review02",
"sorted_data/books.all.review03",
"sorted_data/books.all.review04",
"sorted_data/books.all.review05",
"sorted_data/books.all.review06",
"sorted_data/music/all.review",
"sorted_data/dvd/all.review",
"sorted_data/video/all.review",
"sorted_data/electronics/all.review",
"sorted_data/kitchen_&_housewares/all.review",
"sorted_data/toys_&_games/all.review",
"sorted_data/camera_&_photo/all.review",
"sorted_data/apparel/all.review",
"sorted_data/health_&_personal_care/all.review",
"sorted_data/sports_&_outdoors/all.review",
"sorted_data/magazines/all.review",
"sorted_data/computer_&_video_games/all.review",
"sorted_data/baby/all.review",
"sorted_data/software/all.review",
"sorted_data/beauty/all.review",
"sorted_data/grocery/all.review",
"sorted_data/jewelry_&_watches/all.review",
"sorted_data/outdoor_living/all.review",
"sorted_data/gourmet_food/all.review",
"sorted_data/cell_phones_&_service/all.review",
"sorted_data/automotive/all.review",
"sorted_data/office_products/all.review",
"sorted_data/musical_instruments/all.review",
"sorted_data/tools_&_hardware/all.review" )

for file in mdsd_files:
    filepath = Path("..", file)
    parsed_data.extend(mdsd.parse_file(filepath))


# Format parsed data to FastText format and write training and test files.
tqdm.write("\nFormatting data and writing files. Reviews {}\n".format(len(parsed_data)))
with Path(train_file).open("w", encoding="utf-8") as train_output, \
     Path(test_file).open("w", encoding="utf-8") as test_output:
    for d in tqdm(parsed_data):
        ft = mdsd.format_line(d)
        if random.random() <= test_percent:
            test_output.write(ft +"\n")
        else:
            train_output.write(ft + "\n")

