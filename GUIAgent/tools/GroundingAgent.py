import requests

API_URL = "https://kxrpf3h2ro98k5xr.us-east-1.aws.endpoints.huggingface.cloud"
headers = {
	"Accept" : "application/json",
	"Authorization": "Bearer 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",
	"Content-Type": "application/json" 
}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()

def get_coordinates(image_b64, task, k=2, context=False):
    payload = {
        "inputs": {    
            "image": image_b64,
            "task": task,
            "k": str(k),
            "context": str(context)
        },
        "parameters": {}
    }
    return query(payload)



