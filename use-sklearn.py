from sklearn.datasets import fetch_20newsgroups
import mdsd 
from pathlib import Path

file = Path("../sorted_data/software/all.review")

data = mdsd.parse_file(file)

twenty_train = fetch_20newsgroups(subset='train', shuffle=True)