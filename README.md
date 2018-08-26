# ML-Review-Classifier
Text classifier for 5-star type reviews using [FastText](https://github.com/facebookresearch/fastText/), 
[scikit-learn](http://scikit-learn.org) Python.

Right now the preprocess is working for the MDSD dataset. 
Outputs train and test files that work to build a model. 

## Data Sets
- Multi-Domain Sentiment Dataset (version 2.0) - http://www.cs.jhu.edu/~mdredze/datasets/sentiment/
- Yelp Reviews - https://www.yelp.com/dataset/download

### MDSD

The MDSD dataset has about 1.4M Amazon reviews.

```
$ bin/fasttext supervised -input fasttext-mdsd-train.txt -output msds-model
Read 215M words
Number of words:  1068916
Number of labels: 4
Progress: 100.0% words/sec/thread: 1118237 lr:  0.000000 loss:  0.660613 ETA:   0h 0m

$ bin/fasttext test msds-model.bin fasttext-mdsd-test.txt
N       142392
P@1     0.738
R@1     0.738
Number of examples: 142392
```

## References 

[Machine Learning, NLP: Text Classification using scikit-learn, python and NLTK](https://towardsdatascience.com/machine-learning-nlp-text-classification-using-scikit-learn-python-and-nltk-c52b92a7c73a)