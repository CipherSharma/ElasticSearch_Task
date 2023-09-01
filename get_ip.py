import requests
from requests.auth import HTTPDigestAuth
from ipify import get_ip

atlas_group_id = "60eeeeccc9f71759d18248ce"
atlas_api_key_public = "vxondbah"
atlas_api_key_private = "00b4ea09-7c21-4a7c-a467-1f22a86b9d6a"
ip = get_ip()
print(ip)

resp = requests.post(
    "https://cloud.mongodb.com/api/atlas/v1.0/groups/{atlas_group_id}/accessList".format(atlas_group_id=atlas_group_id),
    auth=HTTPDigestAuth(atlas_api_public_key, atlas_api_private_key),
    json=[{'ipAddress': ip, 'comment': 'From PythonAnywhere'}]  # the comment is optional
)
if resp.status_code in (200, 201):
    print("MongoDB Atlas accessList request successful", flush=True)
else:
    print(
        "MongoDB Atlas accessList request problem: status code was {status_code}, content was {content}".format(
            status_code=resp.status_code, content=resp.content
        ),
        flush=True
    )