#!/usr/bin/env python3

# tags:_attic
# target::/usr/local/bin/
# mode:755

import socket
import os
import sys
import signal

if len(sys.argv) != 2:
  sys.stderr.write("Usage:\n\tunixd socket-path\n")
  sys.exit(8)

unix_socket = sys.argv[1]

if not os.path.exists(unix_socket):
  sys.stderr.write("%s: not found" % unix_socket)
  sys.exit(14)

conn = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
conn.connect(unix_socket)

pid = os.fork()
if pid:
  while 1:
    data = conn.recv(8192)
    if not data: break
    sys.stdout.write(data.decode('utf-8'))
  os.kill(pid, signal.SIGTERM)
else:
  while 1:
    data = sys.stdin.readline(8192)
    if not data: break
    conn.send(data.encode())
  os.kill(os.getppid(), signal.SIGTERM)
