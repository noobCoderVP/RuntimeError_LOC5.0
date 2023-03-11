# this file is responsible for signing, encoding, decoding and returning JWTs.

import time

# can be used for setting the expiry of JWT token

import jwt
from decouple import config

JWT_SECRET = config("SECRET")
JWT_ALGORITHM = config("ALGORITHM")

# this function returns the generated tokens (JWTs)
def token_response(token: str):
    return {"access token": token}


# function used for signing with JWT
def signJWT(userID: str):
    # creating the payload to be sent to the client
    payload = {"userid": userID, "expiry": time.time() + 10000}

    token = jwt.encode(payload, key=JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token_response(token)


# function used for decoding the JWT token
def decodeJWT(token: str):
    try:
        decoded_token = jwt.decode(token, key=JWT_SECRET, algorithms=JWT_ALGORITHM)

        #  it will be decoded only if it is not expired
        if decoded_token["expiry"] >= time.time():
            return decoded_token
        else:
            return None
    except:
        return {}
