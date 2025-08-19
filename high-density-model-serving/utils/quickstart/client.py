import json

import requests

if __name__ == "__main__":
    # Define our data for prediction
    data = {
        "inputs": [
            {
                "name": "predict",
                "shape": [1, 64],
                "datatype": "FP32",
                "data": [
                    0.0,
                    0.0,
                    1.0,
                    11.0,
                    14.0,
                    15.0,
                    3.0,
                    0.0,
                    0.0,
                    1.0,
                    13.0,
                    16.0,
                    12.0,
                    16.0,
                    8.0,
                    0.0,
                    0.0,
                    8.0,
                    16.0,
                    4.0,
                    6.0,
                    16.0,
                    5.0,
                    0.0,
                    0.0,
                    5.0,
                    15.0,
                    11.0,
                    13.0,
                    14.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    2.0,
                    12.0,
                    16.0,
                    13.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    13.0,
                    16.0,
                    16.0,
                    6.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    16.0,
                    16.0,
                    16.0,
                    7.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    11.0,
                    13.0,
                    12.0,
                    1.0,
                    0.0,
                ],
            }
        ]
    }

    response = requests.post(
        "http://localhost:8008/v2/models/example-sklearn-isvc/infer",
        data=json.dumps(data),
    )

    print(response.json())
