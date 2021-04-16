from virtualbox import VirtualBox
from virtualbox.library import MachineState
import json
import subprocess


def handle_transfer(body):
    res = dict(body)
    if "originVM" in body and "originPath" in body and "destVM" in body and "destPath" in body and len(body) == 5:
        vbox = VirtualBox()
        originVM = vbox.find_machine(body["originVM"])
        destVM = vbox.find_machine(body["destVM"])
        if (originVM.state == MachineState.running or originVM.state == MachineState.paused) and (destVM.state == MachineState.running or destVM.state == MachineState.paused):
            process = subprocess.Popen(["VBoxManage", "guestcontrol", body["originVM"], "copyfrom",
                                        "--target-directory", "C:/cc-vms", body["originPath"],
                                        "--username", "ali", "--password", "123456"],
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()

            process_ = subprocess.Popen(["VBoxManage", "guestcontrol", body["destVM"], "copyto",
                                        "--target-directory", body["destPath"], "C:/cc-vms/" + body["originPath"].rsplit('/', 1)[1],
                                         "--username", "ali", "--password", "123456"],
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE)
            stdout_, stderr_ = process_.communicate()
            if stderr:
                res.update({"response": stderr.decode("utf-8")})
            elif stderr_:
                res.update({"response": stderr_.decode("utf-8")})
            else:
                res.update({"response": "ok"})
        else:
            raise Exception("Machine is off.")
    else:
        raise Exception("Bad request.")
    return json.dumps(res)
