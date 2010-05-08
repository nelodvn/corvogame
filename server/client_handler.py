# -*- coding: utf-8 -*-
import asyncore, socket

class ClientHandler(asyncore.dispatcher):
  def __init__(self, conn):
    asyncore.dispatcher.__init__(self, conn)
    self.obuffer = []

  def write(self, data):
    self.obuffer.append(data)

  def shutdown(self):
    self.obuffer.append(None)
       
  def writable(self):
    return self.obuffer
    
  def handle_write(self):
    if self.obuffer[0] is None:
      self.close()
      return

    sent = self.send(self.obuffer[0])
    if sent >= len(self.obuffer[0]):
      self.obuffer.pop(0)
    else:
      self.obuffer[0] = self.obuffer[0][sent:]   
        
    
      
    
    