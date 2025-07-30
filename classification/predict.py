import joblib
model = joblib.load("models/doc_classifier.pkl")

def classify_document(text):
    return model.predict([text])[0]
