import re
from pathlib import Path
import random
import tqdm

def parse(review_str):
    m = re.search(r"<rating>\s*(\d)\.\d\s*</rating>", review_str)
    if m:
        rating = m.groups(0)[0]
        
    m = re.search(r"<review_text>\s*(.*)\s*</review_text>", review_str, re.DOTALL)
    if m:
        text = m.groups(0)[0]
        
    return { 'rating': rating, 'text': text}

def pretty(line):
    # pretty print the file out
    global ilevel
    indent_str = "    "
    
    if re.match(r"\s*<\w+>", line) :
        print(indent_str * ilevel + line.strip())
        ilevel += 1
        
    elif re.match(r"\s*</\w+>", line) :
        ilevel -= 1
        print(indent_str * ilevel + line.strip())
        
    else:
        # found text,not a tag
        print(indent_str * ilevel + line.strip())


parsed_data = []
mdsd_file = Path("../sorted_data/books/all.review")
mdsd_file = Path("../sorted_data/software/all.review")

with mdsd_file.open() as data:

    ilevel     = 0
    review_str = ""

    for line in tqdm.tqdm(data):

        # put all lines from the same review into a string 
        if re.match(r"\s*<review>\s*", line):
            review_str = line
        elif re.match(r"\s*</review>\s*", line):
            review_str += line
            # full review text in str, parse data
            parsed_data.append(parse(review_str))
        else:
            review_str += line
                
        #pretty(line)


test_percent = 0.1

with Path("fasttext-mdsd-train.txt").open("w") as train_output, \
     Path("fasttext-mdsd-test.txt").open("w") as test_output:
    # convert to the format fasttext needs
    for d in tqdm.tqdm(parsed_data):
        # FastText expects the review text to be all one line, lowercase with puntuation seperated
        text = d.get("text").replace("\n", "").lower()
        text = re.sub(r"([.!?,/()])", r" \1 ", text)
        ft = "__label__{} {}".format(d.get("rating"), text)
        
        if random.random() <= test_percent:
            test_output.write(ft +"\n")
        else:
            train_output.write(ft + "\n")
            