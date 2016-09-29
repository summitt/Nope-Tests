import sys
import subprocess


def preIntercept(input, isC2S):
   if not isC2S:
     return input
   print "Starting PreIntercept"
   p = subprocess.Popen(['/Users/ascetik/NopeTests/protoc', '--decode=tutorial.AddressBook', './addressbook.proto'], 
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
   p = subprocess.Popen(['/Users/ascetik/NopeTests/protoc', '--encode=tutorial.AddressBook', './addressbook.proto'], 
     stdout=subprocess.PIPE,
     stderr=subprocess.PIPE,
     stdin=subprocess.PIPE)
   out, err = p.communicate(input)
   return bytearray(out)


