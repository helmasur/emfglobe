import android, time, math, sys, socket, pickle
droid = android.Android()

# TODO
 
droid.startSensingTimed(1, 1)

sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("192.168.1.82",27000))

def main():

    amount = 0
    for x in range(300):

        # msg = str(x)
        # msg += " "
        # sock.send("x")

        time.sleep(.1)

        #read sensors
        data=[]
        pos = droid.sensorsReadOrientation().result
        mag = droid.sensorsReadMagnetometer().result

        if pos[0] != None or mag[0] != None:
            for x in range(len(pos)):
                pos[x] = round(pos[x]*1.0, 5)
            data.append(pos)
            data.append(mag)
            # data.append("end")
            data_pickled = pickle.dumps(data,0) #the number is for protocol version, 0 is the original ASCII protocol, 1 is the old binary format, 2 was introduced in Python 2.3. It provides much more efficient pickling of new-style classes.
            data_pickled += "STOP"
            # print data_pickled
            # mag_pickled = pickle.dumps(mag,2)

            #send data
            amount += len(data_pickled)
            sock.send(data_pickled)
            # sock.send(mag_pickled)

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

        # time.sleep(.05)
    print "amount", amount
    sock.close
    droid.stopSensing()


if __name__ == '__main__':
    main()