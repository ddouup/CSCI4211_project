# CSCI4211_project
## Packages needed:
* socket
* _thread
* sys
* os

## Server
Run:
```
python3 domain_server.py org 5354 org.dat
python3 domain_server.py gov 5355 gov.dat
python3 domain_server.py com 5356 com.dat
python3 root_server.py ROOT 5353 server.dat
python3 local_server.py default_local 5352 default.dat
```

## Client
Run:
```
python3 client.py PC1 127.0.0.1 5352
```