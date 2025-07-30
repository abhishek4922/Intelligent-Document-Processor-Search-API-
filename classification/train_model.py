import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline
import joblib 

def train_classifier():
    df = pd.read_csv("data/sample_data.csv")
    x,y =df["text"],df["label"]

    clf_pipeline = Pipeline([
        ("tfidf",TfidfVectorizer()),
        ("clf",SGDClassifier())
    ])


    clf_pipeline.fit(x,y)
    joblib.dump(clf_pipeline,"models/doc_classifier.pkl")
    print("model trained")

if __name__=="__main__":
    train_classifier()
    