import base64
import hashlib
import hmac
import os
import struct
import random as _random

import time

import six


class token:

    seed = None
    token = None
    user = None

    IntLen = 3  # dont change

    pattern = "{t}.{u}.bubbles.com"
    def __init__(self,user):

        self.user = user
        file_name = user + '.seed'
        if os.path.isfile(file_name):
            #read seed from file
            with open(file_name ,'r+') as fd:
                self.seed = fd.read()
        else:
            self.seed = self.generate_seed()

            with open(file_name ,'w+') as fd:
                fd.write(self.seed)



    #generate seed
    def generate_seed(self):
        return self.random_base32()


    #return current OTP
    def get_opt(self):
        return self.get_totp(self.seed,interval_length=self.IntLen)

    #write SSID to file
    def get_ssid(self):
        return self.pattern.format(t = self.get_opt(), u=self.user)

    #write SSID to file
    def write_ssid(self):
        file_name = self.user + '.ssid'
        with open(file_name, 'w+') as fd:
            fd.write(self.get_ssid())

        return self.pattern.format(t = self.get_opt(), u=self.user)

    def random_base32(self, length=16, random=_random.SystemRandom(),
                         chars=list('ABCDEFGHIJKLMNOPQRSTUVWXYZ234567')):
           return ''.join(random.choice(chars) for _ in range(length))

    def get_hotp(
            self,
            secret,
            intervals_no,
            as_string=False,
            casefold=True,
            digest_method=hashlib.sha1,
            token_length=6,
    ):
        if isinstance(secret, six.string_types):
            # It is unicode, convert it to bytes
            secret = secret.encode('utf-8')
        # Get rid of all the spacing:
        secret = secret.replace(b' ', b'')
        try:
            key = base64.b32decode(secret, casefold=casefold)
        except (TypeError):
            raise TypeError('Incorrect secret')
        msg = struct.pack('>Q', intervals_no)
        hmac_digest = hmac.new(key, msg, digest_method).digest()
        ob = hmac_digest[19] if six.PY3 else ord(hmac_digest[19])
        o = ob & 15
        token_base = struct.unpack('>I', hmac_digest[o:o + 4])[0] & 0x7fffffff
        token = token_base % (10 ** token_length)
        if as_string:
            # TODO: should as_string=True return unicode, not bytes?
            return six.b('{{:0{}d}}'.format(token_length).format(token))
        else:
            return token

    def get_totp(
            self,
            secret,
            as_string=False,
            digest_method=hashlib.sha1,
            token_length=6,
            interval_length=30,
            clock=None,
    ):
        if clock is None:
            clock = time.time()
        interv_no = int(clock) // interval_length
        return self.get_hotp(
            secret,
            intervals_no=interv_no,
            as_string=as_string,
            digest_method=digest_method,
            token_length=token_length,
        )


def main():
    file_name = 'user.name'

    if not os.path.isfile(file_name):
        print('user.name file missing - please write user name to file.')
        exit(-1)

    with open(file_name, 'r+') as fd:
        user_name = fd.read()

    user = token(user_name)

    print(user.get_ssid())
    user.write_ssid()

if __name__ == "__main__":
    main()