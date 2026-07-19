# Exercise 5 — TCP Live Data Client with Rolling Buffer

## Overview

In the previous exercise, the signal was generated locally inside the application.

In this exercise, the signal comes from a **TCP server**.

The goal is to replace the old simulated `SignalModel` with a new `TcpClientModel`.

The rest of the application should stay mostly the same:

```text
Previous exercise:
SignalModel -> MainViewModel -> MainView -> PlotView

This exercise:
TcpClientModel -> MainViewModel -> MainView -> PlotView
```

This is an important MVVM lesson:

> If the architecture is clean, we can replace the data source without rewriting the whole application.

---

## Learning Goals

By the end of this exercise, you should understand:

- what TCP is
- what a TCP server does
- what a TCP client does
- why TCP sends bytes instead of NumPy arrays
- why client and server must agree on the data format
- how `connect()` and `disconnect()` work
- what `recv()` does
- why we need a byte buffer
- how raw bytes are converted back into NumPy arrays
- what a rolling buffer is
- why data receiving is often done in a separate thread
- why this exercise uses a `QTimer` and non-blocking socket instead of a receive thread

---

# Part 1 — What is TCP?

TCP stands for **Transmission Control Protocol**.

It is a communication protocol used to send data between programs.

These programs may run:

- on the same computer
- on different computers in the same network
- on different computers over the internet

In this exercise, both programs run on the same computer:

```text
TCP server  -> sends EMG data
TCP client  -> receives EMG data and plots it
```

The server listens for incoming connections.

The client connects to the server.

Once the connection exists, bytes can be sent from one side to the other.

---

## Server and Client

A TCP communication usually has two roles:

### Server

The server:

- opens a port
- waits for a client
- accepts a connection
- sends or receives data

In this exercise, the server sends EMG data.

### Client

The client:

- knows the server address
- connects to the server
- receives data
- converts the received bytes back into useful values

In this exercise, the client receives EMG data and passes it to the plot.

---

## Host and Port

To connect to a TCP server, the client needs two pieces of information:

```python
host = "localhost"
port = 12345
```

### Host

The host says where the server is running.

In this exercise:

```python
host = "localhost"
```

means:

> The server is running on the same computer.

### Port

The port identifies the specific program that should receive the connection.

In this exercise:

```python
port = 12345
```

The server and client must use the same port.

---

# Part 2 — What does the server send?

The server sends EMG data.

For this exercise, the server sends:

```text
32 channels
18 samples per packet
float64 values
```

So one packet has this shape:

```text
(32, 18)
```

That means:

- 32 rows = 32 EMG channels
- 18 columns = 18 samples per channel

Example:

```text
Channel 1:  [sample 1, sample 2, ..., sample 18]
Channel 2:  [sample 1, sample 2, ..., sample 18]
...
Channel 32: [sample 1, sample 2, ..., sample 18]
```

---

## Important: TCP does not send NumPy arrays

The server may start with a NumPy array:

```python
current_window = self.emg_signal[:, :, window_index]
```

This has shape:

```text
(32, 18)
```

But TCP cannot directly send a NumPy array.

TCP sends **bytes**.

Therefore, the server converts the array into bytes:

```python
data_bytes = current_window.tobytes()
client_socket.sendall(data_bytes)
```

After this conversion, the shape and dtype information are no longer included.

The client only receives raw bytes.

That means the client must already know:

```text
number of channels
samples per packet
data type
```

This agreement between server and client is called the **data contract**.

---

## Data contract for this exercise

The server and client agree on this format:

```python
channels = 32
samples_per_packet = 18
dtype = np.float64
```

This means the client expects each packet to contain:

```text
32 * 18 = 576 values
```

Because `float64` uses 8 bytes per value:

```text
576 * 8 = 4608 bytes
```

So one complete EMG packet has:

```text
4608 bytes
```

In code:

```python
self.packet_size = self.channels * self.samples_per_packet
self.packet_size_bytes = self.packet_size * np.dtype(self.dtype).itemsize
```

For this exercise:

```python
self.packet_size = 32 * 18
self.packet_size_bytes = 32 * 18 * 8
```

---

# Part 3 — Connecting to the Server

The client connects to the server using a socket.

A socket is the object that represents the TCP connection.

The basic steps are:

```python
self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
self.socket.connect((self.host, self.port))
self.socket.setblocking(False)
self.is_connected = True
```

---

## What does this line mean?

```python
self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
```

This creates a TCP socket.

`socket.AF_INET` means:

> Use IPv4 addresses.

`socket.SOCK_STREAM` means:

> Use TCP.

---

## What does this line mean?

```python
self.socket.connect((self.host, self.port))
```

