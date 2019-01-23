from pysnmp.hlapi import *
import json
import requests
import time

default_information = '''
Battery Time Remaining (.1.3.6.1.4.1.534.1.2.1)         = bat_remain / 'xupsBatTimeRemaining'       -   Time remaining in seconds on UPS
Battery Status (.1.3.6.1.4.1.534.1.2.5)                 = bat_status / 'xupsBatteryAbmStatus'       -   1 = Battery Charging, 2 = Battery Discharging, 3 = Battery Floating, 4 = Battery Resting, 5 = Unknown State
Battery Capacity (.1.3.6.1.4.1.534.1.2.4)               = bat_capaci / 'xupsBatCapacity'            -   0 to 100 value of percentage available
Input Source (.1.3.6.1.4.1.534.1.3.5)                   = in_source/ 'xupsInputSource'              -   1 to 8, 2 = None, 3 = Primary Utility
Load (.1.3.6.1.4.1.534.1.4.1)                           = tot_load/ 'xupsOutputLoad'                -   0 to 200, Output load in percent of rate capacity
Output Wattage (.1.3.6.1.4.1.534.1.4.4.1.4)             = out_watts/ 'xupsOutputWatts'              -   Total Wattage being outputted
Output Source (.1.3.6.1.4.1.534.1.4.5)                  = out_source/ 'xupsOutputSource'            -   1 to 11, 2 = None, 3 = Normal, 4 = Bypass, 5 = Battery
'''

ups_name = 'name_of_device'
ups_ipv4_ip = '1.1.1.1'

ups_devices = [
    {'name': ups_name, 'ip': ups_ipv4_ip,'bat_remain': 0, 'bat_status': 0, 'bat_capaci': 0, 'in_source': 0, 'tot_load': 0, 'out_watts': 0, 'out_source': 0}
    ]

post_data = False

def get_snmp(device):
    snmp_bat_remain = 'xupsBatTimeRemaining'
    snmp_bat_status = 'xupsBatteryAbmStatus'
    snmp_bat_capaci = 'xupsBatCapacity'
    snmp_in_source = 'xupsInputSource'
    snmp_tot_load = 'xupsOutputLoad'
    snmp_out_watts = 'xupsOutputWatts'
    snmp_out_source = 'xupsOutputSource'
    community = 'public'
    # Perform a SNMP GET
    #error_indication, error_status, error_index, var_binds = cmd_gen.getCmd(
    #    cmdgen.CommunityData(community, mpModel=0), cmdgen.UdpTransportTarget((device, 161)), snmp_bat_remain, snmp_bat_status, snmp_bat_capaci, snmp_in_source, snmp_tot_load, snmp_out_watts, snmp_out_source
    #)
    for (error_indication, error_status, error_index, var_binds) in nextCmd(SnmpEngine(),
        CommunityData(community, mpModel=0),
        UdpTransportTarget((device, 161)),
        ContextData(),
        ObjectType(ObjectIdentity('XUPS-MIB', snmp_bat_remain)),
        ObjectType(ObjectIdentity('XUPS-MIB', snmp_bat_status)),
        ObjectType(ObjectIdentity('XUPS-MIB', snmp_bat_capaci)),
        ObjectType(ObjectIdentity('XUPS-MIB', snmp_in_source)),
        ObjectType(ObjectIdentity('XUPS-MIB', snmp_tot_load)),
        ObjectType(ObjectIdentity('XUPS-MIB', snmp_out_watts)),
        ObjectType(ObjectIdentity('XUPS-MIB', snmp_out_source)),
        lexicographicMode=False):
        
        v_bat_remain = None
        v_bat_status = None
        v_bat_capaci = None
        v_in_source = None
        v_tot_load = None
        v_out_watts = None
        v_out_source = None
        snmp_error = None
        
        if error_indication:                         # Check for SNMP errors
            snmp_error = str(error_indication)
        else:
            if error_status:
                snmp_error = error_status.prettyPrint()
                print(snmp_error)
            else:
                # varBinds are returned as SNMP objects, so convert to integers
                v_bat_remain = int(var_binds[0][1])
                v_bat_status = str(var_binds[1][1])
                v_bat_capaci = int(var_binds[2][1])
                v_in_source = str(var_binds[3][1])
                v_tot_load = int(var_binds[4][1])
                v_out_watts = int(var_binds[5][1])
                v_out_source = str(var_binds[6][1])
    
    return v_bat_remain, v_bat_status, v_bat_capaci, v_in_source, v_tot_load, v_out_watts, v_out_source, snmp_error

def grab_data():
    for i in ups_devices:
        ups_bat_remain, ups_bat_status, ups_bat_capaci, ups_in_source, ups_tot_load, ups_out_watts, ups_out_source, snmp_error = get_snmp(i['ip'])
        i['bat_remain'] = ups_bat_remain
        i['bat_status'] = ups_bat_status
        i['bat_capaci'] = ups_bat_capaci
        i['in_source'] = ups_in_source
        i['tot_load'] = ups_tot_load
        i['out_watts'] = ups_out_watts
        i['out_source'] = ups_out_source

def print_data(single_dataset):
    print('UPS Name: {}'.format(single_dataset['name']))
    print('UPS IP: {}'.format(single_dataset['ip']))
    print('Battery Remaining: {}%'.format(single_dataset['bat_remain']))
    print('Battery Status: {}'.format(single_dataset['bat_status']))
    print('Battery Capacity: {}'.format(single_dataset['bat_capaci']))
    print('Power Input Source: {}'.format(single_dataset['in_source']))
    print('Total UPS Load: {}'.format(single_dataset['tot_load']))
    print('Output Wattage: {}'.format(single_dataset['out_watts']))
    print('Ouput Source: {}'.format(single_dataset['out_source']))

def send_data():
    base_url = 'http://api.something.com/v0'                    # Update to the URL to push data too
    headers = {
        'Content-Type': 'application/json'
        }
    request = []
    for i in ups_devices:
        request.append(i)
    putdata = json.dumps(request)
    puturl = '{0}/UPS/stats'.format(str(base_url))              # Update with the correct path
    response = requests.post(puturl, headers=headers, data=putdata)

while True:
    grab_data()
    send_data()
    #print('=' * 180)
    #print_data(ups_devices[0])
    time.sleep(60)