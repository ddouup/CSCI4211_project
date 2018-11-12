CSCI4211_project

Name: Daihui DOU
Email: dou00005@umn.edu
Stu ID: 5514178

Run server:
python3 local_server.py default_local 5352 default.dat server.dat

Run client:
python3 client.py PC1 127.0.0.1 5352

For phase 1, I implemented the multi-thread local_server listen on "0.0.0.0". After running local_server and then client, user could DNS query in client in the format: <ID, hostname, I/R>. The client will end when ‘q’ is entered. Up to 5 clients could access the server at the same time.

The local_server right now read the default.dat as its DNS map. If the query is in the map, the server returns <0x00, Server_ID, IP>. If not, the server returns <0xFF, Server_ID, ”Host not found”>. If the format is invalid, the server returns <0xEE, ID, “Invalid format”>.

The server.dat is currently no use but it is needed in the parameter.