from virtualbox import VirtualBox, Session
from virtualbox.library import MachineState, LockType
import json


def handle_power(body):
    res = dict(body)
    if "vmName" in body and len(body) == 2:
        vbox = VirtualBox()
        machine = vbox.find_machine(body["vmName"])
        session = Session()
        if machine.state == MachineState.powered_off or machine.state == MachineState.aborted:
            progress = machine.launch_vm_process(session, "gui", [])
            progress.wait_for_completion()
            res.update({"status": "powering on"})
        elif machine.state == MachineState.running or machine.state == MachineState.paused:
            machine.lock_machine(session, LockType(1))
            progress = session.console.power_down()
            # progress = session.console.power_button()
            res.update({"status": "powering off"})
    else:
        raise Exception("Bad request.")
    return json.dumps(res)
