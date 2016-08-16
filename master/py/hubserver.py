#!/usr/bin/env python
#
# Copyright 2009 Facebook
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
"""Simplified chat demo for websockets.

Authentication, error handling, etc are left as an exercise for the reader :)
"""

import tornado.escape
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket
import tornado.httpclient
import os.path

import time
import json
import base64
import queue
import threading

import requests
from tornado.options import define, options

define("port", default=8888, help="run on the given port", type=int)


class Application(tornado.web.Application):
    def __init__(self):
        self.devices = {}
        self.Devices = dict()

        handlers = [
            (r"/", MainHandler),
            (r"/console", ConsoleHandler),
            (r"/terminal", TerminalHandler),
            (r"/fileproxy", FileProxy),
            (r"/run", RunProxy),
            (r"/stop", StopProxy),
            (r"/proxy", TerminalProxy),
            (r"/check", CheckHandler),
            (r"/device", DeviceHandler),
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
        )
        tornado.web.Application.__init__(self, handlers, **settings)


class TerminalHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        id = self.get_argument("id")
        print(id)
        device = self.application.Devices.get(id)
        if device:
            self.render("terminal.html", id=id)
        else:
            self.write("ID not Existed")


class FileProxy(tornado.web.RequestHandler):
    def post(self):
        print("wwww %s" % self.get_argument("ids", ""))
        ids = self.get_argument("ids", "").split(",")
        print(ids)
        print(self.request.files)
        if not self.request.files:
            self.write("You missed a field")
            return
        file_metas = self.request.files['file'][0]
        filename = file_metas['filename']
        raw = file_metas['body']
        # tmp = open("upload.tmp", 'wb')
        # tmp.write(raw)
        # file = open("upload.tmp", 'rb')
        # chosen_devices = [device for device in self.application.Devices if device.id in ids]
        chosen_devices = [self.application.Devices[id] for id in self.application.Devices if id in ids]
        for device in chosen_devices:
            device.write_message(json.dumps({"cmd":103, "params":{"payload": base64.b64encode(raw).decode(), 'filename': filename}}))

        self.redirect("/")


class RunProxy(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.set_header('Access-Control-Max-Age', 1000)
        self.set_header('Access-Control-Allow-Headers', '*')

    def post(self):
        print(self.request.body)
        data = tornado.escape.json_decode(self.request.body)
        script = data.get("script", "")
        ids = data.get("ids", "")
        print(script, ids)
        chosen_devices = [self.application.Devices[id] for id in self.application.Devices if id in ids]
        for device in chosen_devices:
            device.write_message(json.dumps({"cmd":105, "params":{"script": script}}))
        self.redirect("/")

class StopProxy(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.set_header('Access-Control-Max-Age', 1000)
        self.set_header('Access-Control-Allow-Headers', '*')

    def post(self):
        print(self.request.body)
        data = tornado.escape.json_decode(self.request.body)
        ids = data.get("ids", "")
        print(ids)
        # chosen_devices = [device for device in self.application.Devices if device.id in ids]
        chosen_devices = [self.application.Devices[id] for id in self.application.Devices if id in ids]
        for device in chosen_devices:
            device.write_message(json.dumps({"cmd":107, "params":{}}))
        self.redirect("/")

class TerminalProxy(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self, *args, **kwargs):
        print("connected!!")
        id = self.get_argument("id", "")

        def loop(ws):
            count = 0
            try:
                while True:
                    ws.write_message("I can see your halo %s" % count)
                    time.sleep(2)
                    count = count + 1
            except tornado.websocket.WebSocketClosedError:
                print("The end")

        device = self.application.Devices.get(id)
        self.device = device

        self.register()
        device.write_message(json.dumps({"cmd": 109, "params": {}}))

        # self.proc = threading.Thread(target=loop, args=(self,))
        # self.proc.start()

    def register(self):
        self.device.add_listener(self)

    def unregister(self):
        self.device.remove_listener(self)

    def on_message(self, message):
        self.write_message()

    def on_device_message(self, msg):
        self.write_message(msg)

    def on_close(self):
        self.device.write_message(json.dumps({"cmd": 111, "params": {}}))
        self.unregister()

class DeviceHandler(tornado.websocket.WebSocketHandler):
    decices = {}

    def check_origin(self, origin):
        return True

    def open(self, *args, **kwargs):
        print(self.request.remote_ip)
        print("new born")
        self.id = "undefinded"
        self.application.Devices[self.id] = self
        self.write_message(json.dumps({"cmd":101, "params":{}}))
        self.queue = queue.Queue(maxsize=1)
        self.terminal_proxies = set()

    def on_message(self, message):
        print("on_message")
        print(message)
        msg = json.loads(message)
        self.dispatch(msg)

    def on_close(self):
        print("connect close %s" %self.id)
        del self.application.Devices[self.id]

    def add_listener(self, listener):
        self.terminal_proxies.add(listener)

    def remove_listener(self, listener):
        self.terminal_proxies.remove(listener)

    def dispatch(self, msg):
        cmd = msg.get("cmd")
        params = msg.get("params")
        if not cmd:
            return "no such command"
        if cmd == 102:
            id = params.get("id")
            self.application.Devices.pop(self.id, None)
            self.id = id
            self.application.Devices[self.id] = self
        elif cmd in (112, 110,  200):
            if cmd == 200:
                line = params.get("content", "")
            else:
                line = params
            for proxy in self.terminal_proxies:
                try:
                    proxy.on_device_message(line)
                except Exception as e:
                    print("Error in sending message to Proxy")
                    print(e)
        return


class ConsoleHandler(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self, *args, **kwargs):
        pass

    def on_message(self, message):
        pass

    def on_close(self):
        pass


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        devices = self.application.Devices
        devices_list = [{"id": devices[d].id, "address": devices[d].request.remote_ip} for d in devices]
        self.render("index.html", devices=devices_list)


class CheckHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        devices = self.application.devices
        devices_list = [{"id": k, "address": v} for k, v in zip(devices.keys(), devices.values())]
        self.write(json.dumps(devices_list))


def main():
    tornado.options.parse_command_line()
    app = Application()
    app.listen(options.port)
    print("Listening %s port" % options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
