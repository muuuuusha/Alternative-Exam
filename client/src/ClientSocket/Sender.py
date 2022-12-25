from src.ClientSocket.ClientSocket import ClientSocket

class Sender:
    def __init__(self, server_ip: str, server_port: int):
        self.server_ip = server_ip
        self.server_port = server_port
        
    def send(self, json: dict) -> dict:
        try:
            with ClientSocket(self.server_ip, self.server_port) as sock:
                sock.send(json)
                return sock.recv()
        except ConnectionRefusedError as e:
            print(e)
            return {'code': 'Connection failed'}
        except Exception as e:
            print(e)
            return {'code': str(e)}
            