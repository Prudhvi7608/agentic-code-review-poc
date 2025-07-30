from fastapi import FastAPI
from pydantic import BaseModel
import requests
import json

app = FastAPI()

class ReviewRequest(BaseModel):
    code: str

@app.post("/review")
async def review_code(request: ReviewRequest):
    code_input = request.code
    payload = {
        "agent_id": "<your-agent-id>",
        "additional_data": {
            "query": json.dumps({
                "code_input": code_input,
                "review_criteria": "default_review_criteria"
            })
        }
    }
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": "<your-api-key>",
        "x-grid": "<your-grid-id>",
        "x-clientrefid": "<your-grid-id>"
    }
    url = "<x42-api-url>"  # TODO: Replace with actual URL
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        result = response.json()
        return {"review": result}
    except Exception as e:
        return {"error": str(e)}
