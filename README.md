# Adding-rules-to-FortiGate-using-FortiAPI

With the parameters specified in use, the hostname is created in FortiGate and after this hostname is included in the group, the created group is included in the specified policy.
<br><br>
<b>Installation</b>
- pip install pyfortiapi
- git clone https://github.com/jsimpso/PyFortiAPI
- python3 PyFortiAPI/setup.py install
- echo "FORTI_USERNAME FORTI_PASSWORD" > CREDENTIAL_FILE_PATH
  
<b>Usage</b>
- python3 fortiapi.py FORTI_IP CREDENTIAL_FILE_PATH POLICY_NAME GROUP_NAME HOST_NAME IP_ADDRESS INCOMING_INTERFACE OUTGOING_INTERFACE

<b>Example</b>
  - python3 fortiapi.py 192.168.123.123 forti_credentials.txt TEST_POLICY TEST_GROUP hostname-1 1.2.3.4 port2 port3
