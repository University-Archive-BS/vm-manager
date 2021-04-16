from virtualbox import VirtualBox
from virtualbox.library import MachineState, CloneOptions
import json


def handle_clone(body):
    res = dict(body)
    if "sourceVmName" in body and "destVmName" in body and len(body) == 3:
        vbox = VirtualBox()
        sourceVm = vbox.find_machine(body["sourceVmName"])
        for m in vbox.machines:
            if body["destVmName"] == m.name:
                raise Exception("destVm is available.")
        if sourceVm.state == MachineState.powered_off or sourceVm.state == MachineState.aborted:
            sourceVm.clone(name=body["destVmName"], options=[
                           CloneOptions.keep_natma_cs])
            res.update({"status": "ok"})
        else:
            raise Exception("sourceVm is running.")
    else:
        raise Exception("Bad request.")
    return json.dumps(res)
