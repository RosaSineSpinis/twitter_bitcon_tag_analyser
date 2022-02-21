from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
BASE_SOURCE = Path(__file__).resolve().parent.parent
BASE_SOURCE = os.path.join(BASE_SOURCE, "twitter_tag_analysis")
print("BASE_DIR", BASE_DIR)
print("BASE_SOURCE", BASE_SOURCE)
# Use a separate file for the secret key
# for f in os.listdir(BASE_SOURCE):
#     print("f", f)
with open(os.path.join(BASE_SOURCE, 'Secret_Key.py')) as f:
    key_django = f.read().strip().split()[2].strip("\"")
    print("key_django1 ", key_django)
# C:\\Users\\piotr\\PycharmProjects\\twitter_webapp\\twitter_tag_analysis\\Secret_Key.py
# C:\Users\piotr\PycharmProjects\twitter_webapp\src\twitter_tag_analysis\Secret_Key.py

BASE_SOURCE = Path(__file__).resolve().parent
with open(os.path.join(BASE_SOURCE, '_twitter_api_keys.py')) as f:
    key_django = f.read().strip().split()[2].strip("\"")

count = 0
consumer_key, consumer_secret, access_token, access_token_secret, bearer_token = "", "", "", "", ""

with open(os.path.join(BASE_SOURCE, '_twitter_api_keys.py')) as f:
    while True:
        line = f.readline()
        if not line:
            break
        line = line.strip().split()
        key_django_name = line[0].strip()
        key_django = line[2].strip("\"")
        if key_django_name == "consumer_key":
            consumer_key = key_django
        elif key_django_name == "consumer_secret":
            consumer_secret = key_django
        elif key_django_name == "access_token":
            access_token = key_django
        elif key_django_name == "access_token_secret":
            access_token_secret = key_django
        elif key_django_name == "bearer_token":
            bearer_token = key_django

print("consumer_key", consumer_key, "consumer_secret", consumer_secret, "access_token", access_token,
    "access_token_secret", access_token_secret, "bearer_token", bearer_token)
