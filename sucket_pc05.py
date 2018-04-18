import time, math, sys, socket, pickle, threading, os
import pygame
from pygame.locals import *
from threading import Thread

# TODO

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, 'data')

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
        self.data=[]

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

    #initialize and setup screen
    pygame.init()
    screen = pygame.display.set_mode((1000, 480), 0, 32)
    screen.fill ((100, 100, 100))

    #Create The Backgound
    # background = pygame.Surface(screen.get_size())
    # background = background.convert()
    back_color = (250,100,100)
    # background.fill(back_color)

    #Display The Background
    # screen.blit(background, (0, 0))
    screen.fill(back_color)
    pygame.display.flip()

    #create text surfaces
    font = pygame.font.Font(os.path.join(data_dir, 'vgafix.fon'), 14)

    text = ""
    going = True

    time.sleep(1)
    print "worker on"
    while going:

        text_surface = font.render(text, False, (128,128,128))

        #render stuff to screen
        screen.fill(back_color)
        screen.blit(text_surface, (0,0))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == QUIT:
                going = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                going = False

        data_parts = image.input.partition("STOP")
        if data_parts[1] == "STOP":
            image.pickles.append(data_parts[0])
            image.input = data_parts[2]
            data = pickle.loads(data_parts[0])
            image.data.append(data)
            text = str(data)
        # elif image.finished: break


    # print "input", image.input
    time.sleep(.2)
    print "pickles found:", len(image.pickles)



if __name__ == '__main__':
    Thread(target = listener).start()
    Thread(target = worker).start()
    # main()