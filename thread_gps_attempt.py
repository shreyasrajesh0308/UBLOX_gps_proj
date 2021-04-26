import serial
import threading, multiprocessing
import queue
import time

ser = serial.Serial('/dev/ttyUSB0')
ser.baudrate = 115200

def read_gps_input(inputQueue):

    while True:
        buffer_val= ser.read().hex()
        inputQueue.put(buffer_val)

def process_data(text_list):

    i = 0
    d3_count = 0
    found_d3 = False

    
    while True:

        if text_list.qsize() > 0:

     
        #print(text_list)


            queue_char = text_list.get()
            if found_d3 == True:

                length_byte_one = queue_char
                length_byte_two = text_list.get()
                    
                message_length = int(bin(int(length_byte_one, 16)).split('b')[-1].zfill(8)[-2::] + bin(int(length_byte_two, 16)).split('b')[-1].zfill(8), 2)
                #print(d3_count, message_length)
                
                message_length_with_offset = message_length + 3
                queue_count = 0
                message_list = []
                while queue_count < message_length_with_offset + 1:

                  message_list.append(text_list.get())
                  queue_count+=1
                  #  if text_list.get() == "d3":
                  #      print("d3")
                  #  queue_count+=1

                if message_list[-1] == "d3":
                    found_d3 = True
                    message_type = message_list[0] + message_list[1][0]
                    print(message_list[-1], int(message_type, 16))

                else:
                    print("D3count - {}, found d3 - {}".format(d3_count, found_d3))



            else:
                if queue_char == "d3":
                    
                    d3_count +=1
                
                    length_byte_one = text_list.get()
                    length_byte_two = text_list.get()
                    
                    message_length = int(bin(int(length_byte_one, 16)).split('b')[-1].zfill(8)[-2::] + bin(int(length_byte_two, 16)).split('b')[-1].zfill(8), 2)
                    #print(d3_count, message_length)
                    
                    message_length_with_offset = message_length + 3
                    queue_count = 0
                    message_list = []
                    while queue_count < message_length_with_offset + 1:

                      message_list.append(text_list.get())
                      queue_count+=1
                      #  if text_list.get() == "d3":
                      #      print("d3")
                      #  queue_count+=1

                    if message_list[-1] == "d3":
                        found_d3 = True
                        message_type = message_list[0] + message_list[1][0]
                        print(message_list[-1], int(message_type, 16))

                    else:
                        print("D3count - {}, found d3 - {}".format(d3_count, found_d3))


def main():

    inputQueue = queue.Queue()

    inputThread = threading.Thread(target=read_gps_input, args=(inputQueue,), daemon=True)
    inputThread.start()

    process_data(inputQueue)


if __name__ == "__main__":

    main()

