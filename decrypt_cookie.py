"""
The `main_decryption` function is owned by Nathan Henrie
Gist link : https://gist.github.com/n8henrie/8715089
"""

from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2


def main_decryption(value):
    # replace with your encrypted_value from sqlite3
    encrypted_value = value

    # Trim off the 'v10' that Chrome/ium prepends
    encrypted_value = encrypted_value[3:]

    # Default values used by both Chrome and Chromium in OSX and Linux
    salt = b'saltysalt'
    iv = b' ' * 16
    length = 16

    # On Mac, replace MY_PASS with your password from Keychain
    # On Linux, replace MY_PASS with 'peanuts'
    my_pass = 'peanuts'
    my_pass = my_pass.encode('utf8')

    # 1003 on Mac, 1 on Linux
    iterations = 1

    key = PBKDF2(my_pass, salt, length, iterations)
    cipher = AES.new(key, AES.MODE_CBC, IV=iv)

    decrypted = cipher.decrypt(encrypted_value)
    decrypted = decrypted.decode('utf-8')
    decrypted.strip()
    cleared_value = clear_decrypted_value(decrypted)
    return cleared_value


def clear_decrypted_value(text):
    """clear some junk characters """
    final_value = ''
    escape_list = [2, 3, 5, 6, 8, 9, 10, 14, 15, 16]
    for i in text:
        if ord(i) not in escape_list:
            final_value += i
    return final_value
