import socket
import select

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

host = ""
port = 8888

p1 = [100, 100, 0.0]
p2 = [700, 100, 3.0]
p3 = [100, 500, 0.0]
p4 = [700, 500, 3.0]

# bullet = [player, angle, x, y]

keys = [False, False, False, False]

server_socket.bind((host, port))
print "Server bounded."

players = {"1": "", "2": "", "3": "", "4": ""}
addrs = []

while True:
    try:
        msg, addr = server_socket.recvfrom(2048)
        code = msg[:2]
        print "start - ", msg, code, addr
        if code == "00":
            if addr not in addrs:
                if players["1"] == "":
                    players["1"] = addr
                    addrs.append(addr)
                    server_socket.sendto("You are player #1", addr)
                    server_socket.sendto("zz,1," + str(p1[0]) + "," + str(p1[1]) + "," + str(p1[2]), addr)
                    server_socket.sendto("zz,2," + str(p2[0]) + "," + str(p2[1]) + "," + str(p2[2]), addr)
                    server_socket.sendto("zz,3," + str(p3[0]) + "," + str(p3[1]) + "," + str(p3[2]), addr)
                    server_socket.sendto("zz,4," + str(p4[0]) + "," + str(p4[1]) + "," + str(p4[2]), addr)
                    for addr in addrs:
                        server_socket.sendto("T,Player #1 Connected.", addr)
                elif players["2"] == "":
                    players["2"] = addr
                    addrs.append(addr)
                    server_socket.sendto("You are player #2", addr)
                    server_socket.sendto("zz,1," + str(p1[0]) + "," + str(p1[1]) + "," + str(p1[2]), addr)
                    server_socket.sendto("zz,2," + str(p2[0]) + "," + str(p2[1]) + "," + str(p2[2]), addr)
                    server_socket.sendto("zz,3," + str(p3[0]) + "," + str(p3[1]) + "," + str(p3[2]), addr)
                    server_socket.sendto("zz,4," + str(p4[0]) + "," + str(p4[1]) + "," + str(p4[2]), addr)
                    for addr in addrs:
                        server_socket.sendto("T,Player #2 Connected.", addr)
                elif players["3"] == "":
                    players["3"] = addr
                    addrs.append(addr)
                    server_socket.sendto("You are player #3", addr)
                    server_socket.sendto("zz,1," + str(p1[0]) + "," + str(p1[1]) + "," + str(p1[2]), addr)
                    server_socket.sendto("zz,2," + str(p2[0]) + "," + str(p2[1]) + "," + str(p2[2]), addr)
                    server_socket.sendto("zz,3," + str(p3[0]) + "," + str(p3[1]) + "," + str(p3[2]), addr)
                    server_socket.sendto("zz,4," + str(p4[0]) + "," + str(p4[1]) + "," + str(p4[2]), addr)
                    for addr in addrs:
                        server_socket.sendto("T,Player #3 Connected.", addr)
                elif players["4"] == "":
                    players["4"] = addr
                    addrs.append(addr)
                    server_socket.sendto("You are player #4", addr)
                    server_socket.sendto("zz,1," + str(p1[0]) + "," + str(p1[1]) + "," + str(p1[2]), addr)
                    server_socket.sendto("zz,2," + str(p2[0]) + "," + str(p2[1]) + "," + str(p2[2]), addr)
                    server_socket.sendto("zz,3," + str(p3[0]) + "," + str(p3[1]) + "," + str(p3[2]), addr)
                    server_socket.sendto("zz,4," + str(p4[0]) + "," + str(p4[1]) + "," + str(p4[2]), addr)
                    for addr in addrs:
                        server_socket.sendto("T,Player #4 Connected.", addr)
                else:
                    server_socket.sendto("Maximum number of players connected.", addr)
        elif code == "11":
            print 'Getting pos#1'
            data = msg[2:]
            print data, addr
            data = data.split(',')
            for i in xrange(len(data) - 1):
                p1[i] = int(data[i])
            p1[2] = data[2]
            server_socket.sendto("OK. " + "\tP1: " + str(p1), addr)
            # notify all players
            for addr in addrs:
                server_socket.sendto("zz,1," + str(p1[0]) + "," + str(p1[1]) + "," + str(p1[2]), addr)
        elif code == "12":
            print 'Getting pos#2'
            data = msg[2:]
            print data, addr
            data = data.split(',')
            for i in xrange(len(data) - 1):
                p2[i] = int(data[i])
            p2[2] = data[2]
            server_socket.sendto("OK. " + "\tP2: " + str(p2), addr)
            # notify all players
            for addr in addrs:
                server_socket.sendto("zz,2," + str(p2[0]) + "," + str(p2[1]) + "," + str(p2[2]), addr)
        elif code == "13":
            print 'Getting pos#3'
            data = msg[2:]
            print data, addr
            data = data.split(',')
            for i in xrange(len(data) - 1):
                p3[i] = int(data[i])
            p3[2] = data[2]
            server_socket.sendto("OK. " + "\tP3: " + str(p3), addr)
            # notify all players
            for addr in addrs:
                server_socket.sendto("zz,3," + str(p3[0]) + "," + str(p3[1]) + "," + str(p3[2]), addr)
        elif code == "14":
            print 'Getting pos#4'
            data = msg[2:]
            print data, addr
            data = data.split(',')
            for i in xrange(len(data) - 1):
                p4[i] = int(data[i])
            p4[2] = data[2]
            server_socket.sendto("OK. " + "\tP4: " + str(p4), addr)
            # notify all players
            for addr in addrs:
                server_socket.sendto("zz,4," + str(p4[0]) + "," + str(p4[1]) + "," + str(p4[2]), addr)
        elif code == "20":
            print 'Getting keys'
            data = msg[2:]
            print data, addr
            data = data.split(',')
            for i in xrange(len(data)):
                keys[i] = True if data[i] == "True" else False
            server_socket.sendto("OK. " + "\tKEYS: " + str(keys), addr)

        elif code == "31":
            print 'Sending pos#1'
            server_socket.sendto(str(p1[0]) + "," + str(p1[1]) + "," + str(p1[2]), addr)
        elif code == "32":
            print 'Sending pos#2'
            server_socket.sendto(str(p2[0]) + "," + str(p2[1]) + "," + str(p2[2]), addr)
        elif code == "33":
            print 'Sending pos#3'
            server_socket.sendto(str(p3[0]) + "," + str(p3[1]) + "," + str(p3[2]), addr)
        elif code == "34":
            print 'Sending pos#4'
            server_socket.sendto(str(p4[0]) + "," + str(p4[1]) + "," + str(p4[2]), addr)

        elif code == "99":
            if players["1"] == addr:
                players["1"] = ""
                addrs.remove(addr)
                server_socket.sendto("Disconnected player #1", addr)
            elif players["2"] == addr:
                players["2"] = ""
                addrs.remove(addr)
                server_socket.sendto("Disconnected player #2", addr)
            elif players["3"] == addr:
                players["3"] = ""
                addrs.remove(addr)
                server_socket.sendto("Disconnected player #3", addr)
            elif players["4"] == addr:
                players["4"] = ""
                addrs.remove(addr)
                server_socket.sendto("Disconnected player #4", addr)

        else:
            server_socket.sendto("Wrong code. " + code , addr)
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print message


    # server_socket.sendto("OK. " + "\tP1: " + str(p1) + "\tKEYS: " + str(keys), addr)
