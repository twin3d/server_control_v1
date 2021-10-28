# Task deskription

This is collaborative prototype of code for python for outsoursing tasks and server control.


Soon ansible will be integrated in our flow, however we need tool for discovering and updating host ip's I propose do a tool which discover proper host IPs on the network. 


# Step 1 Minimal working ping tool
Task is to create python application launched on server control machine which scans in gateway network with intention to find machines where some specific port is open. Client application is also sysemctl launched on client machines. When it is asking on this port host and a control server handshake on this port and if sucsessful, then if server sends a special "ping" commands returns some specific information about the macine such as: prescripted scanner, it's ip, and other information which can be updated however we need.