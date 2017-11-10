import hashlib
import os
from Crypto.Cipher import AES
import struct
import argparse

'''
    [Config Resource Format]
    0x00: resource size (4 bytes)
    0x04: AES key seed (32 bytes)
    0x16: AES IV seed (32 bytes)
    0x30: AES encrypted config

    [Decrypted Config Format]
    0x00: config size (4 bytes)
    0x04: some crap (idk yet)
    0x08: start of config XML
'''


class ConfigDecrypter:
    def __init__(self, config):
        self.config = config[0x30:]
        self.aes_key = self.running_sha256(config[:0x20])
        self.aes_iv = self.running_sha256(config[0x10:0x30])

    @staticmethod
    def running_sha256(initial_data):
        hash_data = initial_data

        while 1:
            sha256_hash = hashlib.sha256(hash_data).digest()
            hash_data += sha256_hash

            if len(hash_data) > 0x1000:
                break
        return sha256_hash

    def decrypt(self, data=None):
        if data is None:
            data = self.config

        cipher = AES.new(self.aes_key, AES.MODE_CBC, self.aes_iv[:16])
        decrypted_data = cipher.decrypt(data)
        config_length = struct.unpack('<I', decrypted_data[:4])[0]
        config_length += 0x08

        return decrypted_data[0x08:config_length]


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help="config file to decrypt", required=True)
    parser.add_argument('-o', '--output', help="file to save decrypted config to")
    args = parser.parse_args()

    config_file = open(args.input, "rb")
    config_res = config_file.read()
    config_file.close()

    decrypter = ConfigDecrypter(config_res)
    decrypted_config = decrypter.decrypt()

    if args.output is None:
        print(decrypted_config)

    else:
        out_file = open(args.output, 'w')
        out_file.write(decrypted_config)
        out_file.close()
