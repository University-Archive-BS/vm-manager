from virtualbox import VirtualBox
from virtualbox.library import MachineState
import json
import subprocess


def handle_setting(body):
    res = dict(body)
    if "vmName" in body and "cpu" in body and "ram" in body and len(body) == 4:
        vbox = VirtualBox()
        machine = vbox.find_machine(body["vmName"])
        if machine.state == MachineState.powered_off or machine.state == MachineState.aborted:
            process = subprocess.Popen(["VBoxManage", "modifyvm", body["vmName"],
                                        "--cpus", str(body["cpu"]),
                                        "--memory", str(body["ram"])],
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            res.update({"status": "ok"})
        else:
            raise Exception("vm is running.")
    else:
        raise Exception("Bad request.")
    return json.dumps(res)
