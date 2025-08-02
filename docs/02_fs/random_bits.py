with open("/dev/urandom", "rb") as reader:
    bytes = reader.read(8)
print([hex(b) for b in bytes])