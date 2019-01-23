import json
import subprocess
import time

dataset = {}

def get_apc_stats():
    filename = 'apc_output.txt'
    command = 'apcaccess'
    f = open(filename, 'w')
    subprocess.call([command], stdout=f)
    
    global dataset
    with open(filename) as f:
        for line in f:
            name,value = line.split(":", 1)
            name = name.strip()
            value = value.strip()
            value = value.strip('\n')
            dataset[name] = str(value)


def main():
    get_apc_stats()
    while dataset['STATUS'] == 'ONBATT':
        print('#' * 60)
        print('Status: {}'.format(str(dataset['STATUS'])))
        print('Load: {}'.format(str(dataset['LOADPCT'])))
        print('Time Remaining: {}'.format(str(dataset['TIMELEFT'])))
        print('Battery Remaining: {}'.format(str(dataset['BCHARGE'])))
        print('Transferred to Battery: {}'.format(str(dataset['XONBATT'])))
        time.sleep(60)
        get_apc_stats()
    while dataset['STATUS'] != 'ONBATT':
        print('#' * 60)
        print('Status: {}'.format(str(dataset['STATUS'])))
        print('Load: {}'.format(str(dataset['LOADPCT'])))
        print('Time Remaining: {}'.format(str(dataset['TIMELEFT'])))
        print('Battery Remaining: {}'.format(str(dataset['BCHARGE'])))
        print('Transferred to Main: {}'.format(str(dataset['XOFFBATT'])))
        time.sleep(60)
        get_apc_stats()
main()