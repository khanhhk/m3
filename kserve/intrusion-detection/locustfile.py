import json

from locust import HttpUser, task

# Define YOUR OWN authservice_session for authentication
cookies = {
    "authservice_session": "MTcxNTE3NTgyMXxOd3dBTkRWV1JFWkpNa0V6VDFSQ05GTk5SVE0yUjBRelIxVXlXa1F5TjBkVk0wbzBTakkwUmtaS1ExTTBWRXhRUkZkRU0xZFZURUU9fBW9GFBi0ABdYdRguQSsrvLQEpB-up8Ts1yhtYuoBXvP",
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


class ModelUser(HttpUser):
    @task
    def detect(self):
        kserve_svc_name = "intrusion-detection-model"
        self.client.post(
            f"/v1/models/{kserve_svc_name}:predict",
            cookies=cookies,
            data=json.dumps(data),
            headers=headers,
        )
