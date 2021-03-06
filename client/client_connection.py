# -*- coding: utf-8 -*-
#    This file is part of corvogame.
#
#    corvogame is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    corvogame is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with corvogame.  If not, see <http://www.gnu.org/licenses/>.

from common import client_handler
import asyncore
import socket
import logging

def debug(str):
    logging.debug("Read from socket:")
    logging.debug(str)

class Client(client_handler.ClientHandler):
    ''' Basic TCP client. '''
    def __init__(self, ip, port):
        client_handler.ClientHandler.__init__(self)
        logging.debug("Initializing Client...")

        self.message_handlers = {}
        self.ip = ip
        self.port = port

        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((ip,port))

    def register_message_handler(self, protocol, handler):
        ''' Register message handlers. Used to make the client abstract on how
            messages are parsed. '''
        logging.debug("Registering {0} as a message handler".format(handler))
        self.message_handlers[protocol] = handler
        self.message_handler = handler

    def shutdown(self):
        logging.debug("Client is shutting down...")

    def handle_connect(self):
        self.obuffer.append('json') # TODO select protocol from configuration
        self.read_handler = debug

