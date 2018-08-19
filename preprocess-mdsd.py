import re
from pathlib import Path


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

with Path("mdsd-example.txt").open() as data:

    ilevel     = 0
    review_str = ""

    for line in data:

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

print("done")