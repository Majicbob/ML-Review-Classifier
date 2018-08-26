import fasttext
import re


def format(text):
    text = text.replace("\n", "").lower()
    text = re.sub(r"([.!?,/()])", r" \1 ", text)
    
    return text
    
    
reviews = [
    "This restaurant literally changed my life. This is the best food I've ever eaten!",
    "I hate this place so much. They were mean to me.",
    "I don't know. It was ok, I guess. Not really sure what to say."
]

preprocessed_reviews = list(map(format, reviews))

classifier = fasttext.load_model('reviews_model.vec')

labels, probabilities = classifier.predict(preprocessed_reviews, 1)

# Print the results
for review, label, probability in zip(reviews, labels, probabilities):
    stars = int(label[0][-1])

    print("{} ({}% confidence)".format("☆" * stars, int(probability[0] * 100)))
    print(review)
    print()