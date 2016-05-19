import time
import itertools

import informers
from device import Device

device = Device()

device.print_rows("Starting", "informer")

informer_functions = []

for (name, function) in informers.__dict__.items():
    if name.endswith('informer'):
        informer_functions.append(function)

time.sleep(5)
device.print_rows("Hi!", "My name is Box.")
time.sleep(7)
device.print_rows("Nice to meet", "you there!")
time.sleep(7)

for informer in itertools.cycle(informer_functions):
    try:
        informer(device)
    except Exception as error:
        print('Problem with', informer, error)
        continue
    time.sleep(7)
