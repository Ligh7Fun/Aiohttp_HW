import requests

# create user
# response = requests.post(
#     "http://127.0.0.1:8080/user",
#     json={"email": "user1@mail.ru", "password": "12345"},
#     headers={"Content-Type": "application/json"},
#     timeout=(10, 10),
# )

# get by user id
response = requests.get(
    "http://127.0.0.1:8080/user/1",
    headers={"Content-Type": "application/json"},
    timeout=(10, 10),
)

# patch user by id
# response = requests.patch(
#     "http://127.0.0.1:8080/user/1",
#     json={"email": "new_user1@mail.ru"},
#     headers={"Content-Type": "application/json"},
#     timeout=(10, 10),
# )

# delete user by id
# response = requests.delete(
#     "http://127.0.0.1:8080/user/1",
#     headers={"Content-Type": "application/json"},
#     timeout=(10, 10),
# )

print(response.status_code)
print(response.text)
