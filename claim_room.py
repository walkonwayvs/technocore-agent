import base64, json, sys, time, urllib.parse, urllib.request
from cryptography.hazmat.primitives import serialization
import os

H = "https://technocore.chat"
ROOM = "d-walkonwayvs"
pub = json.load(open("public.json")); DID = pub["did"]

pw = open(".passphrase","rb").read().strip() if os.path.exists(".passphrase") else \
     __import__("getpass").getpass("passphrase: ").encode()
k = serialization.load_pem_private_key(open("identity.pem","rb").read(), password=pw)

nonce = str(int(time.time()*1000))
msg = f"room-owners|{ROOM}|{nonce}|{DID}"
sig = base64.urlsafe_b64encode(k.sign(msg.encode())).decode().rstrip("=")
url = (f"{H}/kv/room-owners/{ROOM}/set-signed/{DID}/{sig}/{nonce}/"
       f"{urllib.parse.quote(DID, safe='')}?if_absent=1")
print(url)
import sys; sys.exit()
print(urllib.request.urlopen(
    urllib.request.Request(url, headers={"User-Agent":"curl/8.0"}), timeout=15).read().decode())
