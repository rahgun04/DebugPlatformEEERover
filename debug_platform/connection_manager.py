
from enum import Enum
import socket
import asyncio
import asyncudp
import time, _thread
BUFFER_SIZE = 1024
HEADER_LEN = 4




class PacketType(Enum):
    DRIVE = 1
    HANDSHAKE = 2
    AGE = 3
    MAGNET = 4
    NAME = 5

class client_connection_manager():

    def __init__(self):
        self.UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.connection_state = False
        self.serverAddressPort = []
        self.dis_callback = None
        self.con_callback = None
        self.recieved_packet_callback = None

    def disconnect_callback_assign(self, callback):
        self.dis_callback = callback;

    def connect_callback_assign(self, callback):
        self.con_callback = callback;

    def recieved_packet_callback_assign(self, callback):
        self.recieved_packet_callback = callback;

    #async def __make_sock(self, dest):
    #    self.sock = await asyncudp.create_socket(remote_addr=dest)





    def connect(self, dest):
        self.UDPClientSocket.settimeout(5);
        self.serverAddressPort = dest
        try:
            #asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
            #asyncio.run(self.__make_sock(dest))

            #self.UDPClientSocket.sendto(bytearray("init_connection", encoding = "ascii"), self.serverAddressPort)
            self.send_packet(2, bytearray([255]))
        except Exception as e:
            print(e)
            print("Failed To connect")
            return False
        self.connection_state = True
        if self.con_callback != None:
            self.con_callback()
        try:
            _thread.start_new_thread(self.__recieve_thread, ())
        except:
            print("Failed to start thread")
        return True

    def __send_bytes(self, bytes):
        try:
            self.UDPClientSocket.sendto(bytes, self.serverAddressPort)
            #self.sock.sendto(bytes)
        except Exception as e:
            print(e)
            print("Failed To Send")
            return False
        return True

    def send_packet(self, type, data):
        length = len(data)
        header = bytearray([type]) + length.to_bytes(2, "big")  + bytearray([0])
        self.__send_bytes((header + bytearray(data)))

    def __recieve_thread(self):
        while True:
            try:
                data_raw, addr = self.UDPClientSocket.recvfrom(1024)
                if self.recieved_packet_callback != None:
                    self.recieved_packet_callback(data_raw[0], data_raw[4:])
            except Exception as e:
                print("No Data to recv")
                print(e)



