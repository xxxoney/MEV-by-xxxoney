def to_bufferable(binary):
    return binary


def _get_byte(c):
    return ord(c)


try:
    xrange
except:

    def to_bufferable(binary):
        if isinstance(binary, bytes):
            return binary
        return bytes(ord(b) for b in binary)


    def _get_byte(c):
        return c


def append_PKCS7_padding(data):
    pad = 16 - (len(data) % 16)
    return data + to_bufferable(chr(pad) * pad)


def strip_PKCS7_padding(data):
    if len(data) % 16 != 0:
        raise ValueError("invalid length")

    pad = _get_byte(data[-1])

    if pad > 16:
        raise ValueError("invalid padding byte")

    return data[:-pad]
