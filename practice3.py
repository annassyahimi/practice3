import os
import socket
import time
from datetime import datetime


class SocketServer:
    def __init__(self):
        self.bufsize = 1024  # buffer size
        self.DIR_PATH = './request'
        self.createDir(self.DIR_PATH)

    def createDir(self, path):
        """디렉토리 생성"""
        if not os.path.exists(path):
            try:
                os.makedirs(path)
                print(f"Directory created at {path}")
            except OSError:
                print("Error: Failed to create the directory.")

    def run(self, ip, port):
        """서버 실행"""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((ip, port))
        self.sock.listen(10)

        print("Socket server started...")
        print("Press Ctrl+C to stop the server.\n")

        try:
            while True:
                # 클라이언트 요청 대기
                clnt_sock, req_addr = self.sock.accept()
                clnt_sock.settimeout(5.0)
                print(f"Received request from {req_addr}")

                # 실습 1
                raw_data = clnt_sock.recv(self.bufsize)
                timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
                filename = f"{timestamp}.bin"
                bin_path = os.path.join(self.DIR_PATH, filename)

                with open(bin_path, 'wb') as f:
                    f.write(raw_data)
                print(f"Saved raw request to {bin_path}")

                # 실습 2
                if b"Content-Type: image/jpeg" in raw_data:
                    print("Image detected in request body")

                    # Very simple extraction
                    body_split = raw_data.split(b"\r\n\r\n", 1)
                    if len(body_split) > 1:
                        image_part = body_split[1]
                        end_marker = image_part.find(b"\r\n--")
                        if end_marker != -1:
                            image_part = image_part[:end_marker]

                        image_filename = f"{timestamp}.jpg"
                        image_path = os.path.join(self.DIR_PATH, image_filename)

                        with open(image_path, 'wb') as img:
                            img.write(image_part)

                        print(f"Image saved to {image_path}")
                    else:
                        print("Could not extract image part from request")

                # 응답 전송
                response = b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nSocket server received your data!"
                clnt_sock.sendall(response)

                # 클라이언트 소켓 닫기
                clnt_sock.close()

        except KeyboardInterrupt:
            print("\n Stopping the server...")

        # 서버 소켓 닫기
        self.sock.close()


if __name__ == '__main__':
    server = SocketServer()
    server.run('127.0.0.1', 8000)