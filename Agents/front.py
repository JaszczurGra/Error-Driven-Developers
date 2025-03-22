import socket
def receive_data(host='localhost', port=4443):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen(1)
        print(f"Listening on {host}:{port}...")
        
        conn, addr = server_socket.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                data = conn.recv(1024)
                if not data:
                    break

                try:
                    print("Received:",data.decode())
                except:
                    print("Received:",data)
                

if __name__ == "__main__":
    receive_data()

# import http.server
# import ssl

# class RequestHandler(http.server.BaseHTTPRequestHandler):
#     def do_POST(self):
#         content_length = int(self.headers.get('Content-Length', 0))
#         post_data = self.rfile.read(content_length).decode('utf-8')
#         print(f"Received POST request:\n{post_data}")
        
#         self.send_response(200)
#         self.send_header('Content-Type', 'text/plain')
#         self.end_headers()
#         self.wfile.write(b"Received")

#     def do_GET(self):
#         self.send_response(200)
#         self.send_header('Content-Type', 'text/plain')
#         self.end_headers()
#         self.wfile.write(b"Hello, this is an HTTPS server!")


# def run_server(port=4443, certfile="cert.pem", keyfile="key.pem"):
#     server_address = ('', port)
#     httpd = http.server.HTTPServer(server_address, RequestHandler)
#     httpd.socket = ssl.wrap_socket(httpd.socket,server_side=False)# certfile=certfile, keyfile=keyfile, server_side=True)
#     print(f"Serving on https://localhost:{port}")
#     httpd.serve_forever()

# if __name__ == "__main__":
#     run_server()