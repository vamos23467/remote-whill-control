#!/usr/bin/env python
# -*- coding: utf-8 -*-
import serial
import time
import websocket

#set url and serial port
WHILLPORT = ""
SERVER_URL = ""

#get serial value from arduino
class GetData(object):

    def __init__(self):
        self.port = WHILLPORT
        self.baudrate = 115200
        print("Open Port")
        try:
            self.ser = serial.Serial(self.port, self.baudrate, timeout=1)
        except:
            print("can not connect serial")

    def get_data(self):
        value = self.ser.readline()
        value = value.decode()
        value = value.split(",") 
        return value

    def ser_close(self):
        print("Close Port")
        self.ser.close()


#send joycon data xy value
def socket_send(ws, x, y):
    json_data = {}
    json_data["x"] = x
    json_data["y"] = y
    ws.send(str(json_data))
    print(json_data)


def main() :
    global ws
    global data
    x, y = 0, 0

    ws = websocket.create_connection(SERVER_URL)
    data = GetData()

    # get data from arduino and send to server
    while True:
        try:
            receive = data.get_data()
            if receive[0] and receive[1]:
                x = int(receive[0])
                y = int(receive[1])
                socket_send(ws, x, y)
        except KeyboardInterrupt:
            data.ser_close()
            ws.close()
            break
        time.sleep(0.01)

if __name__ == '__main__':
    try:
        main()
        data.ser_close()
        ws.close()
    except:
        print("error occured")
