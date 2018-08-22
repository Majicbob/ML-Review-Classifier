import re
from pathlib import Path
import random
from tqdm import tqdm


def parse_review(review_str):
    """Parse rating and review text out of the given string and return.
    
    Args: 
        review_str: A whole review in the XML-like format the MDSD files use.
        
    Returns: A dict with rating and text.
    """
    m = re.search(r"<rating>\s*(\d)\.\d\s*</rating>", review_str)
    if m:
        rating = m.groups(0)[0]

    m = re.search(r"<review_text>\s*(.*)\s*</review_text>", review_str, re.DOTALL)
    if m:
        text = m.groups(0)[0]

    return { 'rating': rating, 'text': text}

def pretty(line, ilevel):
    """Print a line with the given indentation level and return the new level

    Based on the XML like format of the MDSD files.
    Increase indent on open tag, decrease on close.
    
    Args:
        line: Line to print 
        ilevel: Indentation level
    """
    if ilevel == None:
        ilevel = 0


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

    return ilevel

def linecount(filename):
    """A fast function to get the number of lines in a file."""
    def _make_gen(reader):
        b = reader(1024 * 1024)
        while b:
            yield b
            b = reader(1024*1024)

    f = open(filename, 'rb')
    f_gen = _make_gen(f.raw.read)

    return sum( buf.count(b'\n') for buf in f_gen )

def parse_file(file):
    """Read file line by line, when a whole review has been read parse it.
    
    """
    num_lines = linecount(file)

    tqdm.write("File: {}\nLines: {}\n".format(file.resolve(), num_lines))

    with file.open() as data:
        parsed_data = []
        ilevel      = 0
        review_str  = ""
    
        for line in tqdm(data, total=num_lines):
            # put all lines from the same review into a string
            if re.match(r"\s*<review>\s*", line):
                review_str = line
            elif re.match(r"\s*</review>\s*", line):
                review_str += line
                # full review text in str, parse data
                parsed_data.append(parse_review(review_str))
            else:
                review_str += line
    
            # ilevel = pretty(line, ilevel)
        
        return parsed_data


"""Some of the MDSD files with various sizes for testing

1.4G sorted_data/books/all.review
198M sorted_data/dvd/all.review
7.0M sorted_data/apparel/all.review
315K sorted_data/musical_instruments/all.review
"""
mdsd_file = Path("../sorted_data/musical_instruments/all.review")

parsed_data  = []
test_percent = 0.1 # percent of reviews to be put in test file instead of train file

parsed_data.extend(parse_file(mdsd_file))
parsed_data.extend(parse_file(Path("../sorted_data/apparel/all.review")))
parsed_data.extend(parse_file(Path("../sorted_data/software/all.review")))

# Format parsed data to FastText format and write training and test files.
tqdm.write("\nFormatting data and writing files\n")
with Path("fasttext-mdsd-train.txt").open("w") as train_output, \
     Path("fasttext-mdsd-test.txt").open("w") as test_output:
    for d in tqdm(parsed_data):
        # FastText expects the review text to be all one line, lowercase with puntuation seperated
        text = d.get("text").replace("\n", "").lower()
        text = re.sub(r"([.!?,/()])", r" \1 ", text)

        # strip the ascii control chars, they cause errors (might be faster to do outside of python)
        text = re.sub(r'[\x00-\x1F]', r'', text)

        ft = "__label__{} {}".format(d.get("rating"), text)

        if random.random() <= test_percent:
            test_output.write(ft +"\n")
        else:
            train_output.write(ft + "\n")

