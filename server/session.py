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

from common.client_handler import ClientHandler
import logging

class Session(ClientHandler):
    def __init__(self, unknown_connection):
        self.username = unknown_connection.username
        ClientHandler.__init__(self, unknown_connection.socket)
        self.obuffer = self.obuffer + unknown_connection.obuffer
        self.message_handler = unknown_connection.message_handler
        self.read_handler = self.handle_session_messages
        self.incoming_message_handler = None

    def handle_session_messages(self, message):
        logging.debug("Received message {0} from session user {1}".format(message, self.username))
        if self.incoming_message_handler:
            logging.debug("Sending to handler {0}".format(self.incoming_message_handler))
            self.incoming_message_handler(self, message)

    def write(self, message):
        logging.debug("Writting message {0} to user {1}".format(message, self.username))
        ClientHandler.write(self, self.message_handler.to_string(message))

    def handle_error(self, _type, value, traceback ):
        logging.debug("Tracked an session error of type {0} and value {1}\n Traceback {2}".format(_type, value, traceback))
        self.close()
