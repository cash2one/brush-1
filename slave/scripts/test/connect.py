import socket
import struct
import os
import time
import hashlib

HOST = '192.168.1.76'
PORT = 8000
BUFFER_SIZE = 1024
FILE_NAME = 'usertrj.txt'   # Change to your file
FILE_SIZE = os.path.getsize(FILE_NAME)
HEAD_STRUCT = '128sIq32s'  # Structure of file head


def send_file():
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect the socket to the server
    server_address = (HOST, PORT)

    #Calculate MD5
    print("Calculating MD5...")
    fr = open(FILE_NAME, 'rb')
    md5_code = hashlib.md5()
    md5_code.update(fr.read())
    fr.close()
    print("Calculating success")

    # Need open again
    fr = open(FILE_NAME, 'rb')
    # Pack file info(file name and file size)
    file_head = struct.pack('128sIq32s', b'usertrj.txt', len(FILE_NAME), FILE_SIZE, md5_code.hexdigest())

    try:
        # Connect
        sock.connect(server_address)
        print("Connecting to %s port %s" % server_address)
        # Send file info
        sock.send(file_head)
        send_size = 0
        print("Sending data...")
        time_start = time.time()
        while send_size < FILE_SIZE:
            if FILE_SIZE - send_size < BUFFER_SIZE:
                file_data = fr.read(FILE_SIZE - send_size)
                send_size = FILE_SIZE
            else:
                file_data = fr.read(BUFFER_SIZE)
                send_size += BUFFER_SIZE
            sock.send(file_data)
        time_end = time.time()
        print("Send success!")
        print("MD5 : %s" % md5_code.hexdigest())
        print("Cost %f seconds" % (time_end - time_start))
        fr.close()
        sock.close()
    except socket.errno as e:
        print("Socket error: %s" % str(e))
    except Exception as e:
        print("Other exception : %s" % str(e))
    finally:
        print("Closing connect")

if __name__ == '__main__':
    send_file()