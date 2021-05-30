"""

Requirment: Read GPS data from the serial port continuously while processing this data to extract packet data.
This is achieved using pythons threading module. 

A thread is started to continuously read input data byte by byte and append to a global queue.
The main program goes on to processing this data i.e identifying the start of the packet and extracting packet information.

"""

import serial
import threading, multiprocessing
import queue
import time

# Initialize serial port and Baudrate
ser = serial.Serial('/dev/ttyUSB0')
ser.baudrate = 115200


def read_gps_input(inputQueue):
    """
    Read Serial Port data byte by byte and append value to Queue. This is run on a serperate thread.
    Input: Input Queue (Initially Empty Queue)
    Output: No Return
    """

    while True:
        buffer_val = ser.read().hex()
        inputQueue.put(buffer_val)

def process_data(data_queue):
    """
    Process Input Queue data, Identify start of first message and store the message packet in a priority queue
    Input: Data Queue
    Output: Return the Priority Queue with just the packet after verifying checksum
    """

    found_d3 = False
    last_message = ""

    #output_queue = queue.PriorityQueue()
    output_queue = []
    
    while True:

        if data_queue.qsize() > 0:

            queue_char = data_queue.get()

            if found_d3 == True or queue_char == "d3":

                if found_d3 == True:
                    length_byte_one = queue_char
                    length_byte_two = data_queue.get()
                    

                elif queue_char == "d3":
                    
                
                    length_byte_one = data_queue.get()
                    length_byte_two = data_queue.get()
                
                message_length = int(bin(int(length_byte_one, 16)).split('b')[-1].zfill(8)[-2::] + bin(int(length_byte_two, 16)).split('b')[-1].zfill(8), 2)
                
                message_length_with_offset = message_length + 3
                queue_count = 0
                message_list = []
                message_list.append(length_byte_one)
                message_list.append(length_byte_two)

                while queue_count < message_length_with_offset:

                  message_list.append(data_queue.get())
                  queue_count+=1
                  #  if data_queue.get() == "d3":
                  #      print("d3")
                  #  queue_count+=1

                last_message = data_queue.get()

                if last_message == "d3":
                    found_d3 = True
                    message_type = message_list[2] + message_list[3][0]
                    output_queue.append((len(message_list), "".join(message_list)))
                    #print("".join(message_list), int(message_type, 16))
                    yield output_queue

                else:
                    print("Found d3 - {}".format(found_d3))


def start_ublox():
    """
    Main Function to start reading and processing data
    Does not require any input
    """
    inputQueue = queue.Queue()

    inputThread = threading.Thread(target=read_gps_input, args=(inputQueue,), daemon=True)
    inputThread.start()

    output_gen = process_data(inputQueue)

    return output_gen


if __name__ == "__main__":

    start_ublox()

