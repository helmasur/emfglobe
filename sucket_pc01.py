import time, math, sys, socket

# TODO

 
sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("192.168.1.82",12345))
sock.listen(5)
c,addr=sock.accept()
print "got connection from ",addr
while True:
  reply = c.recv(4096)
  print reply
  # c.close()




sock.close
droid.stopSensing()


