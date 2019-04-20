import socket
import sys
import _thread

size = 20480

def black_list(): #hàm này là đọc file black list
    data = open("blacklist.conf", "r")
    black_data = data.readlines()
    black_data = [x.strip() for x in black_data]
    data.close()
    return black_data

def proxy_thread(request): #hàm này để phân tích cái gói tin gửi 
    change_format = request.decode("utf-8") #chuyển dạng gói tin về với định dạng utf-8
    first_line = change_format.split('\n')[0] # parse the first line

    # find the webserver and port
    url = first_line.split(' ')[1]  #dòng này lấy cái địa chỉ url

    http_pos = url.find("://") # tìm ://
    if(http_pos == -1):
        temp = url
    else:
        temp = url[(http_pos + 3):]

    #tìm cái port phụ nếu có
    port_pos = temp.find(":")

    #tìm kết thúc của cái server
    web_server_pos = temp.find("/")

    if web_server_pos == -1:
        web_server_pos = len(temp)

    if port_pos==-1 or web_server_pos < port_pos:
        port = 80   #set lại port bằng 80(80 là HTTP)
        web_server = temp[:web_server_pos]
    else:   #port riêng nè
        port = int((temp[(port_pos + 1):])[:web_server_pos - port_pos - 1])
        web_server = temp[:port_pos]

    return web_server, port


def Get(request, server, size, black_list):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        host, port = proxy_thread(request)

        Block = False
        for i in black_list:
            if host in i:
                Block = True
                break

        if not Block:
            client_socket.connect((host, port))
            client_socket.sendall(request)
            Post(client_socket, server, size)
        else:
            Error(server)
    except socket.error:
        client_socket.close()
        server.close()
        sys.exit(1)
    except:
        pass

def Post(client, server, size):
    while True:
        respond = client.recv(size)
        if len(respond) > 0:
            server.send(respond)
        else:
            break
    client.close()
    server.close()

def Error(server):
    server.send(b'HTTP/1.1 403 Forbidden\r\n\r\n<html>\r\n<title>403 Forbidden</title>\r\n<body>\r\n'
                        b'<h1>Error 403: Forbidden</h1>\r\n<p>This page is blocked by proxy server.</p>\r\n'
                        b'<p>Do you wanna access the website, Direct me <3</p>'
                        b'</body>\r\n</html>\r\n')
    server.close()

def main():
    time = 1000
    Block_list = black_list()

    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('', 8888))
        server.listen(time)

    except socket.error as error:
        print("Loading error: {}".format(error))
        sys.exit(2)
    
    while True:
        server_connection, client_addr = server.accept()
        request = server_connection.recv(size)
        _thread.start_new_thread(Get,
                                 (request, server_connection, size, Block_list))
    server.close()
    sys.exit(1)

if __name__ == "__main__":
    main()
