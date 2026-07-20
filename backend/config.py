import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

MODEL_FOLDER = os.path.join(BASE_DIR, "models")

UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")

ALLOWED_EXTENSIONS = {"csv", "xlsx"}

DEBUG = True