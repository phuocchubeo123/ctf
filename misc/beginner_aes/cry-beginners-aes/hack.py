from Crypto.Util.Padding import pad
from Crypto.Cipher import AES
from os import urandom
import hashlib
from tqdm import tqdm

flag_hash = '6a96111d69e015a07e96dcd141d31e7fc81c4420dbbef75aef5201809093210e'

for i in range(128):
    for j in range(128):
        key = b'the_enc_key_is_'
        iv = b'my_great_iv_is_'
        key += i.to_bytes()
        iv += j.to_bytes()

        cipher = AES.new(key, AES.MODE_CBC, iv)
        enc = b'\x16\x97,\xa7\xfb_\xf3\x15.\x87jKRaF&"\xb6\xc4x\xf4.K\xd77j\xe5MLI_y\xd96\xf1$\xc5\xa3\x03\x990Q^\xc0\x17M2\x18'

        msg = cipher.decrypt(enc)

        try:
            FLAG = msg.decode()
            new_flag_hash = hashlib.sha256(msg).hexdigest()
            print(FLAG)
            print(FLAG == "FLAG{7h3_f1r57_5t3p_t0_Crypt0!!}")
        except UnicodeDecodeError:
            continue