import os
import mongoengine
from dotenv import load_dotenv

# IP-Handling on MongoDB Atlas
import requests
from requests.auth import HTTPDigestAuth

load_dotenv()  # initialize / load env variables
DB_URI = os.getenv("mongodb+srv://Cipher:Test@cluster0.qabsj.mongodb.net/?retryWrites=true&w=majority")
db = mongoengine.connect(host=DB_URI)

# whitelist current IP adress via API Key on MongoDB Atlas
# source: https://help.pythonanywhere.com/pages/MongoDB/
print("Whitelisting...")
atlas_group_id = os.getenv("60eeeeccc9f71759d18248ce")
atlas_public_key = os.getenv("vxondbah")
atlas_private_key = os.getenv("00b4ea09-7c21-4a7c-a467-1f22a86b9d6a")

# alternative to receive external ip-adress: https://checkip.amazonaws.com, https://ident.me 
ip = requests.get('https://ident.me').text.strip()

print(ip)

resp = requests.post(
    "https://cloud.mongodb.com/api/atlas/v1.0/groups/{atlas_group_id}/whitelist".format(atlas_group_id=atlas_group_id),
    auth=HTTPDigestAuth(atlas_public_key, atlas_private_key),
    json=[{'ipAddress': ip, 'comment': 'From PythonAnywhere'}]  # the comment is optional
)

if resp.status_code in (200, 201):
    print("MongoDB Atlas whitelist request successful", flush=True)
else:
    print(
        "MongoDB Atlas whitelist request problem: status code was {status_code}, content was {content}".format(
            status_code=resp.status_code, content=resp.content
        ),

        flush=True
    )