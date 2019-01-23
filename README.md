## Repository for APC UPS Scripts
### Going to use this repository for bugs & feature requests.
To report a bug or feature request, we will use the Issues option, and create a new issue for each bug or feature request.

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