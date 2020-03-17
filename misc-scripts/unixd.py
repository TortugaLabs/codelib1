#!/usr/bin/env python3

# tags:_attic
# target::/usr/local/bin/
# mode:755


import socket
import os
import sys
import signal

# Ignore children
signal.signal(signal.SIGCHLD, signal.SIG_IGN)

if len(sys.argv) < 2:
  sys.stderr.write("Usage:\n\tunixd socket-path cmd\n")
  sys.exit(8)

unix_socket = sys.argv[1]
command = sys.argv[2:]

if len(command) == 0:
  command = [ '/bin/sh', '-il' ]

# ~ print("Cmd: " , str(command))

if os.path.exists(unix_socket):
  os.remove(unix_socket)

server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
server.bind(unix_socket)
server.listen(5)

while True:
  client,addr = server.accept()
  # ~ print("Got connection from %s" % str(addr))

  if os.fork():
    client.close()
  else:
    server.close()
    os.dup2(client.fileno(),0)
    os.dup2(client.fileno(),1)
    os.execv(command[0],command)
    os.exit(37)

  


