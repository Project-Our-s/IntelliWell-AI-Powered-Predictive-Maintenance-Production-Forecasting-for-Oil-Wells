import os
import joblib
from config import MODEL_FOLDER

# ===============================
# Load Models
# ===============================

production_model = joblib.load(
    os.path.join(MODEL_FOLDER, "production_model.pkl")
)

pressure_model = joblib.load(
    os.path.join(MODEL_FOLDER, "pressure_model.pkl")
)

pressure_scaler = joblib.load(
    os.path.join(MODEL_FOLDER, "pressure_scaler.pkl")
)

production_features = joblib.load(
    os.path.join(MODEL_FOLDER, "production_features.pkl")
)

pressure_features = joblib.load(
    os.path.join(MODEL_FOLDER, "pressure_features.pkl")
)

print("All models loaded successfully.")