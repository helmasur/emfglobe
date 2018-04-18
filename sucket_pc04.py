import time, math, sys, socket, pickle, threading
from threading import Thread

# TODO

 
sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("192.168.1.82",27000))
sock.listen(5)
print "listening"
c,addr=sock.accept()
print "got connection from ",addr

class image_data():
	def __init__(self):
		self.input = ""
		self.pickles = []
		self.finished = False

image = image_data()


def listener():


	count = 0
	amount = 0
	time_begin = time.time()
	time_taken = 0
	while True:
		# print "will sleep"
		# time.sleep(.001)
		# print "taking reply"
		reply = c.recv(4096)
		if reply:
	  		# print "took reply"
			# print "length", len(reply)
			amount += len(reply)
			# reply = pickle.loads(reply)
			image.input += reply
	  		count += 1
	 	if not reply:
	  		# print "silence"
	  		time_end = time.time()
	  		time_taken = time_end - time_begin
	  		time_taken *= 1.0
	  		image.finished = True
	  		break

	# print image.input
	print "replies taken", count
	print "amount", amount
	print "time", time_taken
	print "speed", amount/time_taken


	
	c.close()
	sock.close()


def worker():
	time.sleep(1)
	print "worker on"
	while True:
		data_parts = image.input.partition("STOP")
		if data_parts[1] == "STOP":
			image.pickles.append(data_parts[0])
			image.input = data_parts[2]
		else:
			if image.finished == True: break
	# print "input", image.input
	time.sleep(.2)
	print "pickles found:", len(image.pickles)



if __name__ == '__main__':
	Thread(target = listener).start()
	Thread(target = worker).start()
    # main()