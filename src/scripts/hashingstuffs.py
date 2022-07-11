import base64
import hashlib
import hmac
import secrets
from dataclasses import dataclass
from typing import Callable

import pytest


class AuthenticationError(Exception):
    pass


""" Plaintext = BAD"""


def update_password_plaintext(db, user, password: str) -> None:
    user.password = password
    db.store(user)


def verify_password_plaintext(user, password: str) -> None:
    pw = user.password
    if not hmac.compare_digest(pw, password):
        raise AuthenticationError


"""Hashed = GOOD"""


def hash_name(hash_fn: Callable[[bytes], bytes]) -> str:
    if hash_fn.name == "blake2b":
        return "blake2b"
    raise ValueError


def hash_from_name(name: str) -> Callable[[bytes], bytes]:
    if name == "blake2b":
        def hash_fn(data: bytes) -> bytes:
            return hashlib.blake2b(data).digest()

        hash_fn.name = "blake2b"
        return hash_fn
    raise ValueError


def hash_str_and_b64_encode(hash_fn: Callable[[bytes], bytes], password: str) -> None:
    password_bytes = password.encode("utf-8")
    hashed_bytes = hash_fn(password_bytes)
    hashed_bytes = base64.b64encode(hashed_bytes)
    hashed_password = hashed_bytes.decode("ascii")
    return hashed_password


def update_password_hashed(db, user, hash_fn: Callable[[bytes], bytes], password: str) -> None:
    hashed_password = hash_str_and_b64_encode(hash_fn, password)
    name = hash_name(hash_fn)
    user.password = f'{name}:{hashed_password}'
    db.store(user)


def verify_password_hashed(user, password: str) -> None:
    hash_fn_name, hashed_password = user.password.split(":")
    hash_fn = hash_from_name(hash_fn_name)
    h = hash_str_and_b64_encode(hash_fn, password)

    if not hmac.compare_digest(hashed_password, h):
        raise AuthenticationError


"""Hashed and Salted = EVEN BETTER"""


def gen_salt() -> str:
    return secrets.token_urlsafe(20)


def update_password_hashed_salted(db, user, hash_fn: Callable[[bytes], bytes], password: str) -> None:
    salt = gen_salt()
    hashed_password = hash_str_and_b64_encode(hash_fn, salt + password)
    name = hash_name(hash_fn)
    user.password = f'{name}:{salt}:{hashed_password}'
    db.store(user)


def verify_password_hashed_salted(user, password: str) -> None:
    hash_fn_name, salt, hashed_password = user.password.split(":")
    hash_fn = hash_from_name(hash_fn_name)
    h = hash_str_and_b64_encode(hash_fn, salt + password)

    if not hmac.compare_digest(hashed_password, h):
        raise AuthenticationError


"""Hashed and Salted and Peppered = BEST"""


def get_global_pepper() -> str:
    return "deez nuts"


def update_password_hashed_salted_peppered(db, user, hash_fn: Callable[[bytes], bytes], password: str) -> None:
    salt = gen_salt()
    pepper = get_global_pepper()
    hashed_password = hash_str_and_b64_encode(
        hash_fn, salt + pepper + password)
    name = hash_name(hash_fn)
    user.password = f'{name}:{salt}:{pepper}:{hashed_password}'
    db.store(user)


def verify_password_hashed_salted_peppered(user, password: str) -> None:
    hash_fn_name, salt, pepper, hashed_password = user.password.split(':')
    hash_fn = hash_from_name(hash_fn_name)
    h = hash_str_and_b64_encode(hash_fn, salt + pepper + password)

    if not hmac.compare_digest(hashed_password, h):
        raise AuthenticationError


def main():
    class FakeDB:
        def __init__(self):
            self.user = None

        def store(self, user):
            self.user = user
            print(f'Stored {user.email} with password: {user.password}\n')

    @dataclass
    class User:
        email: str
        password: str

    user = User(email='test@gmail.com', password='password')
    db = FakeDB()
    hash_fn = hash_from_name("blake2b")

    print('Plaintext:')
    update_password_plaintext(db, user, 'password')
    verify_password_plaintext(user, 'password')
    with pytest.raises(AuthenticationError):
        verify_password_plaintext(user, 'wrong')

    print('Hashed:')
    update_password_hashed(db, user, hash_fn, 'password')
    verify_password_hashed(user, 'password')
    with pytest.raises(AuthenticationError):
        verify_password_hashed(user, 'wrong')

    print('Hashed and Salted:')
    update_password_hashed_salted(db, user, hash_fn, 'password')
    verify_password_hashed_salted(user, 'password')
    with pytest.raises(AuthenticationError):
        verify_password_hashed_salted(user, 'wrong')

    print('Hashed and Salted and Peppered:')
    update_password_hashed_salted_peppered(db, user, hash_fn, 'password')
    verify_password_hashed_salted_peppered(user, 'password')
    with pytest.raises(AuthenticationError):
        verify_password_hashed_salted_peppered(user, 'wrong')


if __name__ == '__main__':
    main()
