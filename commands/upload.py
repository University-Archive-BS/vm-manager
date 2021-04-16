from virtualbox import VirtualBox
from virtualbox.library import MachineState
import json
import subprocess


def handle_upload(body):
    res = dict(body)
    if "vmName" in body and "file" in body and "target_path" in body and len(body) == 4:
        vbox = VirtualBox()
        machine = vbox.find_machine(body["vmName"])
        if machine.state == MachineState.running or machine.state == MachineState.paused:
            process = subprocess.Popen(["VBoxManage", "guestcontrol", body["vmName"], "copyto",
                                        "--target-directory", body["target_path"], body["file"],
                                        "--username", "ali", "--password", "123456"],
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            if stderr:
                res.update({"response": stderr.decode("utf-8")})
            else:
                res.update({"response": "ok"})
        else:
            raise Exception("Machine is off.")
    else:
        raise Exception("Bad request.")
    return json.dumps(res)
