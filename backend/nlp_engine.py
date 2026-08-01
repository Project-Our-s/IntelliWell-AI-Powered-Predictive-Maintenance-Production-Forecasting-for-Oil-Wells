import nltk

nltk.download("punkt")
nltk.download("stopwords")
nltk.download("wordnet")
nltk.download("omw-1.4")

"""
=========================================================
IntelliWell NLP Engine
=========================================================
Natural Language Processing Engine for
Maintenance Report Analysis
=========================================================
"""

import re
import string

import yake

from textblob import TextBlob

from nltk.corpus import stopwords

from nltk.tokenize import word_tokenize

from nltk.stem import WordNetLemmatizer


import nltk
import os
import re
import string
import joblib
import numpy as np

import yake

from textblob import TextBlob
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# ==========================================================
# Trained NLP Model Loader
# ==========================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "nlp_maintenance_classifier.pkl"
)

VECTORIZER_PATH = os.path.join(
    BASE_DIR,
    "models",
    "nlp_tfidf_vectorizer.pkl"
)


try:

    nlp_model = joblib.load(
        MODEL_PATH
    )

    nlp_vectorizer = joblib.load(
        VECTORIZER_PATH
    )

    NLP_MODEL_AVAILABLE = True

    print(
        "IntelliWell NLP classifier loaded successfully."
    )

except Exception as error:

    nlp_model = None
    nlp_vectorizer = None

    NLP_MODEL_AVAILABLE = False

    print(
        "WARNING: NLP classifier could not be loaded."
    )

    print(
        "Reason:",
        error
    )



lemmatizer = WordNetLemmatizer()

STOP_WORDS = set(stopwords.words("english"))

def clean_text(text):
    """
    Clean maintenance report text.
    """

    text = str(text).lower()

    text = re.sub(r"http\S+", "", text)

    text = re.sub(r"\d+", "", text)

    text = text.translate(
        str.maketrans(
            "",
            "",
            string.punctuation
        )
    )

    words = word_tokenize(text)

    words = [

        lemmatizer.lemmatize(word)

        for word in words

        if word not in STOP_WORDS

    ]

    return " ".join(words)
def extract_keywords(text, top_n=5):
    """
    Extract important keywords.
    """

    extractor = yake.KeywordExtractor(
        top=top_n
    )

    keywords = extractor.extract_keywords(text)

    return [

        keyword

        for keyword, score in keywords

    ]
ISSUE_KEYWORDS = {

    "Pressure Issue": [
        "pressure",
        "annulus",
        "downhole",
        "tubing pressure"
    ],

    "Mechanical Issue": [
        "pump",
        "motor",
        "bearing",
        "vibration"
    ],

    "Production Issue": [
        "production",
        "flow",
        "oil",
        "gas"
    ],

    "Leak": [
        "leak",
        "tubing leak",
        "pipeline"
    ],

    "Valve Issue": [
        "valve",
        "choke",
        "blockage"
    ],

    "Electrical Issue": [
        "voltage",
        "sensor",
        "electrical"
    ]

}
def classify_issue_rule_based(text):

    text = text.lower()

    for category, words in ISSUE_KEYWORDS.items():

        if any(
            word in text
            for word in words
        ):

            return category

    return "Normal Operation"
# ==========================================================
# ML Maintenance Issue Classification
# ==========================================================

def classify_issue_ml(cleaned_text):
    """
    Classify a maintenance report using the trained
    TF-IDF + Machine Learning classifier.
    """

    if not NLP_MODEL_AVAILABLE:

        return None

    try:

        vector = nlp_vectorizer.transform(
            [cleaned_text]
        )

        prediction = nlp_model.predict(
            vector
        )[0]

        return str(prediction)

    except Exception as error:

        print(
            "ML classification failed:",
            error
        )

        return None
def analyze_sentiment(text):

    polarity = TextBlob(text).sentiment.polarity

    if polarity > 0.2:
        return "Positive"

    if polarity < -0.2:
        return "Negative"

    return "Neutral"
# ==========================================================
# Report Summarization
# ==========================================================

def summarize_report(text, max_sentences=2):
    """
    Generate a concise summary of a maintenance report.
    """

    sentences = re.split(r'(?<=[.!?])\s+', text.strip())

    if len(sentences) <= max_sentences:
        return text

    return " ".join(sentences[:max_sentences])
