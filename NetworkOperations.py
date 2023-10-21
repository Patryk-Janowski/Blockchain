import socket


class NetworkOperations:
    block_port = 50000
    users_port = 50001

    def get_my_ip(self):
        try:
            # get the host name
            host_name = socket.gethostname()
            # get the IP address
            host_ip = socket.gethostbyname(host_name)
            return host_ip
        except socket.error as err:
            print(f"Unable to get Hostname and IP. Error: {str(err)}")

    def send_data_util(self, ip, port, data):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((ip, port))
            s.sendall(data)

    def receive_data_util(self, port, ip="0.0.0.0", buffer_size=1024):
        # Create a socket to listen for incoming connections
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((ip, port))
            s.listen()
            print(f"Listening on {ip}:{port}")
            # Wait for a connection
            conn, addr = s.accept()
            with conn:
                print(f"Connected by: {addr}")
                data_received = bytearray()
                # Loop to receive all data sent
                while True:
                    data_chunk = conn.recv(buffer_size)
                    if not data_chunk:
                        break
                    data_received.extend(data_chunk)
        return data_received.decode()  # Decoding bytes to string
