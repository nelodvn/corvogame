#!/usr/bin/python
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

import sys
sys.path.append('..')

from common import json_handler
import server_listener
import simple_auth
import lobby as l
import asyncore
import logging

logging.basicConfig(level=logging.DEBUG, format= '%(asctime)s %(levelname)-8s %(module)-20s[%(lineno)-3d] %(message)s')

lobby = l.Lobby()

def add_to_lobby(session):
    lobby.handshake(session)

if __name__ == "__main__":
    logging.debug("Starting corvogame...")
    server = server_listener.ServerListener("0.0.0.0", 5000)

    server.register_auth_handler(simple_auth.authenticate)
    server.register_message_handler("json", json_handler.Handler() )
    server.register_logon_handler(add_to_lobby)

    try:
        logging.info("Corvogame is running...")
        asyncore.loop(timeout=1.0)
    except KeyboardInterrupt:
        logging.info("Closing corvogame server")
        logging.debug("Stopping lobby")
        lobby.stop()
        logging.debug("done")
        logging.debug("Stopping server")
        server.shutdown()
        logging.debug("done")
        logging.info("Shutdown complete.")
