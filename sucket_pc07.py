import time, math, sys, socket, threading, os, cPickle
import pygame
import Queue
from collections import deque
from pygame.locals import *
from threading import Thread

# TODO

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, 'data')

sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("192.168.1.82",27005))
sock.listen(5)
print "listening"
c,addr=sock.accept()
print "got connection from ",addr

class image_data():
    def __init__(self):
        self.data_queue = Queue.LifoQueue(10000000)
        self.stream_queue = deque()
        self.pickles_decoded_count = 0
        self.listner_messages_count = 0
        self.listner_data_amount = 0
        self.pickle_decode_time = 0
        self.time_begin = 0
        self.frametime = 0
        self.latest_data = []
        self.finished = False
        self.azimuth = 0
        self.pitch = 0
        self.magnitude = 0
        self.x_pos = 0
        self.y_pos = 0


image = image_data()
image.time_begin = time.time()

def listener():
    while not image.finished:
        reply = c.recv(4096)
        if reply:
            image.stream_queue.append(reply)
            image.listner_messages_count += 1
            image.listner_data_amount += len(reply)
        if not reply:
            image.finished = True

    time_end = time.time()
    c.close()
    sock.close()
    time_taken = time_end - image.time_begin
    print "replies taken", image.listner_messages_count
    print "amount", image.listner_data_amount
    print "time", time_taken
    print "speed", image.listner_data_amount/(time_taken*1.0)

def stream_decoder():
    decoder_going = True
    # time.sleep(1)
    while decoder_going:

        while image.pickles_decoded_count < image.listner_messages_count:
            time_begin = time.time()
            stream_part = image.stream_queue.popleft()
            while not "STOP" in stream_part: # part has no comlete pickle
                stream_part += image.stream_queue.popleft()
            while "STOP" in stream_part:
                data_parts = stream_part.partition("STOP")
                try:
                    data = cPickle.loads(data_parts[0])
                    stream_part = data_parts[2]
                    image.pickles_decoded_count += 1
                except:
                    print "failing pickle"

            image.data_queue.put(data)
            image.latest_data = data
            image.pickle_decode_time = time.time() - time_begin

def worker():

    #initialize and setup screen
    pygame.init()
    screen = pygame.display.set_mode((1000, 480), 0, 32)

    back_color = (250,100,100)

    #create text surfaces
    font = pygame.font.Font(os.path.join(data_dir, 'vgafix.fon'), 14)

    # xpos_text = ""
    # ypos_text = ""
    # magnitude_text = ""

    cursor = pygame.Surface((5,5))
    cursor.fill((0,0,0))

    # time.sleep(1)

    print "worker on"
    going = True
    while going:

        frametime_begin = time.time()

        for event in pygame.event.get():
            if event.type == QUIT:
                going = False
                image.finished = True
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                going = False
                image.finished = True

        azimuth = image.latest_data[0][0]
        pitch = image.latest_data[0][1]
        magnitude = image.latest_data[1][1]

        image.magnitude = magnitude

        x_pos = ((azimuth+math.pi)/(2*math.pi)) # 0 to 1
        image.x_pos = x_pos * screen.get_width()
        
        y_pos = pitch + (math.pi/2.0) # 0 up, pi down
        y_pos = y_pos / math.pi # 0 up, 1 down
        y_pos = (y_pos - (1.0/4.0)) / (2.0/4.0) # 0 at 45deg up, 1 at 45deg down
        image.y_pos = int(y_pos * screen.get_height())

        # mag_x = mag[0] # phone side-side
        # mag_y = mag[1] # phone top-bottom
        # mag_z = mag[2] # phone front-back
        # azimuth = pos[0] # pi -pi, 0 = norr
        # pitch = pos[1] # pi/2 -pi/2, negativ uppat, positiv nerat, 0 = horisontell
        # roll = pos[2] # pi -pi, positiv medsols, negativ motsols, 0 = horisontell

        magnitude_text = "Mag " + str(magnitude)
        streamsize_text = "Stream " + str(len(image.stream_queue))
        datasize_text = "Data " + str(image.data_queue.qsize())
        dectime_text = "Decode time " + str(image.pickle_decode_time)
        frametime_text = "Frametime " + str(image.frametime)

        streamsize_text_surface = font.render(streamsize_text, False, (128,128,128))
        datasize_text_surface = font.render(datasize_text, False, (128,128,128))
        mag_text_surface = font.render(magnitude_text, False, (128,128,128))
        dectime_surface = font.render(dectime_text, False, (128,128,128))
        frametime_surface = font.render(frametime_text, False, (128,128,128))

        #render stuff to screen
        screen.fill(back_color)
        screen.blit(streamsize_text_surface, (0,0))
        screen.blit(datasize_text_surface, (0,20))
        screen.blit(mag_text_surface, (0,40))
        screen.blit(dectime_surface, (0,60))
        screen.blit(frametime_surface, (0,80))
        screen.blit(cursor, (image.x_pos, image.y_pos))
        pygame.display.flip()

        image.frametime = time.time() - frametime_begin


    # time.sleep(.2)
    print "pickles found:", image.pickles_decoded_count



if __name__ == '__main__':
    Thread(target = listener).start()
    Thread(target = stream_decoder).start()
    Thread(target = worker).start()
    # main()