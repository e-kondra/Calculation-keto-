import hashlib


def make_hash(password):
    if password:
        hash_obj = hashlib.sha256(bytes(password.encode('utf-8'))).hexdigest()
        return hash_obj
    return None