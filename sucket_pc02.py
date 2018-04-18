import time, math, sys, socket

# TODO

 
sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("192.168.1.82",12345))
sock.listen(5)
c,addr=sock.accept()
print "got connection from ",addr


def main():


	run = True
	while run:
	  reply = c.recv(128)
	  print reply
	  if not reply:
	  	print "silence"
	  	run = False
	
	c.close()
	sock.close()


if __name__ == '__main__':
    main()