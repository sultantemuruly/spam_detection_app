from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

import uvicorn
from joblib import load

from email_schema import EmailSchema
from text_processing import preprocess_text

import os

app = FastAPI()

origins = ["https://sultantemuruly.github.io/spam_detection_app"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

vectorizer = load("vectorizer.joblib")
joblib_in = open("spam_detection.joblib", "rb")
model = load(joblib_in)


@app.get("/")
def index():
    return {"message": "Spam Detection ML API"}


@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    return FileResponse("static/favicon.ico")


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
