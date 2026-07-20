from flask import Flask
from routes import api

app = Flask(__name__)

app.register_blueprint(api)

@app.route("/")
def home():

    return {
        "Application": "IntelliWell API",
        "Version": "1.0",
        "Status": "Running"
    }

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )