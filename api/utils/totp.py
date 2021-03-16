# 
# conda env export -n <env-name> > environment.yml

import hmac, base64, struct, hashlib, time, secrets

SEED_LENGTH = 32
TIME_INTERVAL=120

def get_hotp_token(secret, random_seq, intervals_no):
    secret = secret.replace(random_seq[0], random_seq[1])
    secret = secret.replace(random_seq[2], random_seq[3])
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


def get_totp_token(secret, random_seq, intervals_no = time.time()):
    #ensuring to give the same otp for 30 seconds
    x =str(
      get_hotp_token(
        secret, 
        random_seq,
        int(intervals_no)//TIME_INTERVAL, 
        ))
    #adding 0 in the beginning till OTP has 6 digits
    while len(x)!=6:
        x+='0'
    return x


def generate_seed():
    return secrets.token_hex(SEED_LENGTH)


def generate_secret_key(seed):
    m = hashlib.sha256(str.encode(seed))
    m.digest()
    hex_string = m.hexdigest()
    return base64.b32encode(bytearray(hex_string, 'ascii')).decode('utf-8')
