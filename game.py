import math
import socket
import threading

import pygame
from pygame.locals import *

my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

s_host = ("77.139.180.35", 8888)
pid = 0

p1 = [100, 100, 0.0]
p2 = [700, 100, 3.0]
p3 = [100, 500, 0.0]
p4 = [700, 500, 3.0]
player_positions = [p1, p2, p3, p4]

p1_health = 30
p2_health = 30
p3_health = 30
p4_health = 30
players_health = [p1_health, p2_health, p3_health, p4_health]

bullets = []
player_pos = []

mouse = []


class ReceiveThread(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        global p1
        global p2
        global p3
        global p4
        global player_positions
        global player_pos
        global bullets

        print "Listening"
        while True:
            try:
                (data, addr) = my_socket.recvfrom(8192)
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
                            player_positions.remove(player_pos)
                            player_pos = [int(x), int(y), float(angle)]
                            player_positions.insert(int(p) - 1, player_pos)
                        else:
                            player_positions.remove(p1)
                            p1 = [int(x), int(y), float(angle)]
                            player_positions.insert(int(p) - 1, p1)
                    elif p == "2":
                        if pid == p:
                            player_positions.remove(player_pos)
                            player_pos = [int(x), int(y), float(angle)]
                            player_positions.insert(int(p) - 1, player_pos)
                        else:
                            player_positions.remove(p2)
                            p2 = [int(x), int(y), float(angle)]
                            player_positions.insert(int(p) - 1, p2)
                    elif p == "3":
                        if pid == p:
                            player_positions.remove(player_pos)
                            player_pos = [int(x), int(y), float(angle)]
                            player_positions.insert(int(p) - 1, player_pos)
                        else:
                            player_positions.remove(p3)
                            p3 = [int(x), int(y), float(angle)]
                            player_positions.insert(int(p) - 1, p3)
                    elif p == "4":
                        if pid == p:
                            player_positions.remove(player_pos)
                            player_pos = [int(x), int(y), float(angle)]
                            player_positions.insert(int(p) - 1, player_pos)
                        else:
                            player_positions.remove(p4)
                            p4 = [int(x), int(y), float(angle)]
                            player_positions.insert(int(p) - 1, p4)
                elif code == "B":
                    if data[1] != "[]":
                        bullets_data = data[1][1:-1]
                        bullets_data = bullets_data.split("#")
                        bullets = []
                        for bullet_data in bullets_data:
                            bullet_data = bullet_data[1:-1]
                            bullet_data = bullet_data.split("$")
                            bullets.append(
                                [str(bullet_data[0]), float(bullet_data[1]), int(bullet_data[2]), int(bullet_data[3])]
                            )

                elif code == "hp":
                    p = int(data[1])
                    hp = int(data[2])
                    players_health[p - 1] = hp
                    if players_health[p - 1] <= 0:
                        player_positions[p - 1] = None
                    # if p == 1:
                    #     p1_health = hp
                    # elif p == 2:
                    #     p2_health = hp
                    # elif p == 3:
                    #     p3_health = hp
                    # elif p == 4:
                    #     p4_health = hp

            except Exception as error:
                print error.message
                print "Thread ERR"
                pygame.quit()
                exit(0)


lThread = ReceiveThread("1")


def initial_connect():
    global pid
    global lThread

    my_socket.sendto("00", s_host)
    (data, addr) = my_socket.recvfrom(1024)
    print "The server sent: " + data
    try:
        pid = data.split("#")[1]
        lThread.start()
    except Exception as error:
        print error.message
        print "You can't connect the lobby right now"
        disconnect()
        my_socket.close()
        pygame.quit()
        exit(0)


def send_player_pos():
    s = ""
    # Send Player coordinates
    for player_position in player_positions:
        if player_position is player_pos:
            for co in player_position:
                s += str(co) + ","
    my_socket.sendto("1" + str(pid) + s[:-1], s_host)


def send_player_keys():
    s = ""
    # Send Keys
    for key in keys:
        s += str(key) + ","
    my_socket.sendto("2" + str(pid) + s[:-1], s_host)


def send_bullet(bullet_info):
    s = ""
    for n in bullet_info:
        s += str(n) + ","

    my_socket.sendto("40" + s[:-1], s_host)


def send_mouse(angle):
    my_socket.sendto("6" + pid + str(angle), s_host)


def delete_bullet(bullet_info):
    s = ""
    for n in bullet_info:
        s += str(n) + ","
    my_socket.sendto("50" + s[:-1], s_host)


def disconnect():
    my_socket.sendto("99", s_host)


def enemy_hit(enemy_id):
    my_socket.sendto("7" + str(enemy_id), s_host)

pygame.init()
pygame.mixer.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Top Down Shooter")
flags = screen.get_flags()
keys = [False, False, False, False]
bullet_speed = 12
player_speed = 6
clock = pygame.time.Clock()
frame = 0

player_img = pygame.image.load('player.png')
player_img = pygame.transform.scale(player_img, (62, 41))
# bullet_img = pygame.image.load('bullet1.png')
# bullet_img = pygame.transform.scale(bullet_img, (14, 6))
bullet_img = pygame.image.load('bullet.png').convert()
bullet_img.set_colorkey((255, 255, 255))
bullet_img = pygame.transform.scale(bullet_img, (13, 5))
background_img = pygame.image.load('bg1.jpg')
background_img = pygame.transform.scale(background_img, (width, height))
bad_guys = []

ammo = pygame.transform.rotate(bullet_img, 90)
ammo = pygame.transform.scale2x(ammo)
shot = 0

initial_connect()

if pid == "1":
    player_pos = [p1[0], p1[1], p1[2]]
    player_positions.remove(p1)
    player_positions.append(player_pos)
elif pid == "2":
    player_pos = [p2[0], p2[1], p2[2]]
    player_positions.remove(p2)
    player_positions.append(player_pos)
elif pid == "3":
    player_pos = [p3[0], p3[1], p3[2]]
    player_positions.remove(p3)
    player_positions.append(player_pos)
elif pid == "4":
    player_pos = [p4[0], p4[1], p4[2]]
    player_positions.remove(p4)
    player_positions.append(player_pos)

oplayerspos = []
oplayerangle = []
arrows = []

running = 1
exitcode = 0
while running:
    try:
        screen.blit(background_img, (0, 0))
    except Exception as e:
        print e.message
        disconnect()
        my_socket.close()
        exit(0)
    new_bad_guys = []
    id = 1
    for playerp in player_positions:
        if playerp is player_pos:
            if playerp is not None:
                position = pygame.mouse.get_pos()
                playerp[2] = math.atan2(position[1] - (playerp[1] + 31), position[0] - (playerp[0] + 20))
                playerrot = pygame.transform.rotate(player_img, 360 - playerp[2] * 57.29)
                playerpos1 = (playerp[0] - playerrot.get_rect().width / 2, playerp[1] - playerrot.get_rect().height / 2)
                screen.blit(playerrot, playerpos1)
                if position != mouse:
                    send_mouse(playerp[2])
                    mouse = position
            id += 1
        else:
            if playerp is not None:
                playerrot = pygame.transform.rotate(player_img, 360 - playerp[2] * 57.29)
                playerpos1 = (playerp[0] - playerrot.get_rect().width / 2, playerp[1] - playerrot.get_rect().height / 2)
                screen.blit(playerrot, playerpos1)
                new_bad_guys.append([screen.blit(playerrot, playerpos1), id])
            else:
                new_bad_guys.append(bad_guys[id - 2])
            id += 1
    bad_guys = new_bad_guys
    for bullet in bullets:
        if bullet[0] == pid:
            delete_bullet(bullet)
            index = 0
            velx = math.cos(bullet[1]) * bullet_speed
            vely = math.sin(bullet[1]) * bullet_speed
            bullet[2] += int(velx)
            bullet[3] += int(vely)
            if bullet[2] < -64 or bullet[2] > width or bullet[3] < -64 or bullet[3] > height:
                bullets.pop(index)
                shot -= 1 if shot > 0 else 0
            else:
                send_bullet(bullet)
            index += 1
        for projectile in bullets:
            bullet1 = pygame.transform.rotate(bullet_img, 360 - projectile[1] * 57.29)
            screen.blit(bullet1, (projectile[2], projectile[3]))

    for i in xrange(5 - shot):
        screen.blit(ammo, (20 + i * 15, 560))

    for badguy, id in bad_guys:
        index1 = 0
        for bullet in bullets:
            bullrect = pygame.Rect(bullet_img.get_rect())
            bullrect.left = bullet[2]
            bullrect.top = bullet[3]
            if badguy.colliderect(bullrect):
                # bad_guys.pop(index)
                print "HIT"
                players_health[1] -= 1
                print enemy_hit(id)
                # print player_positions
                bullets.pop(index1)
                index1 -= 1
                shot -= 1 if shot > 0 else 0
                delete_bullet(bullet)
                break
            index1 += 1

    pygame.display.flip()

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
                flags ^= FULLSCREEN
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
            b = [pid,
                 math.atan2(position[1] - (player_pos[1] + 31), position[0] - (player_pos[0] + 20)),
                 player_pos[0] + 31,
                 player_pos[1] + 20]
            bc = [bullet for bullet in bullets if bullet[0] == pid]
            if len(bc) <= 3:
                send_bullet(b)
                shot += 1

    moved = False
    if keys[0]:
        player_pos[1] -= player_speed
        moved = True
    elif keys[2]:
        player_pos[1] += player_speed
        moved = True
    if keys[1]:
        player_pos[0] -= player_speed
        moved = True
    elif keys[3]:
        player_pos[0] += player_speed
        moved = True
    if moved:
        send_player_pos()
    clock.tick(30)
