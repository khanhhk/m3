# Ref: https://github.com/cloudevents/sdk-python#receiving-cloudevents
from fastapi import FastAPI, Request

app = FastAPI()

# Create an endpoint at http://localhost:8000
@app.post("/")
async def on_event(request: Request):
    # Inspect the data
    data = await request.json()
    # Inspect the headers
    headers = request.headers
    
    print("Received a new event!")
    print("data: ", data)
    print("headers: ", headers)

    # Return no content
    return "", 204