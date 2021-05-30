import serial
from collections import deque
import multiprocessing, threading

ser = serial.Serial('/dev/ttyUSB0')
ser.baudrate = 115200

q = deque()

def read_data():

    while True:
        buffer = ser.readline().hex()

        while i < len(buffer):
            q.append(buffer[i: i+2])
            i+=2
        write_data(q)

def read_2():

    if ser.inWaiting() > 0:
        buffer = ser.read(ser.inWaiting()).hex()
        print(data)

while True:
    read_2()

        
def write_data(q):

    print(len(q))

#def process_data():
        

#while True:
#
#    #read_data()
#    #p1 = multiprocessing.Process(target=read_data)
#    #p2 = multiprocessing.Process(target=write_data)
#    t1 = threading.Thread(target=read_data)
#    t2 = threading.Thread(target=write_data)
#
#
#    t1.start()
#    t2.start()
#    t2.join()
#    #t1.join()
#    #t2.start()

t1 = threading.Thread(target=read_data)
t1.start()


