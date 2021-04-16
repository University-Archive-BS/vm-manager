from virtualbox import VirtualBox
from virtualbox.library import MachineState
import json


def handle_delete(body):
    res = dict(body)
    if "vmName" in body and len(body) == 2:
        vbox = VirtualBox()
        machine = vbox.find_machine(body["vmName"])
        if machine.state == MachineState.powered_off or machine.state == MachineState.aborted:
            machine.remove()
            res.update({"status": "ok"})
        else:
            raise Exception("Machine is running.")
    else:
        raise Exception("Bad request.")
    return json.dumps(res)
