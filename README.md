# Nope-Tests

You can use these files to test creating your own protocol decoders in python to convert binary protocols into human readable formates before sending to the interceptor. After modification in the interceptor they will be encoded back into the binary protocol the server is expecting.


Steps:

1. Start the simple simpleSocket.py

 ```
 python ./simpleSocket.py
 ```
2. Start burp and the Nope proxy. Set Server address to local host, server port to 8888 and listen port to 8889.
 ![](http://i.imgur.com/oqWyLXO.png)
1. Click the enable checkbox from the table.
1. Now send protobuf binary traffic though Nope

 ```
 cat add_file | nc localhost 8889
 ```
1. Notice the traffic should be flowing through the History tab and if you intercept you can see that some of the data is human readable but not all.
 ![](http://i.imgur.com/rCGIJho.png)
 
##Now we need to use the python Mangler to decode the data for use so that it is easier to edit in the interceptor. 
1. copy addressbook.proto to the same folder you ran Burp from.
1. Add the following python code to the python Mangler and update **path2protoc** with your path to the protoc command. Download protoc [here for your distro](https://github.com/google/protobuf/releases).
 ```
 import sys
 import subprocess

 path2protoc=[YOUR PATH 2 PROTOC]
 def preIntercept(input, isC2S):
   if not isC2S:
     return input
   print "Starting PreIntercept"
   p = subprocess.Popen([path2protoc + '/protoc', '--decode=tutorial.AddressBook', './addressbook.proto'], 
     stdout=subprocess.PIPE,
     stderr=subprocess.PIPE,
     stdin=subprocess.PIPE)
   out, err = p.communicate(input)
   return bytearray(out)

 def mangle(input, isC2S):
   print "New test"
   return input

 def postIntercept(input, isC2S):
   if not isC2S:
     return input
   print "Post Intercept"
   print input
   p = subprocess.Popen([path2protoc+'/protoc', '--encode=tutorial.AddressBook', './addressbook.proto'], 
     stdout=subprocess.PIPE,
     stderr=subprocess.PIPE,
     stdin=subprocess.PIPE)
   out, err = p.communicate(input)
   return bytearray(out)
 ```
1. Now turn enable the python Mangler on the Nope proxy automation tab.
  ![](http://i.imgur.com/3vPWsV4.png)
1. Turn on intercepting.
1. Repeat step 3 and you should see the decoded protobuf that you can edit before sending to the server.
 ![](http://i.imgur.com/z2e6wpW.png)


##Installing protobufs in python (Unrelated but needed for this tutorial)
Download them here: https://github.com/google/protobuf/releases/download/v3.1.0/protobuf-python-3.1.0.tar.gz
```
wget https://github.com/google/protobuf/releases/download/v3.1.0/protobuf-python-3.1.0.tar.gz
tar xzvf protobuf-python-3.1.0.tar.gz
cd protobuf-3.1.0
./autogen.sh
./configure
make
cd /python
python ./setup.py install
```