# ==========================================================
# Risk Priority
# ==========================================================

def calculate_priority(category, sentiment):

    if category in [
        "Leak",
        "Electrical Issue"
    ]:
        return "Critical"

    if category in [
        "Pressure Issue",
        "Mechanical Issue"
    ]:
        return "High"

    if sentiment == "Negative":
        return "Medium"

    return "Low"
# ==========================================================
# Maintenance Recommendation
# ==========================================================

RECOMMENDATIONS = {

    "Pressure Issue":
        "Inspect tubing pressure, annulus pressure and choke settings.",

    "Mechanical Issue":
        "Inspect pump, bearings and vibration levels.",

    "Leak":
        "Inspect well immediately for possible leakage.",

    "Valve Issue":
        "Check choke valve and clean any blockage.",

    "Electrical Issue":
        "Inspect electrical system and sensor wiring.",

    "Production Issue":
        "Review production parameters and optimize flow.",

    "Normal Operation":
        "No immediate action required."

}


def recommend_action(category):

    return RECOMMENDATIONS.get(

        category,

        "No recommendation available."

    )
# ==========================================================
# Complete NLP Analysis
# ==========================================================

def analyze_report(report_text):
    """
    Complete NLP analysis pipeline.
    """

    cleaned = clean_text(report_text)

    keywords = extract_keywords(cleaned)

    category = classify_issue(cleaned)

    sentiment = analyze_sentiment(report_text)

    summary = summarize_report(report_text)

    priority = calculate_priority(
        category,
        sentiment
    )

    recommendation = recommend_action(category)

    return {

    "original_report": report_text,

    "clean_report": cleaned,

    "summary": summary,

    "keywords": keywords,

    "category": category,

    "sentiment": sentiment,

    "priority": priority,

    "severity": severity_score(category),

    "root_cause": root_cause(category),

    "actions": immediate_actions(category),

    "confidence": confidence(category),

    "recommendation": recommendation

}
# ==========================================================
# Severity Score
# ==========================================================

SEVERITY = {

    "Leak":95,

    "Electrical Issue":90,

    "Pressure Issue":80,

    "Mechanical Issue":75,

    "Valve Issue":65,

    "Production Issue":55,

    "Normal Operation":10

}


def severity_score(category):

    return SEVERITY.get(

        category,

        30

    )
# ==========================================================
# Root Cause Analysis
# ==========================================================

ROOT_CAUSES = {

    "Pressure Issue":
        "Possible tubing restriction, choke malfunction or reservoir pressure decline.",

    "Mechanical Issue":
        "Pump wear, bearing degradation or motor imbalance.",

    "Leak":
        "Tubing leak, casing integrity issue or pipeline failure.",

    "Valve Issue":
        "Valve blockage, scaling or choke malfunction.",

    "Electrical Issue":
        "Sensor failure, damaged wiring or unstable power supply.",

    "Production Issue":
        "Reservoir depletion or flow instability.",

    "Normal Operation":
        "No significant operational issues detected."

}


def root_cause(category):

    return ROOT_CAUSES.get(

        category,

        "Unable to determine probable cause."

    )
# ==========================================================
# Immediate Actions
# ==========================================================

ACTIONS = {

    "Pressure Issue":[

        "Inspect tubing pressure",

        "Inspect annulus pressure",

        "Check choke settings"

    ],

    "Mechanical Issue":[

        "Inspect ESP pump",

        "Check vibration levels",

        "Inspect bearings"

    ],

    "Leak":[

        "Shut down well if necessary",

        "Inspect tubing",

        "Pressure test pipeline"

    ],

    "Valve Issue":[

        "Inspect choke valve",

        "Clean blockage"

    ],

    "Electrical Issue":[

        "Check sensors",

        "Inspect wiring"

    ],

    "Production Issue":[

        "Review production trend",

        "Optimize flow"

    ],

    "Normal Operation":[

        "Continue monitoring"

    ]

}


def immediate_actions(category):

    return ACTIONS.get(

        category,

        []

    )
# ==========================================================
# Confidence Score
# ==========================================================

def confidence(category):

    scores = {

        "Leak":97,

        "Pressure Issue":93,

        "Mechanical Issue":91,

        "Electrical Issue":90,

        "Valve Issue":88,

        "Production Issue":84,

        "Normal Operation":80

    }

    return scores.get(

        category,

        75

    )
