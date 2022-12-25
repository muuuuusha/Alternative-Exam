import socketserver
from RequestHandler import RequestHandler

#TODO add same config file for client and server
LISTEN_IP = ''
LISTEN_PORT = 3000

if __name__ == '__main__':
    print('Server starting...') 
    serv = socketserver.TCPServer((LISTEN_IP, LISTEN_PORT), RequestHandler)
    print('Server started on port', LISTEN_PORT)
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print('Server stopped by admin')
        serv.shutdown()
        serv.server_close()
    except Exception as e:
        print('Server stopped by exception:', e)
        serv.shutdown()
        serv.server_close()