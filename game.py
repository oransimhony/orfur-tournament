#1 Import libraries
import pygame, math, random
from pygame.locals import *
import socket
import threading

my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

s_host = ("127.0.0.1", 8888)
pid = 0

p1 = [100, 100, 0.0]
p2 = [700, 100, 3.0]
p3 = [100, 500, 0.0]
p4 = [700, 500, 3.0]
players = [p1, p2, p3, p4]


class receiveThread(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        global p1
        global p2
        global p3
        global p4
        global playerpos

        print "Listening"
        while True:
            (data, addr) = my_socket.recvfrom(1024)
            print "The server sent: " + data
            data = data.split(",")
            code = data[0]

            if code == "zz":
                p = data[1]
                x = data[2]
                y = data[3]
                angle = data[4]
                if p == "1":
                    if pid == p:
                        players.remove(playerpos)
                        playerpos = [int(x), int(y), float(angle)]
                        players.append(playerpos)
                    else:
                        players.remove(p1)
                        p1 = [int(x), int(y), float(angle)]
                        players.append(p1)
                elif p == "2":
                    if pid == p:
                        players.remove(playerpos)
                        playerpos = [int(x), int(y), float(angle)]
                        players.append(playerpos)
                    else:
                        players.remove(p2)
                        p2 = [int(x), int(y), float(angle)]
                        players.append(p2)
                elif p == "3":
                    if pid == p:
                        players.remove(playerpos)
                        playerpos = [int(x), int(y), float(angle)]
                        players.append(playerpos)
                    else:
                        players.remove(p3)
                        p3 = [int(x), int(y), float(angle)]
                        players.append(p3)
                elif p == "4":
                    if pid == p:
                        players.remove(playerpos)
                        playerpos = [int(x), int(y), float(angle)]
                        players.append(playerpos)
                    else:
                        players.remove(p4)
                        p4 = [int(x), int(y), float(angle)]
                        players.append(p4)            # get_player_pos()

def initialConnect():
    pass
#
# class sendThread(threading.Thread):
#     def __init__(self, name):
#         threading.Thread.__init__(self)
#         self.name = name
#         initialConnect()
#     def run(self):
#         print "Starting connection"
#         connection()
#         print "Ending connection"

# connectionThread = sendThread("1")
lThread = receiveThread("1")


def initialConnect():
    global pid
    global lThread

    my_socket.sendto("00", s_host)
    (data, addr) = my_socket.recvfrom(1024)
    print "The server sent: " + data
    try:
        pid = data.split("#")[1]
        lThread.start()
        # lThread.run()
    except Exception as e:
        print e.message
        print "You can't connect the lobby right now"
        disconnect()
        my_socket.close()
        pygame.quit()
        exit(0)



# def connection():
#     get_player_pos()

def send_player_pos():
    s = ""
    # Send Player coordinates
    for playerp in players:
        if playerp is playerpos:
            for co in playerp:
                s += str(co) + ","
    my_socket.sendto("1" + str(pid) + s[:-1], s_host)
    # (data, addr) = my_socket.recvfrom(1024)
    # print "The server sent: " + data

def send_player_keys():
    s = ""
    # Send Keys
    for key in keys:
        s += str(key) + ","
    my_socket.sendto("2" + str(pid) + s[:-1], s_host)

def get_player_pos():
    global playerpos
    global oplayerspos
    global angle
    global oplayerangle

    oplayerspos = []
    oplayerangle = []

    # my_socket.sendto("3" + str(pid), s_host)
    (data, addr) = my_socket.recvfrom(1024)
    #print "The server sent: " + data
    pos = data.split(',')
    playerpos = [int(pos[0]), int(pos[1]), float(pos[2])]

    if pid == "1":
        my_socket.sendto("32", s_host)
        (data, addr) = my_socket.recvfrom(1024)
        #print "The server sent: " + data
        pos = data.split(',')
        oplayerspos.append([int(pos[0]), int(pos[1])])
        oplayerangle.append(float(pos[2]))
        my_socket.sendto("33", s_host)
        (data, addr) = my_socket.recvfrom(1024)
        #print "The server sent: " + data
        pos = data.split(',')
        oplayerspos.append([int(pos[0]), int(pos[1])])
        oplayerangle.append(float(pos[2]))
        my_socket.sendto("34", s_host)
        (data, addr) = my_socket.recvfrom(1024)
        #print "The server sent: " + data
        pos = data.split(',')
        oplayerspos.append([int(pos[0]), int(pos[1])])
        oplayerangle.append(float(pos[2]))
    elif pid == "2":
        my_socket.sendto("31", s_host)
        (data, addr) = my_socket.recvfrom(1024)
        #print "The server sent: " + data
        pos = data.split(',')
        oplayerspos.append([int(pos[0]), int(pos[1])])
        oplayerangle.append(float(pos[2]))
        my_socket.sendto("33", s_host)
        (data, addr) = my_socket.recvfrom(1024)
        #print "The server sent: " + data
        pos = data.split(',')
        oplayerspos.append([int(pos[0]), int(pos[1])])
        oplayerangle.append(float(pos[2]))
        my_socket.sendto("34", s_host)
        (data, addr) = my_socket.recvfrom(1024)
        #print "The server sent: " + data
        pos = data.split(',')
        oplayerspos.append([int(pos[0]), int(pos[1])])
        oplayerangle.append(float(pos[2]))
    elif pid == "3":
        my_socket.sendto("31", s_host)
        (data, addr) = my_socket.recvfrom(1024)
        #print "The server sent: " + data
        pos = data.split(',')
        oplayerspos.append([int(pos[0]), int(pos[1])])
        oplayerangle.append(float(pos[2]))
        my_socket.sendto("32", s_host)
        (data, addr) = my_socket.recvfrom(1024)
        #print "The server sent: " + data
        pos = data.split(',')
        oplayerspos.append([int(pos[0]), int(pos[1])])
        oplayerangle.append(float(pos[2]))
        my_socket.sendto("34", s_host)
        (data, addr) = my_socket.recvfrom(1024)
        #print "The server sent: " + data
        pos = data.split(',')
        oplayerspos.append([int(pos[0]), int(pos[1])])
        oplayerangle.append(float(pos[2]))
    elif pid == "4":
        my_socket.sendto("31", s_host)
        (data, addr) = my_socket.recvfrom(1024)
        #print "The server sent: " + data
        pos = data.split(',')
        oplayerspos.append([int(pos[0]), int(pos[1])])
        oplayerangle.append(float(pos[2]))
        my_socket.sendto("32", s_host)
        (data, addr) = my_socket.recvfrom(1024)
        oplayerangle.append(float(pos[2]))
        #print "The server sent: " + data
        pos = data.split(',')
        oplayerspos.append([int(pos[0]), int(pos[1])])
        oplayerangle.append(float(pos[2]))
        my_socket.sendto("33", s_host)
        (data, addr) = my_socket.recvfrom(1024)
        #print "The server sent: " + data
        pos = data.split(',')
        oplayerspos.append([int(pos[0]), int(pos[1])])
        oplayerangle.append(float(pos[2]))

def disconnect():
    my_socket.sendto("99", s_host)

#2 Initialize the game
pygame.init()
pygame.mixer.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Top Down Shooter")
flags = screen.get_flags()
keys = [False, False, False, False]
arrow_speed = 40
player_speed = 6
clock = pygame.time.Clock()
frame = 0

#3 Load images
player = pygame.image.load('player.png') # 62 41
player = pygame.transform.scale(player, (62, 41))
arrow = pygame.image.load('bullet1.png')
arrow = pygame.transform.scale(arrow, (14, 6))
background = pygame.image.load('bg1.jpg')
background = pygame.transform.scale(background, (width, height))


# connectionThread.start()
initialConnect()

if pid == "1":
    playerpos = [p1[0], p1[1], p1[2]]
    players.remove(p1)
    players.append(playerpos)
elif pid == "2":
    playerpos = [p2[0], p2[1], p2[2]]
    players.remove(p2)
    players.append(playerpos)
elif pid == "3":
    playerpos = [p3[0], p3[1], p3[2]]
    players.remove(p3)
    players.append(playerpos)
elif pid == "4":
    playerpos = [p4[0], p4[1], p4[2]]
    players.remove(p4)
    players.append(playerpos)

oplayerspos = []
oplayerangle = []
arrows = []

#4 Keep looping through
running = 1
exitcode = 0
while running:
    #5 Clear the screen before drawing it agains
    screen.fill((255, 255, 255))
    screen.blit(background, (0, 0))
    #6.1 Set player position and rotation
    # position = pygame.mouse.get_pos()
    # playerpos[2] = math.atan2(position[1] - (playerpos[1] + 31), position[0] - (playerpos[0] + 20))
    # playerrot = pygame.transform.rotate(player, 360-playerpos[2] * 57.29)
    # playerpos1 = (playerpos[0] - playerrot.get_rect().width / 2, playerpos[1] - playerrot.get_rect().height / 2)
    # screen.blit(playerrot, playerpos1)
    #
    # # for pos in oplayerspos:
    # #     oplayerrot = pygame.transform.rotate(player, 360-oplayerangle[i] * 57.29)
    # #     oplayerpos1 = (pos[0] - oplayerrot.get_rect().width / 2, pos[1] - oplayerrot.get_rect().height / 2)
    # #     screen.blit(oplayerrot, oplayerpos1)
    # #     i += 1
    # playerrot = pygame.transform.rotate(player, 360 - p2[2] * 57.29)
    # playerpos1 = (p2[0] - playerrot.get_rect().width / 2, p2[1] - playerrot.get_rect().height / 2)
    # screen.blit(playerrot, playerpos1)
    #
    # playerrot = pygame.transform.rotate(player, 360 - p3[2] * 57.29)
    # playerpos1 = (p3[0] - playerrot.get_rect().width / 2, p3[1] - playerrot.get_rect().height / 2)
    # screen.blit(playerrot, playerpos1)
    #
    # playerrot = pygame.transform.rotate(player, 360 - p4[2] * 57.29)
    # playerpos1 = (p4[0] - playerrot.get_rect().width / 2, p4[1] - playerrot.get_rect().height / 2)
    # screen.blit(playerrot, playerpos1)

    for playerp in players:
        if playerp is playerpos:
            position = pygame.mouse.get_pos()
            playerp[2] = math.atan2(position[1] - (playerp[1] + 31), position[0] - (playerp[0] + 20))
        playerrot = pygame.transform.rotate(player, 360 - playerp[2] * 57.29)
        playerpos1 = (playerp[0] - playerrot.get_rect().width / 2, playerp[1] - playerrot.get_rect().height / 2)
        screen.blit(playerrot, playerpos1)

    for bullet in arrows:
        index = 0
        velx = math.cos(bullet[0]) * arrow_speed
        vely = math.sin(bullet[0]) * arrow_speed
        bullet[1] += velx
        bullet[2] += vely
        if bullet[1] < -64 or bullet[1] > width or bullet[2] < -64 or bullet[2] > height:
            arrows.pop(index)
        index += 1
        for projectile in arrows:
            arrow1 = pygame.transform.rotate(arrow, 360-projectile[0]*57.29)
            screen.blit(arrow1, (projectile[1], projectile[2]))

    #7 Update the screen
    pygame.display.flip()

    #8 Loop through the events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            disconnect()
            my_socket.close()
            pygame.quit()
            exit(0)
        if event.type == pygame.KEYDOWN:
            if event.key == K_w:
                keys[0] = True
            elif event.key == K_a:
                keys[1] = True
            elif event.key == K_s:
                keys[2] = True
            elif event.key == K_d:
                keys[3] = True
            elif event.key == K_f:
                # toggle fullscreen by pressing F key.
                if flags & FULLSCREEN == False:
                    flags |= FULLSCREEN
                    pygame.display.set_mode((width, height), flags)
        if event.type == pygame.KEYUP:
            if event.key == K_w:
                keys[0] = False
            elif event.key == K_a:
                keys[1] = False
            elif event.key == K_s:
                keys[2] = False
            elif event.key == K_d:
                keys[3] = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            position = pygame.mouse.get_pos()
            arrows.append([math.atan2(position[1] - (playerpos[1] + 31), position[0] - (playerpos[0] + 20)), playerpos[0] + 32, playerpos1[1] + 32])
    #9 Move player
    if keys[0]:
        playerpos[1] -= player_speed
        send_player_pos()
    elif keys[2]:
        playerpos[1] += player_speed
        send_player_pos()
    if keys[1]:
        playerpos[0] -= player_speed
        send_player_pos()
    elif keys[3]:
        playerpos[0] += player_speed
        send_player_pos()

    clock.tick(30)
    # frame += 1
    # if frame == 15:
    #     print p1
    #     print p2
    #     print p3
    #     print p4
    #     print playerpos
    #     frame = 0


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            disconnect()
            my_socket.close()
            pygame.quit()
            exit(0)
    pygame.display.flip()
