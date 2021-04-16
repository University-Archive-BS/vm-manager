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

users = [
    User("user1", 123456, "sle3s@knref"),
    User("admin", 123456, "dkjlv@sef34")
]


@app.route('/', methods=["GET"])
def req():
    try:
        body = json.loads(request.data)
        headers = request.headers
        # auth_token = headers["Authorization"]

        if "command" in body:
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
        else:
            raise Exception("Sorry")
    except Exception as e:
        print("error", e)
        return json.dumps({"error": str(e)})


if __name__ == "__main__":
    app.run()
