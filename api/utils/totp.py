# 
# conda env export -n <env-name> > environment.yml

import logging
import hmac, base64, struct, hashlib, time, secrets

SEED_LENGTH = 32
TIME_INTERVAL=120

def get_hotp_token(secret, random_seq, intervals_no):
    secret = secret.replace(random_seq[0], random_seq[1])
    secret = secret.replace(random_seq[2], random_seq[3])

    logging.info('Time Interval = ', intervals_no)

    key = base64.b32decode(secret, True)
    #decoding our key
    msg = struct.pack(">Q", intervals_no)
    #conversions between Python values and C structs represente
    h = hmac.new(key, msg, hashlib.sha1).digest()
    o = o = h[19] & 15
    #Generate a hash using both of these. Hashing algorithm is HMAC
    h = (struct.unpack(">I", h[o:o+4])[0] & 0x7fffffff) % 1000000
    #unpacking
    return h


def get_totp_token(secret, random_seq):
    #ensuring to give the same otp for 120 seconds
    unix_time = time.time()
    time_interval = int(unix_time)//TIME_INTERVAL
    passwords = []
    for n in range(time_interval - 1, time_interval + 2):
        x =str(
        get_hotp_token(
            secret, 
            random_seq,
            n, 
            ))

        #adding 0 in the beginning till OTP has 6 digits
        while len(x)!=6:
            x+='0'
        passwords.append(x)
    return passwords

def generate_seed():
    return secrets.token_hex(SEED_LENGTH)


def generate_secret_key(seed):
    m = hashlib.sha256(str.encode(seed))
    m.digest()
    hex_string = m.hexdigest()
    return base64.b32encode(bytearray(hex_string, 'ascii')).decode('utf-8')
