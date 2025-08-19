import json

import requests

if __name__ == "__main__":
    # Define YOUR OWN authservice_session for authentication
    cookies = {
        "authservice_session": "MTcyMzkxMzA1OXxOd3dBTkVOWU5raFVWVFZUVEZsWk1razFUVE5VUWt0U05qWlRXakphVEZKWVVrMUNWRWcxVXpkQk4xSlBORVpaUmt4WVVqVTJRMEU9fI3YDERwK7Gb5Sx-i1V1uMrgo_nPe9PS-LGf25nJqPlv",
    }

    # We will send requests with content-type is json
    headers = {
        "Host": "intrusion-detection.kserve-test.example.com",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    # Define our data for prediction
    data = [
        [
            5.0,
            0.0,
            0.0,
            0.0,
            0.0,
            1.0,
            0.0,
            0.0,
            255.0,
            250.0,
            0.98,
            0.01,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
        ],
    ]

    response = requests.post(
        "http://localhost:8000/v1/models/intrusion-detection-model:predict",
        cookies=cookies,
        data=json.dumps(data),
        headers=headers,
    )

    print(response.json())
