from flask import Flask, request
from user import User
import json
from commands.status import handle_status
from commands.on_off import handle_power
from commands.setting import handle_setting
from commands.clone import handle_clone
from commands.delete import handle_delete
from commands.execute import handle_execute
from commands.upload import handle_upload
from commands.transfer import handle_transfer

app = Flask(__name__)

users = {
    "user1": User("user1", "123456"),
    "admin": User("admin", "123456")
}


def handle_commands(body, is_admin):
    authorized = is_admin
    for key, value in body.items():
        if value == "VM1":
            authorized = True
            break
    if not authorized:
        raise Exception("UnAuthorized")

    if body["command"] == "status":
        return handle_status(body)
    elif body["command"] == "on/off":
        return handle_power(body)
    elif body["command"] == "setting":
        return handle_setting(body)
    elif body["command"] == "clone":
        return handle_clone(body)
    elif body["command"] == "delete":
        return handle_delete(body)
    elif body["command"] == "execute":
        return handle_execute(body)
    elif body["command"] == "upload":
        return handle_upload(body)
    elif body["command"] == "transfer":
        return handle_transfer(body)


def handle_auth(headers):
    logged_in = False
    is_admin = False
    auth_token = headers["Authorization"]
    for key, user in users.items():
        if user.check_token(auth_token):
            logged_in = True
            if user.is_admin(auth_token):
                is_admin = True
            break
    if not logged_in:
        raise Exception("UnAuthenticated")
    return is_admin


@app.route("/auth", methods=["POST"])
def login():
    try:
        body = json.loads(request.data)
        if "username" in body and "password" in body and len(body) == 2:
            for key, user in users.items():
                token = user.login(body["username"], body["password"])
                if token:
                    return json.dumps({"token": token})
            raise Exception("UnAuthenticated")
        else:
            raise Exception("Sorry")
    except Exception as e:
        print("error", e)
        return json.dumps({"error": str(e)})


@app.route("/", methods=["GET"])
def req():
    try:
        body = json.loads(request.data)
        headers = request.headers
        is_admin = False

        if "Authorization" in headers:
            is_admin = handle_auth(headers)
        else:
            raise Exception("UnAuthenticated")

        if "command" in body:
            return handle_commands(body, is_admin)
        else:
            raise Exception("command is required.")

    except Exception as e:
        print("error", e)
        return json.dumps({"error": str(e)})


if __name__ == "__main__":
    app.run()
