import android, time, math, sys, socket
droid = android.Android()

# TODO
 
droid.startSensingTimed(1, 1)

sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("192.168.1.82",12345))

def main():

	for x in range(1000000):

		# msg = str(x)
		# msg += " "
		sock.send("x")

		#read sensors
		# pos = droid.sensorsReadOrientation().result
		# mag = droid.sensorsReadMagnetometer().result

		# time_this("sensors read")

		#store data and remove some decimals
		# mag_x = mag[0] # phone side-side
		# mag_y = mag[1] # phone top-bottom
		# mag_z = mag[2] # phone front-back
		# mag_x2 = mag[0] * -1 # phone side-side
		# mag_y2 = mag[1] * -1 # phone top-bottom
		# mag_z2 = mag[2] * -1 # phone front-back
		# azimuth = pos[0] # pi -pi, 0 = norr
		# pitch = pos[1] # pi/2 -pi/2, negativ uppat, positiv nerat, 0 = horisontell
		# roll = pos[2] # pi -pi, positiv medsols, negativ motsols, 0 = horisontell

			# if event["data"]["key"] == "4":
				# sys.exit()

		# time.sleep(.05)
	sock.close
	droid.stopSensing()


if __name__ == '__main__':
    main()