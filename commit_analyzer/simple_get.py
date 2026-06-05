import requests
import json
import hashlib

resp = requests.get("https://api.close.com/buildwithus/")
resp.raise_for_status()
instructions = resp.json()
print(json.dumps(instructions, indent=4))


instruct_key = instructions["key"].encode("utf-8")
hashes = []
for key, value in instructions.items():
    if key.lower() == "traits":

        hashes = [
            hashlib.blake2b(
                trait.encode("utf-8"), key=instruct_key, digest_size=64
            ).hexdigest()
            for trait in instructions["traits"]
        ]
post_resp = requests.post("https://api.close.com/buildwithus/", json=hashes)
print(post_resp.status_code)
print(post_resp.text)