This connects the client to the server.

In this exercise, the connection target is:

```python
("localhost", 12345)
```

So the client tries to connect to a server running on the same computer at port `12345`.

---

## What does this line mean?

```python
self.socket.setblocking(False)
```

This puts the socket into **non-blocking mode**.

This is important because we do not want the GUI to freeze.

If a socket is blocking, then this line:

```python
self.socket.recv(...)
```

waits until data arrives.

That can block the Qt event loop and freeze the window.

With a non-blocking socket, `recv()` does not wait forever.

If no data is available, Python raises:

```python
BlockingIOError
```

In our client, we catch that error and simply try again later.

---

## TODO: `connect()`

Your task is to complete:

```python
def connect(self):
    """Connect to the TCP server."""
    if self.is_connected:
        return

    # TODO 1:
    # Create a TCP socket.

    # TODO 2:
    # Connect to self.host and self.port.

    # TODO 3:
    # Set the socket to non-blocking mode.

    # TODO 4:
    # Set self.is_connected to True.
```

Expected structure:

```python
self.socket = ...
self.socket.connect(...)
self.socket.setblocking(...)
self.is_connected = ...
```

---

# Part 4 — Disconnecting from the Server

When the user stops plotting, the client should close the TCP connection.

The basic logic is:

```python
self.is_connected = False

if self.socket is not None:
    self.socket.close()
    self.socket = None
```

---

## Why set `self.socket = None`?

Closing the socket ends the connection.

Setting it to `None` also makes the program state clear:

> There is currently no active socket.

This helps avoid accidentally using an old closed socket.

---

## TODO: `disconnect()`

Your task is to complete:

```python
def disconnect(self):
    """Close the TCP connection."""
    # TODO 1:
    # Set self.is_connected to False.

    # TODO 2:
    # If self.socket is not None:
    #   - close the socket
    #   - set self.socket to None
```

---

# Part 5 — Receiving Data with `recv()`

The client receives data using:

```python
new_bytes = self.socket.recv(self.packet_size_bytes)
```

This means:

> Try to receive up to `self.packet_size_bytes` bytes.

For this exercise:

```text
self.packet_size_bytes = 4608
```

because one EMG packet contains 4608 bytes.

---

## Important: `recv()` may not return a full packet

This is one of the most important TCP concepts.

When you call:

```python
self.socket.recv(self.packet_size_bytes)
```

you are asking for up to one packet of bytes.

But TCP does not guarantee that you receive exactly one packet.

You may receive:

```text
less than one packet
exactly one packet
more data later
```

For example, one server packet may arrive in several pieces:

```text
first recv():  1000 bytes
second recv(): 2000 bytes
third recv(): 1608 bytes
total:         4608 bytes
```

Only after all 4608 bytes have arrived can we reconstruct one complete EMG packet.

That is why we use a **byte buffer**.

---

## Why not use `recv(4096)`?

Many networking examples use:

```python
recv(4096)
```

This is a common general-purpose read size.

But in this exercise, `4096` is confusing because one EMG packet has:

```text
4608 bytes
```

So `4096` is smaller than one packet.

It would still work if we use a byte buffer, but it looks arbitrary.

For teaching, it is clearer to use:

```python
new_bytes = self.socket.recv(self.packet_size_bytes)
```

because this means:

> Try to receive approximately one EMG packet.

Even then, TCP may return fewer bytes, so the byte buffer is still necessary.

---

## TODO: `receive_data()`

Your task is to complete the receiving part:

```python
while True:
    try:
        # TODO 1:
        # Receive up to one packet of bytes from the socket.
        new_bytes = None

        if not new_bytes:
            self.disconnect()
            return

        # TODO 2:
        # Add the newly received bytes to self.byte_buffer.

    except BlockingIOError:
        break
```

Expected ideas:

```python
new_bytes = self.socket.recv(...)
self.byte_buffer.extend(...)
```

---

# Part 6 — Why do we need `self.byte_buffer`?

TCP is a byte stream.

That means received data does not automatically arrive in the same chunks that the server sent.

The server sends packets of 4608 bytes.

But the client may receive the bytes in smaller pieces.

So we collect all received bytes here:

```python
self.byte_buffer = bytearray()
```

Then every time new bytes arrive:

```python
self.byte_buffer.extend(new_bytes)
```

The byte buffer may contain:

```text
not enough bytes for a packet
exactly one packet
more than one packet
one full packet plus part of the next packet
```

Therefore, we only extract a packet when enough bytes are available:

```python
while len(self.byte_buffer) >= self.packet_size_bytes:
    ...
```

---

## Example

Assume one packet has 4608 bytes.

### First receive

