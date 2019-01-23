## Repository for APC UPS Scripts

#### snmp_ups.py: 
- Will us SNMP to get data from SNMP
- Once it has all the data will post it to an API endpoint to be put into a database
- Supports multiple devices

#### apc.py
- This requires 'apcusbd'
- Puts the output of 'apcaccess' into a text file
- Reads the data from text file
- Prints info to screen
- Will make it like snmp_ups.py where it will post the data to an API endpoint to be stored into a database