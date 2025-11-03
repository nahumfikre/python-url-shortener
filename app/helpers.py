import secrets
import string

ALPHABET = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
BASE = len(ALPHABET)

def _base62(n: int) -> str:
    if n == 0:
        return ALPHABET[0]
    s = []
    while n > 0:
        n, r = divmod(n, BASE)
        s.append(ALPHABET[r])
    return ''.join(reversed(s))

def make_short_code(length: int = 8) -> str:
    # random 48-bit number → base62 string
    n = secrets.randbits(48)
    code = _base62(n)
    if len(code) < length:
        code = code.rjust(length, '0')
    return code[:length]

def is_valid_code(code: str) -> bool:
    # check basic format for custom codes
    return (
        3 <= len(code) <= 12 and
        all(c in (string.ascii_letters + string.digits) for c in code)
    )
