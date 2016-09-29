import socket
import sys
import addressbook_pb2
from protobuf_to_dict import protobuf_to_dict
 
HOST = ''   # Symbolic name, meaning all available interfaces
PORT = 8888 # Arbitrary non-privileged port

# Iterates though all people in the AddressBook and prints info about them.
def ListPeople(address_book):
  for person in address_book.person:
    print "Person ID:", person.id
    print "  Name:", person.name
    if person.HasField('email'):
      print "  E-mail address:", person.email

    for phone_number in person.phone:
      if phone_number.type == addressbook_pb2.Person.MOBILE:
        print "  Mobile phone #:",
      elif phone_number.type == addressbook_pb2.Person.HOME:
        print "  Home phone #:",
      elif phone_number.type == addressbook_pb2.Person.WORK:
        print "  Work phone #:",
      print phone_number.number

 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'
 
#Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
     
print 'Socket bind complete'
 
#Start listening on socket
s.listen(10)
print 'Socket now listening'
 
#now keep talking with the client
while 1:
    #wait to accept a connection - blocking call
    conn, addr = s.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])
    while True:   
        #Receiving from client
        data = conn.recv(1024)
        reply = 'OK...\n' 
        if not data: 
            break
        address_book = addressbook_pb2.AddressBook()
        address_book.ParseFromString(data)
	print protobuf_to_dict(address_book)
        conn.sendall(reply)
     
    #came out of loop
    conn.close()
    print "closing Connection"
     
s.close()
