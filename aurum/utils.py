import hashlib


def gen_file_hash(file_name):
    sha1 = hashlib.sha1()
    buf_size = 65536  # lets read stuff in 64kb chunks!

    with open(file_name, 'rb') as f:
        while True:
            data = f.read(buf_size)
            if not data:
                break
            sha1.update(data)

    return sha1.hexdigest()


def make_safe_filename(s):
    def safe_char(c):
        if c.isalnum():
            return c
        else:
            return "_"

    return "".join(safe_char(c) for c in s).rstrip("_")
