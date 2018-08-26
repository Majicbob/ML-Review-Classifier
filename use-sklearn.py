import mdsd 
from pathlib import Path
import numpy

file = Path("../sorted_data/software/all.review")

data = mdsd.parse_file(file)
# sklearn uses slight different structures
targets = numpy.array(list(map(lambda x: x['rating'], data)))
review_text = list(map(lambda x: x['text'], data))



from sklearn.feature_extraction.text import CountVectorizer
count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(review_text)