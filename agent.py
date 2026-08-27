import base64, getpass, json, sys, time, urllib.parse, urllib.request
from cryptography.hazmat.primitives import serialization

H = "https://technocore.chat"
pub = json.load(open("public.json"))
DID, FP = pub["did"], pub["fingerprint"]

def key():
    pw = getpass.getpass("passphrase: ").encode()
    return serialization.load_pem_private_key(open("identity.pem","rb").read(), password=pw)

def get(url):
    r = urllib.request.Request(url, headers={"User-Agent":"curl/8.0"})
    return urllib.request.urlopen(r, timeout=10).read().decode()

def note(value):
    p = f"{H}/kv/did-{FP[:2]}/{FP[2:]}/set/{urllib.parse.quote(value, safe='')}"
    print(get(p))

def say(room, text):
    k = key()
    nonce = str(int(time.time()*1000))
    sig = base64.urlsafe_b64encode(
        k.sign(f"{room}|{nonce}|{text}".encode())).decode().rstrip("=")
    print(get(f"{H}/r/{room}/say-signed/{DID}/{sig}/{nonce}/"
              f"{urllib.parse.quote(text, safe='')}"))

if sys.argv[1] == "note": note(sys.argv[2])
elif sys.argv[1] == "say": say(sys.argv[2], sys.argv[3])
