import os
import hashlib
import binascii
import jwt
from app import app
from functools import wraps
from flask import request,Response,jsonify
from datetime import datetime,timedelta



def hash_pass(password):
    """Hash a password for storing."""

    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                                  salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash)  # return bytes


def verify_pass(provided_password, stored_password):
    """Verify a stored password against one provided by user"""

    stored_password = stored_password.decode('ascii')
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512',
                                  provided_password.encode('utf-8'),
                                  salt.encode('ascii'),
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password


def createJWT(payload)->str:
    exp = datetime.now()+timedelta(minutes=15)
    payload["exp"] = exp.timestamp()
    token = jwt.api_jwt.encode(payload,app.secret_key)
    return token


def verifyJWT(token):
    try:
        res = jwt.api_jwt.decode(token,app.secret_key,algorithms=["HS256"])
        return res, True
    except Exception as e:
        return str(e),False



def auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            token = request.headers["Authorization"].strip().split(sep=" ")[1]
        except Exception:
            return jsonify({"msg":"Missing Bearer Token"}), 401 
        res,ok = verifyJWT(token)
        if ok:
            request.user = {"id":res['id'],"admin":res['admin']}
            return f(*args, **kwargs)
        else:
            return jsonify({"msg":str(res)}), 401 
    return decorated_function