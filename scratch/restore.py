import requests

url = "http://localhost:8000/api/v1/admin/verification/restore-progress"
data = {
    "user_id": "d32c1e2d-8976-4a0b-8464-9abfeeebbb14",
    "completed_count": 14
}
response = requests.post(url, json=data)
print(response.json())
