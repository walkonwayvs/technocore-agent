import getpass, hashlib, json, os, pathlib
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519

B58 = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
def b58(b):
    n = int.from_bytes(b, "big"); out = ""
    while n: n, r = divmod(n, 58); out = B58[r] + out
    return "1" * (len(b) - len(b.lstrip(b"\x00"))) + out

p = pathlib.Path("identity.pem")
if p.exists(): raise SystemExit("identity.pem exists - stopping")

pw = getpass.getpass("passphrase: ")
if pw != getpass.getpass("confirm:    "): raise SystemExit("mismatch")
if len(pw) < 16: raise SystemExit("use 16+ characters")

k = ed25519.Ed25519PrivateKey.generate()
p.write_bytes(k.private_bytes(serialization.Encoding.PEM,
    serialization.PrivateFormat.PKCS8,
    serialization.BestAvailableEncryption(pw.encode())))
os.chmod(p, 0o600)

serialization.load_pem_private_key(p.read_bytes(), password=pw.encode())

pub = k.public_key().public_bytes(serialization.Encoding.Raw,
                                  serialization.PublicFormat.Raw)
did = "did:key:z" + b58(b"\xed\x01" + pub)
fp = hashlib.sha256(did.encode()).hexdigest()[:16]
json.dump({"did": did, "fingerprint": fp}, open("public.json", "w"), indent=2)
print("DID:", did)
print("note path: /kv/did-%s/%s" % (fp[:2], fp[2:]))
