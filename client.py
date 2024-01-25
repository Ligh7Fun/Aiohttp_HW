import requests

# create ads
# response = requests.post(
#     "http://127.0.0.1:8080/ads",
#     json={"title": "ads1", "description": "ads desc 1", "owner": "user1"},
#     headers={"Content-Type": "application/json"},
#     timeout=(10, 10),
# )

# get by ads id
response = requests.get(
    "http://127.0.0.1:8080/ads/1",
    headers={"Content-Type": "application/json"},
    timeout=(10, 10),
)

# patch ads by id
# response = requests.patch(
#     "http://127.0.0.1:8080/ads/1",
#     json={"title": "New ads 1"},
#     headers={"Content-Type": "application/json"},
#     timeout=(10, 10),
# )

# delete ads by id
# response = requests.delete(
#     "http://127.0.0.1:8080/ads/1",
#     headers={"Content-Type": "application/json"},
#     timeout=(10, 10),
# )

print(response.status_code)
print(response.text)
