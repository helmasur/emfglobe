import android, time, math, sys, socket, cPickle
droid = android.Android()

# TODO
 
droid.startSensingTimed(1, 1)

sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("192.168.1.82",27005))

def main():


    amount = 0
    posts = 0
    for x in range(10):

        # msg = str(x)
        # msg += " "
        # sock.send("x")

        # time.sleep(.01)

        #read sensors
        data=[]
        pos = droid.sensorsReadOrientation().result
        mag = droid.sensorsReadMagnetometer().result

        if pos[0] != None and mag[0] != None:
            for x in range(len(pos)):
                pos[x] = round(pos[x]*1.0, 5)
            data.append(pos)
            data.append(mag)
            # data.append("end")
            data_pickled = cPickle.dumps(data,0) #the number is for protocol version, 0 is the original ASCII protocol, 1 is the old binary format, 2 was introduced in Python 2.3. It provides much more efficient pickling of new-style classes.
            data_pickled += "STOP"
            # print data_pickled
            # mag_pickled = pickle.dumps(mag,2)

            #send data
            sock.send(data_pickled)
            amount += len(data_pickled)
            posts += 1
            with open("posts.txt", "w") as text_file:
                text_file.write("Posts: %s " % posts)
            # text_file = open("posts.txt", "w")
            # text_file.write(" Posts: %s" % posts)

            # sock.send(mag_pickled)

        

        # time.sleep(.05)
    # text_file.close()
    print "amount", amount
    print "posts", posts
    sock.close
    droid.stopSensing()


if __name__ == '__main__':
    main()