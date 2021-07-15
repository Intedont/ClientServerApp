import asyncio

serverData = dict()


class ClientServerProtocol(asyncio.Protocol):

    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        self.transport = transport

    def data_received(self, data):
        resp = self.process_data(data.decode())
        print("Отвечаем: ")
        print(resp)
        self.transport.write(resp.encode())

    def process_data(self, data):
        data = data[:len(data)-1]
        request = data.split(' ')
        if request[0] == "put":
            print("Принимаем запрос put: " + request[1])
            if request[1] in serverData.keys():
                serverData[request[1]].append((request[3], request[2]))
            else:
                serverData[request[1]] = list()
                serverData[request[1]].append((request[3], request[2]))
            print(serverData)
            return "ok\n\n"
        elif request[0] == "get":
            print("Принимаем запрос get: " + request[1])
            if request[1] in serverData.keys():
                print("Есть такой элемент!")
                resp = "ok\n"
                for line in serverData[request[1]]:
                    resp = resp + request[1] + " " + str(line[1]) + " " + str(line[0]) + "\n"
                return resp
            elif request[1] == "*":
                print("Выводим все элементы")
                resp = "ok\n"
                for pos in serverData:
                    for line in serverData[pos]:
                        resp += pos + " " + line[1] + " " + line[0] + "\n"
                return resp
            else:
                print("Нет такого ключа!")
                return " "
        else:
            print("Bad command")
            return "error\nwrong command\n\n"


def run_server(host, port):
    loop = asyncio.get_event_loop()
    coro = loop.create_server(
        ClientServerProtocol,
        host, port
    )

    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()

