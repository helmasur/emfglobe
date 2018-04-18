import time, math, sys, socket

# TODO

 
sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("192.168.1.82",12345))
sock.listen(5)
print "listening"
c,addr=sock.accept()
print "got connection from ",addr


def main():

	count = 0
	amount = 0
	time_begin = time.time()
	time_taken = 0
	while True:
		# print "will sleep"
		# time.sleep(1)
		# print "taking reply"
		reply = c.recv(4096)
		if reply:
	  		# print "took reply"
			# print "length", len(reply)
			# print reply
			amount += len(reply)
	  		count += 1
	 	if not reply:
	  		# print "silence"
	  		time_end = time.time()
	  		time_taken = time_end - time_begin
	  		time_taken *= 1.0
	  		break

	print "replies taken", count
	print "amount", amount
	print "time", time_taken
	print "speed", amount/time_taken

	
	c.close()
	sock.close()


if __name__ == '__main__':
    main()