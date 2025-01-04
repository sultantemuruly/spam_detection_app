import uvicorn
from fastapi import FastAPI
from joblib import load
from email_schema import EmailSchema
from text_processing import preprocess_text

app = FastAPI()

vectorizer = load("vectorizer.joblib")
joblib_in = open("spam_detection.joblib", "rb")
model = load(joblib_in)


@app.get("/")
def index():
    return {"message": "Spam Detection ML API"}


@app.post("/email/predict")
def predict_email_type(data: EmailSchema):
    try:
        data = data.dict()
        text = data["text"]
        X_email = vectorize_text(text)

        pred = model.predict_proba(X_email)[0]
        labels = ["Ham", "Spam"]
        prediction_dict = {labels[i]: prob for i, prob in enumerate(pred)}

        return prediction_dict
    except Exception as e:
        return {"status": "Error loading model", "details": str(e)}


@app.get("/health")
def health_check():
    try:
        test_text = "Participate in a lottery and win car for free!"
        X_email = vectorize_text(test_text)
        pred = model.predict_proba(X_email)[0]
        labels = ["Ham", "Spam"]
        prediction_dict = {labels[i]: prob for i, prob in enumerate(pred)}

        return prediction_dict
    except Exception as e:
        return {"status": "Error loading model", "details": str(e)}


def vectorize_text(text):
    processed_text = preprocess_text(text)
    text_corpus = [processed_text]
    X_email = vectorizer.transform(text_corpus)
    return X_email
