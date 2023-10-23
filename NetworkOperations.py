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

    async def send_data_util(self, ip, port, data):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.connect((ip, port))
                s.sendall(data)
            except:
               print(f"Failed to connect to IP: {ip}, Port: {port}")

    async def receive_data_util(self, reader, writer):
        data_received = bytearray()
        while True:
            data_chunk = await reader.read(1024)
            if not data_chunk:
                break
            data_received.extend(data_chunk)
        return data_received.decode()  # Decoding bytes to string
