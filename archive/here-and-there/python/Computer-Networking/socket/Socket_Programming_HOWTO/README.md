# About socket
This note is based on [the doc of how to use socket](https://docs.python.org/2/howto/sockets.html).

## Creating a socket
What is `client socket` and `server socket`?

When you clickd on the link that brought you to a web-page,your brower did something like the following:

```python
# create an AF_INET, STREAMing socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# now connect to the web server on port 80
s.connect(("www.darkframexue.com"), 80)
```

Yes, you are right , this is what a `client socket` is, and when the `connect` completes, the socket `s` can be used to send a request for the text of the page. The **same socket** will read the reply and then be **destroyed**.

What happens in the web server is bit more complex, first the web server creates a `server socket`.

```python
# create an AF_INET, STREAMimg socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# then bind the socket to a public host and the well-known 80 port
# use gethostname()	so taht socket would be visible to the outside world.
server_socket.bind((socket.gethostname(), 80)

# became a server socket
# we want to queue up as many as 5 connect requests before refusing outside connections.
server_socket.listen(5)
```

Now we have a `server socket`, listening on port 80, we can enter the mainloop of the web server:
```
while 1:
	# accept connections from outside
	(clientsocket, address) = serversocket.accept()
	
	# now do something with the clientsocket
	# in this case, we'll pretend this is a threaded server
	ct = client_thread(clientsocket)
	ct.run()
```

## Using a Socket
There are two sets of verbs to use for socket communication. You can use `send` and `recv`, or you can transform your client socket into a file-like beast and use `read` and `write`. These are buffered "files", and a common mistake is `write` something, and `read` for a reply, actually without a `flush` in there, you may wait forever for the reply, because the request may still be in your output buffer.

Now we come to the major stumbling block of sockets - `send` and `recv` operate on the network buffers.  They do not necessarily handle all the bytes you hand them (or expect from them), because their major focus is **handling the network buffers**. In general, they return when the associated network buffers have been filled (send) or emptied (recv). They then tell you how many bytes they handled. It is your responsibility to call them again until your message has been completely dealt with.

When a `recv` return **0 bytes**, it means the other side has **closed**(or is in the process of closing) the connection. You will not receive any more data on this connection. Ever. You may be able to send data successfully.

A protocol like HTTP uses a socket for only one transfer. The client sends a request, then read a reply. That's it. The socket it discarded. This means a client can detect the end of the reply by receiving 0 bytes.


But if you plan to reuse your socket for further transfers, you need to realize that there is **no EOT** on a socket, if the connection has not been broken, you may wait on a `recv` forever, because the socket will not tell you that there’s nothing more to read (for now). Here is the fundamental truth of sockets: *messages must either be fixed length (yuck), or be delimited (分隔)(shrug), or indicate how long they are (much better), or end by shutting down the connection.* The choice is entirely yours, (but some ways are righter than others).


Assuming you don't want to end the connection, the simplest solution is a fixed length message:

```python
class MySocket:
	
	def __init__(self, sock = None):
		if sock is None:
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		else:
			self.sock = sock
	
	def connect(self, host, port):
		self.sock.connect((host, port))

	def mysend(self, msg):
		totalsent = 0
		while totalsent < MSGLEN:
			sent = self.sock.send(msg[totalsent: ])
			if sent == 0:
				raise RuntimeError("socket connection broken")
			totalsent = totalsent + sent

	def myreceive(self):
		chunks = []
		bytes_recd = 0
		while bytes_recd < MSGLEN:
			chunk = self.sock.recv(min(MSGLEN - bytes_recd, 2048))
			if chunk == '':
				raise RuntimeError("socket connection broken")
			chunks.append(chunk)
			bytes_recd = bytes_recd + len(chunk)
		return ''.join(chunks)
```
