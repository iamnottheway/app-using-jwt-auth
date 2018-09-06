from flask import Flask, request, jsonify,session, make_response, redirect, url_for
from jose import jwt
import datetime, time


skey = "testkey"
uid = "123456abcd"


app = Flask(__name__)
app.config["SECRET_KEY"] = "secret"


@app.route("/",methods=["GET"])
def home():
    return "home"



@app.route("/token",methods=["GET"])
def jwt_token():
    # get id
    payload = {
                "uid":uid,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds = 5),
                "iat": round(time.time()),
                "iss": "harowitzblack",
    }
    jwt_tok = jwt.encode(payload, skey, algorithm ='HS256')
    # add the token in a session cookie
    session["uid"] = jwt_tok
    # redirect to the dash for the token to be verified.
    req = make_response(redirect(url_for("dash")))
    return req



@app.route("/cats",methods=["GET"])
def dash():
    # if uid session cookie is found, then decode and verify it
    if session.get("uid"):
        token = session.get("uid")
        if verify_jwt_token(token):
            return jsonify({"Cat supreme":"Donny Mike"})
        return jsonify({"Permission":"unauthorized, token expired"})
    # if the token content doesn't match something - unauthorized.
    return jsonify({"Permission":"unauthorized"})

def verify_jwt_token(token):
    try:
        decoded_token = jwt.decode(token,skey,algorithms=['HS256'])
        uid_from_db = uid
        if decoded_token["uid"] == uid_from_db:
            return True
        return False
    except jwt.ExpiredSignatureError:
        return False


if __name__ == '__main__':
    app.run(debug=True)