```text
byte_buffer contains 2000 bytes
```

Not enough for one packet.

Do nothing yet.

### Second receive

```text
byte_buffer contains 3500 bytes
```

Still not enough.

Do nothing yet.

### Third receive

```text
byte_buffer contains 5000 bytes
```

Now we can extract one full packet:

```text
use first 4608 bytes
leave 392 bytes in the buffer
```

The remaining 392 bytes are the beginning of the next packet.

---

# Part 7 — Extracting packets from the byte buffer

This method converts raw bytes into NumPy arrays.

The full idea is:

```text
bytes -> NumPy array -> reshape to 32 x 18 -> add to packet list
```

---

## Step 1: Take one complete packet

```python
packet_bytes = self.byte_buffer[:self.packet_size_bytes]
```

This takes the first 4608 bytes.

---

## Step 2: Remove these bytes from the byte buffer

```python
del self.byte_buffer[:self.packet_size_bytes]
```

This is important because those bytes are now processed.

If we did not remove them, we would process the same data again.

---

## Step 3: Convert bytes to NumPy values

```python
packet = np.frombuffer(packet_bytes, dtype=self.dtype)
```

This converts raw bytes into numbers.

If `self.dtype = np.float64`, then NumPy reads 8 bytes per value.

The result is a one-dimensional array with 576 values.

---

## Step 4: Reshape the packet

```python
packet = packet.reshape(self.channels, self.samples_per_packet)
```

This converts the one-dimensional array into:

```text
32 x 18
```

Now each row is one channel.

---

## Step 5: Store the packet

```python
packets.append(packet)
```

The list `packets` stores all complete packets extracted during this update.

---

## TODO: `_extract_packets_from_buffer()`

In this exercise, the loop and buffer logic are already provided.

You only need to fill in the most important conversion steps:

```python
while len(self.byte_buffer) >= self.packet_size_bytes:
    # TODO 1:
    # Take one complete packet from the beginning of self.byte_buffer.
    packet_bytes = None

    # TODO 2:
    # Delete those bytes from self.byte_buffer.

    # TODO 3:
    # Convert packet_bytes into a NumPy array.
    packet = None

    # TODO 4:
    # Reshape the packet into:
    # channels x samples_per_packet
    packet = None

    # TODO 5:
    # Add the packet to the list of packets.
```

---

# Part 8 — Combining packets into the data buffer

After complete packets are extracted, they are combined:

```python
new_data = np.concatenate(packets, axis=1)
```

Why `axis=1`?

Each packet has shape:

```text
32 x 18
```

If we receive two packets, we want:

```text
32 x 36
```

not:

```text
64 x 18
```

So we concatenate along the sample axis.

Example:

```text
packet 1: 32 x 18
packet 2: 32 x 18

combined: 32 x 36
```

That means:

- same channels
- more samples over time

---

## Adding new data to the existing buffer

The existing data is stored in:

```python
self.data_buffer
```

New data is added like this:

```python
self.data_buffer = np.concatenate(
    (self.data_buffer, new_data),
    axis=1,
)
```

Again, `axis=1` means:

> Add new samples to the right side.

---

# Part 9 — Rolling Buffer

If we stored all received samples forever, the array would grow continuously.

That is not efficient.

For live plotting, we usually only need the newest data.

In this exercise, we use a 10-second rolling buffer.

---

## How many samples are 10 seconds?

The sampling rate is:

```python
sampling_rate = 2000
```

This means:

```text
2000 samples per second
```

For 10 seconds:

```text
2000 * 10 = 20000 samples
```

In code:

```python
self.window_size = int(self.sampling_rate * self.window_seconds)
```

For this exercise:

```python
self.window_size = 2000 * 10
```

So the buffer keeps only the newest 20000 samples.

---

## Removing old samples

After adding new data, the buffer may be too long.

Then we keep only the newest samples:

```python
if self.data_buffer.shape[1] > self.window_size:
    self.data_buffer = self.data_buffer[:, -self.window_size:]
```

This means:

> Keep all channels, but only the last `window_size` samples.

The `:` means all channels.

The `-self.window_size:` means the last 20000 samples.

---

## Why is this called a rolling buffer?

Because new data enters on the right, and old data leaves on the left.

Conceptually:

```text
old data                         new data
[----------------------------------------]
     old samples removed  ->  new samples added
```

This is exactly what we want for a live signal display.

---

# Part 10 — Signal Time

The app also shows the current signal time.

The signal time is not measured with a wall-clock timer.

It is calculated from the amount of received data.

If the client has received `total_samples_received` samples and the sampling rate is `sampling_rate`, then:

```python
signal_time = total_samples_received / sampling_rate
```

