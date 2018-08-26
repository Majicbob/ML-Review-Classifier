import re
import random
from pathlib import Path
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

def pretty(line, ilevel, indent_str = "    "):
    """Print a line with the given indentation level and return the new level

    Based on the XML like format of the MDSD files.
    Increase indent on open tag, decrease on close.

    Args:
        line: Line to print
        ilevel: Indentation level
        indent_str: String to use as one indent level, default 4 spaces

    Returns: Next indent level
    """
    if ilevel == None:
        ilevel = 0

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

    Args:
        file: File to be parse as a Path object

    Returns: List of dict items with the parsed data
    """
    parsed_data = []
    num_lines   = linecount(file)

    tqdm.write("File: {}\nLines: {}\n".format(file.resolve(), num_lines))

    with file.open(encoding="utf-8",errors="replace") as data:
        ilevel      = 0
        review_str  = ""

        for line in tqdm(data, total=num_lines):
            # put all lines from the same review into a string
            if re.match(r"\s*<review>\s*", line):
                review_str = line

            elif re.match(r"\s*</review>\s*", line):
                review_str += line
                # full review text in str, parse data
                # to handle split files make sure open tag exists
                if re.match(r"\s*<review>\s*", review_str):
                    parsed_data.append(parse_review(review_str))
                else:
                    review_str = ""

            else:
                review_str += line

            # ilevel = pretty(line, ilevel)

        tqdm.write("Reviews: {}\n".format(len(parsed_data)))

    return parsed_data

def format_line(data):
    """Format review data as a single line and return.

    Format is __label__LABELNAME TEXT
    FastText expects the review text to be all one line, lowercase with puntuation seperated.
    Also strips ASCII control chars b/c FastText dies when trying to read them.

    Args:
        data: Dict with rating and text.

    Returns: Properly formatted string.
    """
    text = data.get("text").replace("\n", "").lower()
    text = re.sub(r"([.!?,/()])", r" \1 ", text)

    # strip the ascii control chars, might be faster to do outside of python
    text = re.sub(r'[\x00-\x1F]', r'', text)

    ft = "__label__{} {}".format(d.get("rating"), text)

    return ft