#!/usr/bin/env python
# -*- coding: utf-8 -*-
from whill import ComWHILL
import time
import threading
import websocket
import serial

#set whill serial port and server host and arduino port
WHILL_PORT=""
SERVER_HOST=""
ARDUINO_PORT=""

#get serial value from arduino
class GetData(object):

    def __init__(self):
        self.port = ARDUINO_PORT
        self.baudrate = 9600
        print("Open Port")
        try:
            self.ser = serial.Serial(self.port, self.baudrate, timeout=1)
        except:
            print("can not connect serial")

    def get_data(self):
        value = self.ser.readline()
        value = value.decode()
        return int(value)
        

    def ser_close(self):
        print("Close Port")
        self.ser.close()



def isint(s):
    try:
        int(s, 10)
    except ValueError:
        return False
    else:
        return True

def on_message(ws, message):
    global x,y
    dic = message.split()

    if dic[1] is not None and isint(dic[0]):
        x = int(dic[0])
        y = int(dic[1])


def on_error(ws, error):
    print(error)
    print("error occured")
    # not to shutdown connection, restart when errored
    restart_websocket()
    

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

def restart_websocket():
    try:
        websocket.enableTrace(True)
        wsapp = websocket.WebSocketApp(SERVER_HOST, on_message=on_message, on_error=on_error,on_close=on_close)
        wsapp.daemon = True
        wsapp.run_forever()
    except:
        print("restart failed")

def server_move():
    try:
        websocket.enableTrace(False)
        wsapp = websocket.WebSocketApp(SERVER_HOST, on_message=on_message, on_error=on_error,on_close=on_close)
        wsapp.daemon = True
        wsapp.run_forever()
    except:
        print("exceptoion occured")
        restart_websocket()


if __name__ == "__main__":
    #set first WHILL xy 0
    x = 0
    y = 0
    mode_flag = 1

    data = GetData()
    whill = ComWHILL(WHILL_PORT)

    #receive server data and update xy value
    thread_1 = threading.Thread(target=server_move)
    thread_1.start()

    #move whill using send_joystick method
    # x: -100~100 back or front
    # y: -100~100 left or right
    while True:
        try:
            mode_flag = data.get_data()
            #conrol in remote or wheelchair user 
            if mode_flag:
                #move WHILL by received data
                whill.send_joystick(int(x * 30), int(-y * 30))
        except KeyboardInterrupt:
            data.ser_close()
            break

        time.sleep(0.1)
