import requests

API_URL = "http://127.0.0.1:5000"


def call_api(endpoint, uploaded_file):

    uploaded_file.seek(0)

    files = {

        "file": (

            uploaded_file.name,

            uploaded_file,

            "application/octet-stream"

        )

    }

    response = requests.post(

        f"{API_URL}/{endpoint}",

        files=files

    )

    return response.json()