This is equivalent to:

```python
signal_time = number_of_chunks * samples_per_packet / sampling_rate
```

For example:

```text
chunk size = 18 samples
sampling rate = 2000 Hz
number of chunks = 100

signal time = 100 * 18 / 2000
signal time = 0.9 seconds
```

In code:

```python
def get_signal_time_seconds(self):
    return self.total_samples_received / self.sampling_rate
```

---

# Part 11 — Threads: Why are they often used?

In real applications, receiving data is often done in a separate thread.

Why?

Because receiving data can take time.

If the GUI waits for data, the window may freeze.

A separate receive thread can run independently:

```text
GUI thread:
    handles buttons, labels, plotting, repainting

Receive thread:
    waits for TCP data
    receives data
    stores it in a buffer
```

This is common in real-time applications.

---

## Why not use a thread in this exercise?

Threads are powerful, but they add complexity.

When using threads, we must think about:

- shared data
- race conditions
- locks
- thread-safe communication
- stopping the thread safely
- emitting Qt signals from the correct place

That is too much for this exercise.

Instead, we use a simpler approach:

```text
Qt QTimer
non-blocking socket
byte buffer
```

The ViewModel has a timer:

```python
self.timer = QTimer(self)
self.timer.timeout.connect(self.update_plot)
```

Every 10 ms, the ViewModel calls:

```python
self.model.receive_data()
```

Because the socket is non-blocking, this does not freeze the GUI.

If data is available, we read it.

If no data is available, we continue.

---

## Threaded version vs this exercise

| Real threaded approach | This exercise |
|---|---|
| receive data in background thread | receive data during timer updates |
| blocking socket can be used | non-blocking socket is used |
| needs thread-safe buffer | simple buffer inside model |
| more realistic for large systems | easier to understand |
| more complex | better for learning basics |

---

## Important teaching point

The server uses threads because it may need to handle multiple clients.

The client does not use threads in this exercise.

The client uses:

```text
QTimer + non-blocking recv()
```

This is enough for a simple local teaching application.

---

# Part 12 — How the pieces work together

The full data flow is:

```text
TCP server sends bytes
        ↓
TcpClientModel.receive_data()
        ↓
bytes are added to byte_buffer
        ↓
complete packets are extracted
        ↓
packets become NumPy arrays
        ↓
arrays are added to data_buffer
        ↓
old samples are removed from rolling buffer
        ↓
MainViewModel asks for x and y
        ↓
ViewModel emits plot_updated(x, y)
        ↓
PlotView updates the live plot
```

---

# Part 13 — Debugging Tips

## 1. Client cannot connect

Check:

- Is the server running?
- Does the server use the same port?
- Is the host `"localhost"`?
- Did you start the server before the client?

---

## 2. Received values look extremely large or strange

This usually means the dtype is wrong.

Server and client must agree on:

```python
dtype = np.float64
```

If the server sends `float64`, the client must read `float64`.

If the server sends `float32`, the client must read `float32`.

Wrong dtype creates nonsense values.

---

## 3. Nothing appears in the plot

Check:

- Is the server sending data?
- Is `receive_data()` being called?
- Is `self.byte_buffer` growing?
- Is `self.data_buffer.shape[1]` increasing?
- Is the selected channel maybe zero?
- Is the y-scale too small or too large?

---

## 4. GUI freezes

Check:

- Did you forget `self.socket.setblocking(False)`?
- Are you accidentally using a `while True` loop without `BlockingIOError` handling?
- Is the socket waiting forever for data?

---

# Part 14 — Final Checklist for TODOs

Before running the app, check:

## `connect()`

- created socket
- connected to `(self.host, self.port)`
- set socket to non-blocking
- set `self.is_connected = True`

## `disconnect()`

- set `self.is_connected = False`
- closed socket if it exists
- set `self.socket = None`

## `receive_data()`

- received bytes with `recv(...)`
- checked for empty data
- added bytes to `self.byte_buffer`
- handled `BlockingIOError`

## `_extract_packets_from_buffer()`

- took one full packet from the byte buffer
- deleted processed bytes
- converted bytes to NumPy array
- reshaped array to `channels x samples_per_packet`
- appended packet to `packets`

---

# Final Takeaway

TCP sends bytes, not arrays.

The server and client must agree on the format of those bytes.

In this exercise, one packet is:

```text
32 channels x 18 samples x 8 bytes = 4608 bytes
```

The client collects bytes in a buffer until a full packet is available.

Then it converts the packet back into a NumPy array and adds it to a rolling 10-second buffer.

This gives us a clean live-data model that can replace the old simulated signal model without changing the rest of the MVVM application.
