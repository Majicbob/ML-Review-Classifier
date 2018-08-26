import mdsd 
from pathlib import Path

file = Path("../sorted_data/software/all.review")

data = mdsd.parse_file(file)

