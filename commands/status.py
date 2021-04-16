from virtualbox import VirtualBox
from virtualbox.library import MachineState
import json


def get_machine_state(state):
    res = "off"
    if state == MachineState.powered_off:
        res = "off"
    elif state == MachineState.running or state == MachineState.paused:
        res = "on"
    elif state == MachineState.starting:
        res = "powering on"
    elif state == MachineState.stopping:
        res = "powering off"
    return res


def handle_status(body):
    res = dict(body)
    if len(body) == 1:
        details = []
        vbox = VirtualBox()
        for m in vbox.machines:
            state = m.state
            detail = {"vmName": m.name, "status": "off"}
            detail["status"] = get_machine_state(state)
            details.append(detail)
        res.update({"details": details})
    elif "vmName" in body and len(body) == 2:
        vbox = VirtualBox()
        try:
            machine = vbox.find_machine(body["vmName"])
            res.update({"status": get_machine_state(machine.state)})
        except:
            raise Exception("Machine not found.")
    else:
        raise Exception("Bad request.")
    return json.dumps(res)
