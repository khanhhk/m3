import json

from locust import HttpUser, task

# Define YOUR OWN authservice_session for authentication
cookies = {
    "authservice_session": "MTcwMTAwMTQzNnxOd3dBTkVSQlRFaEhValpWV2xoVFdrdEVXVU5MVjFKTk5sTlBTMGhWVkZFek4wZFJWbFZTUjBKTE5FMVdOME5WV1U0eldUVlVWa0U9fKzy9oiSMjJhP-Jkb4-iF-hwYVaWtJkM66l9XxQ4dvnL",
}

# We will send requests with content-type is json
headers = {
    "Content-Type": "application/x-www-form-urlencoded",
}

# Define our data for prediction
data = {
    "inputs": [
        {
            "name": "predict",
            "shape": [1, 18],
            "datatype": "FP32",
            "data": [
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
        }
    ]
}


class ModelUser(HttpUser):
    @task
    def detect(self):
        mm_svc_name = "intrusion-detection"
        self.client.post(
            f"/v2/models/{mm_svc_name}/infer",
            cookies=cookies,
            data=json.dumps(data),
            headers=headers,
        )