# ==========================================================
# IntelliWell Hybrid Issue Classifier
# ==========================================================

def classify_issue(cleaned_text):
    """
    Primary IntelliWell maintenance issue classifier.

    Uses the trained ML model when available.
    Falls back to the original rule-based classifier
    if the model cannot be loaded or prediction fails.
    """

    ml_prediction = classify_issue_ml(
        cleaned_text
    )

    if ml_prediction is not None:

        return ml_prediction

    return classify_issue_rule_based(
        cleaned_text
    )
def classifier_source():

    if NLP_MODEL_AVAILABLE:

        return "Machine Learning"

    return "Rule-Based Fallback"
# ==========================================================
# Classification Confidence
# ==========================================================

def classification_confidence(cleaned_text, category):
    """
    Return model-derived confidence when supported.

    For models without predict_proba (for example LinearSVC),
    use the decision-function margin converted to a bounded
    display score.

    This score is an operational indicator and should not be
    interpreted as a calibrated probability.
    """

    if not NLP_MODEL_AVAILABLE:

        return None

    try:

        vector = nlp_vectorizer.transform(
            [cleaned_text]
        )

        # ----------------------------------------------
        # Models supporting predict_proba
        # ----------------------------------------------

        if hasattr(nlp_model, "predict_proba"):

            probabilities = nlp_model.predict_proba(
                vector
            )[0]

            return round(
                float(np.max(probabilities)) * 100,
                2
            )

        # ----------------------------------------------
        # Linear SVM / decision-function models
        # ----------------------------------------------

        if hasattr(nlp_model, "decision_function"):

            scores = nlp_model.decision_function(
                vector
            )

            max_margin = float(
                np.max(scores)
            )

            # Bounded display indicator
            confidence_score = (
                1 /
                (
                    1 +
                    np.exp(-max_margin)
                )
            ) * 100

            return round(
                confidence_score,
                2
            )

    except Exception as error:

        print(
            "Confidence calculation failed:",
            error
        )

    return None

# ==========================================================
# Complete IntelliWell NLP Analysis
# ==========================================================

def analyze_report(report_text):
    """
    Complete IntelliWell NLP maintenance analysis pipeline.

    Pipeline:
        Raw Report
            ↓
        Text Cleaning
            ↓
        TF-IDF
            ↓
        ML Classification
            ↓
        NLP Analysis
            ↓
        Decision Support
    """

    # ----------------------------------------------
    # Validate input
    # ----------------------------------------------

    if report_text is None:

        report_text = ""

    report_text = str(
        report_text
    ).strip()

    if not report_text:

        raise ValueError(
            "Maintenance report cannot be empty."
        )

    # ----------------------------------------------
    # NLP preprocessing
    # ----------------------------------------------

    cleaned = clean_text(
        report_text
    )

    # ----------------------------------------------
    # Keyword extraction
    # ----------------------------------------------

    keywords = extract_keywords(
        cleaned
    )

    # ----------------------------------------------
    # ML issue classification
    # ----------------------------------------------

    category = classify_issue(
        cleaned
    )

    # ----------------------------------------------
    # Sentiment
    # ----------------------------------------------

    sentiment = analyze_sentiment(
        report_text
    )

    # ----------------------------------------------
    # Summary
    # ----------------------------------------------

    summary = summarize_report(
        report_text
    )

    # ----------------------------------------------
    # Operational priority
    # ----------------------------------------------

    priority = calculate_priority(
        category,
        sentiment
    )

    # ----------------------------------------------
    # Recommendation
    # ----------------------------------------------

    recommendation = recommend_action(
        category
    )

    # ----------------------------------------------
    # Classification confidence indicator
    # ----------------------------------------------

    model_confidence = classification_confidence(
        cleaned,
        category
    )

    # ----------------------------------------------
    # Final response
    # ----------------------------------------------

    return {

        "original_report":
            report_text,

        "clean_report":
            cleaned,

        "summary":
            summary,

        "keywords":
            keywords,

        "category":
            category,

        "classifier":
            classifier_source(),

        "sentiment":
            sentiment,

        "priority":
            priority,

        "severity":
            severity_score(category),

        "root_cause":
            root_cause(category),

        "actions":
            immediate_actions(category),

        "confidence":
            model_confidence,

        "recommendation":
            recommendation

    }