CSCI4211_project

Name: Daihui DOU
Email: dou00005@umn.edu
Stu ID: 5514178

Packages used:
* socket
* _thread
* sys
* os

Run server:
python3 domain_server.py org 5354 org.dat
python3 domain_server.py gov 5355 gov.dat
python3 domain_server.py com 5356 com.dat
python3 root_server.py ROOT 5353 server.dat
python3 local_server.py default_local 5352 default.dat

Run client:
python3 client.py PC1 127.0.0.1 5352


Make sure to run domain_server.py three times for different top_level DNS servers(org, gov, com).

The IP and port of Root DNS server is hard-coded in local_server.py.

All the log files are appended each time the programs run. Please delete to reset.

The default_local.log, PC1.log, PC2.log and mapping.log in my submission are generated by initializing local_server with default.dat provided by TA, and using the sample user input.