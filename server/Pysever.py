#!/usr/bin/env python
# -*- coding: utf-8 -*-
from websocket_server import WebsocketServer
import ast
import os
        

def new_client(client, server):
    server.send_message_to_all("New client has joined")

def message_received(client, server, message):
    global data
    dic = ast.literal_eval(message)
    if dic["x"] is not None:
        data = str(dic["x"])+" "+str(dic["y"])
        server.send_message_to_all(data)
    else:
        print("can not get correct value {}".format(message))
    server.send_message_to_all(data)

def serverMove(port, host):
    server = WebsocketServer(port=port, host=host)
    server.set_fn_new_client(new_client)
    server.set_fn_message_received(message_received)
    server.run_forever()


if __name__ == '__main__':
    data = ""
    #set port and host by yourself
    port = int(os.environ["PORT"])
    # in remote server set 0.0.0.0
    host = '0.0.0.0'

    serverMove(port, host)
