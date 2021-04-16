from virtualbox import VirtualBox
from virtualbox.library import MachineState
import json
import subprocess


def handle_execute(body):
    res = dict(body)
    if "vmName" in body and "input" in body and len(body) == 3:
        vbox = VirtualBox()
        machine = vbox.find_machine(body["vmName"])
        if machine.state == MachineState.running or machine.state == MachineState.paused:
            process = subprocess.Popen(["VBoxManage", "guestcontrol", body["vmName"],
                                        "run", "--exe", "/bin/sh",
                                        "--username", "ali",
                                        "--password", "123456",
                                       "--wait-stdout",
                                        "--", "sh", "-c", body["input"]],
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            if stdout:
                res.update({"response": stdout.decode("utf-8")})
            else:
                res.update({"response": stderr.decode("utf-8")})
        else:
            raise Exception("Machine is off.")
    else:
        raise Exception("Bad request.")
    return json.dumps(res)
