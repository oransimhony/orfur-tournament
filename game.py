import math
import socket
import threading
import random

import pygame
from pygame.locals import *

my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

hostname = raw_input("Hostname: ")
if "l" in hostname:
    s_host = ("127.0.0.1", 8888)
else:
    s_host = (hostname, 8888)

debug = raw_input("Debug Mode? (Y/N)")
debug = True if "y" in debug.lower() else False

pid = 0
dead = False

p1 = None  # [100, 100, 0.0]
p2 = None  # [700, 100, 3.0]
p3 = None  # [100, 500, 0.0]
p4 = None  # [700, 500, 3.0]aa
player_positions = [p1, p2, p3, p4]

p1_health = 30
p2_health = 30
p3_health = 30
p4_health = 30
players_health = [p1_health, p2_health, p3_health, p4_health]

bullets = []
player_pos = []

# player_rect = Rect(0, 0, 0, 0)

mouse = []

messages = []

player_won_id = -1


def restart_values():
    global p1
    global p2
    global p3
    global p4
    global p1_health
    global p2_health
    global p3_health
    global p4_health
    global bullets
    global player_positions
    global player_pos
    global new
    global messages
    global dead
    global health
    global shot
    global keys

    messages = []

    p1 = None
    p2 = None
    p3 = None
    p4 = None

    player_positions = [p1, p2, p3, p4]
    player_pos = []

    if pid == "1":
        if p1 is not None:
            player_pos = [p1[0], p1[1], p1[2]]
            player_positions.remove(p1)
            player_positions.append(player_pos)
        else:
            player_pos = None
            player_positions.remove(p1)
            player_positions.append(player_pos)
    elif pid == "2":
        if p1 is not None:
            player_pos = [p1[0], p1[1], p1[2]]
            player_positions.remove(p2)
            player_positions.append(player_pos)
        else:
            player_pos = None
            player_positions.remove(p2)
            player_positions.append(player_pos)
    elif pid == "3":
        if p1 is not None:
            player_pos = [p1[0], p1[1], p1[2]]
            player_positions.remove(p3)
            player_positions.append(player_pos)
        else:
            player_pos = None
            player_positions.remove(p3)
            player_positions.append(player_pos)
    elif pid == "4":
        if p1 is not None:
            player_pos = [p1[0], p1[1], p1[2]]
            player_positions.remove(p4)
            player_positions.append(player_pos)
        else:
            player_pos = None
            player_positions.remove(p4)
            player_positions.append(player_pos)

    p1_health = 30
    p2_health = 30
    p3_health = 30
    p4_health = 30
    health = 30
    shot = 0

    bullets = []

    new = False
    dead = []
    keys = [False, False, False, False]


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

        if debug:
            print "Listening"
        while True:
            try:
                (data, addr) = my_socket.recvfrom(8192)
            except Exception as ex:
                template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                message = template.format(type(ex).__name__, ex.args)
                print message
                data, addr = "", ()
            if data != "":
                if debug:
                    print "The server sent: " + data
                data = data.split(",")
                code = data[0]

                if code == "s":
                    restart_values()

                elif code == "zz":
                    p = data[1]
                    x = data[2]
                    if x != "None":
                        if debug:
                            print player_pos, player_positions
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

                    else:
                        if debug:
                            print player_pos, player_positions
                        if p == "1":
                            if pid == p:
                                player_positions.remove(player_pos)
                                player_pos = None
                                player_positions.insert(int(p) - 1, player_pos)
                            else:
                                player_positions.remove(p1)
                                p1 = None
                                player_positions.insert(int(p) - 1, p1)
                        elif p == "2":
                            if pid == p:
                                player_positions.remove(player_pos)
                                player_pos = None
                                player_positions.insert(int(p) - 1, player_pos)
                            else:
                                player_positions.remove(p2)
                                p2 = None
                                player_positions.insert(int(p) - 1, p2)
                        elif p == "3":
                            if pid == p:
                                player_positions.remove(player_pos)
                                player_pos = None
                                player_positions.insert(int(p) - 1, player_pos)
                            else:
                                player_positions.remove(p3)
                                p3 = None
                                player_positions.insert(int(p) - 1, p3)
                        elif p == "4":
                            if pid == p:
                                player_positions.remove(player_pos)
                                player_pos = None
                                player_positions.insert(int(p) - 1, player_pos)
                            else:
                                player_positions.remove(p4)
                                p4 = None
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

                elif code == "T":
                    global messages
                    text = data[1]
                    x = int(data[2])
                    y = int(data[3])
                    messages.append(make_text(text, x, y, (33, 33, 33)))

                elif code == "hp":
                    global dead
                    global health
                    p = int(data[1])
                    hp = int(data[2])
                    hitter = data[3]
                    players_health[p - 1] = hp
                    if int(p) == int(pid):
                        health = hp
                    if players_health[p - 1] <= 0:
                        player_positions[p - 1] = None
                        if int(p) == int(pid):
                            dead = True
                        alive = 0
                        for pos in player_positions:
                            if pos is not None:
                                alive += 1
                        if alive == 1:
                            global player_won_id
                            player_won_id = 1
                            for pos in player_positions:
                                if pos is not None:
                                    won(player_won_id)
                                    break
                                player_won_id += 1
                        killed(hitter, str(p))

                    # if p == 1:
                    #     p1_health = hp
                    # elif p == 2:
                    #     p2_health = hp
                    # elif p == 3:
                    #     p3_health = hp
                    # elif p == 4:
                    #     p4_health = hp

            # except Exception as error:
            #     global running
            #     print error.message
            #     print "Thread ERR"
            #     running = False
            #     disconnect()
            #     my_socket.close()
            #     pygame.quit()
            #     exit(0)


lThread = ReceiveThread("1")


def initial_connect():
    global pid
    global lThread

    my_socket.sendto("00", s_host)
    (data, addr) = my_socket.recvfrom(1024)
    if debug:
        print "The server sent: " + data
    try:
        pid = data.split("#")[1]
        lThread.daemon = True
        lThread.start()
    except Exception as error:
        global running
        print error.message
        print "You can't connect the lobby right now"
        running = False
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


def enemy_hit(enemy_id, hitter):
    if int(hitter) == int(pid):
        my_socket.sendto("7" + str(enemy_id) + "," + pid, s_host)


def killed(killer, killed_p):
    if int(killer) == int(pid):
        my_socket.sendto("2" + str(killed_p) + "," + killer, s_host)


def won(player_won):
    if int(player_won) == int(pid):
        my_socket.sendto("20," + "Player #" + str(player_won) + " won this round,5,400", s_host)
        my_socket.sendto("20," + "Congratulations!,5,400", s_host)


def new_round():
    if debug:
        print player_won_id, pid
    if int(player_won_id) == int(pid):
        if debug:
            print "NEW ROUND SENTTTTTTTTTTTTTT"
        my_socket.sendto("90", s_host)


def make_text(text_message, x, y, text_color):
    text = font.render(text_message, True, text_color, (255, 255, 255))
    text_rect = text.get_rect()
    text_rect.left = x
    text_rect.top = y
    if "SPECTATING" not in text_message:
        offset_messages()
    if "Congrat" in text_message or "won" in text_message:
        return [text, text_rect, time_to_fade * 2, True]
    return [text, text_rect, time_to_fade, False]


def offset_messages():
    index = 0
    for message in messages:
        text_rect = message[1]
        text_rect.top -= text_space
        index += 1

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

player_img = pygame.image.load('player1.png')
player_img = pygame.transform.scale(player_img, (62, 41))
# bullet_img = pygame.image.load('bullet1.png')
# bullet_img = pygame.transform.scale(bullet_img, (14, 6))
bullet_img = pygame.image.load('bullet.png').convert()
bullet_img.set_colorkey((255, 255, 255))
bullet_img = pygame.transform.scale(bullet_img, (13, 5))
bg = random.randint(1, 5)
# if bg == 1:
#     background_img = pygame.image.load('bg1.jpg')
# elif bg == 2:
#     background_img = pygame.image.load('bg2.png')
# elif bg == 3:
#     background_img = pygame.image.load('bg3.png')
# else:
#     background_img = pygame.image.load('bg4.jpg')
background_img = pygame.image.load('bg1.jpg')
background_img = pygame.transform.scale(background_img, (width, height))
youdied_img = pygame.image.load('youDied.jpg')
youdied_img = pygame.transform.scale(youdied_img, (800, 600))
bad_guys = []

ammo = pygame.transform.rotate(bullet_img, 90)
ammo = pygame.transform.scale2x(ammo)
shot = 0

font = pygame.font.SysFont(None, 22)
text_space = 25
time_to_fade = 3000

health = 30
max_health = 30

initial_connect()

# obstacles = [[300, 200, 50, 70], [360, 280, 50, 70]]
# obstacles = [pygame.draw.rect(screen, (300, 200), (255, 0, 0), (50, 70)), pygame.draw.rect(screen, (150, 600), (255, 0, 0), (34, 57))]

if pid == "1":
    if p1 is not None:
        player_pos = [p1[0], p1[1], p1[2]]
        player_positions.remove(p1)
        player_positions.append(player_pos)
    else:
        player_pos = None
        player_positions.remove(p1)
        player_positions.append(player_pos)
elif pid == "2":
    if p1 is not None:
        player_pos = [p1[0], p1[1], p1[2]]
        player_positions.remove(p2)
        player_positions.append(player_pos)
    else:
        player_pos = None
        player_positions.remove(p2)
        player_positions.append(player_pos)
elif pid == "3":
    if p1 is not None:
        player_pos = [p1[0], p1[1], p1[2]]
        player_positions.remove(p3)
        player_positions.append(player_pos)
    else:
        player_pos = None
        player_positions.remove(p3)
        player_positions.append(player_pos)
elif pid == "4":
    if p1 is not None:
        player_pos = [p1[0], p1[1], p1[2]]
        player_positions.remove(p4)
        player_positions.append(player_pos)
    else:
        player_pos = None
        player_positions.remove(p4)
        player_positions.append(player_pos)

oplayerspos = []
oplayerangle = []
arrows = []

new = False


running = 1
exitcode = 0
while running:
    player_rect = screen.blit(screen, (0, 0))
    try:
        screen.blit(background_img, (0, 0))
        # if dead:
        #     screen.blit(youdied_img, (0, 0))
        #     time.sleep(5000)
        #     print "QUITTING"
        #     disconnect()
        #     print "DISCONNECTED"
        #     my_socket.close()
        #     pygame.quit()
        #     print "SOCKET AND PYGAME CLOSED"
        #     exit(0)
    except Exception as e:
        print "QUITTING"
        disconnect()
        print "DISCONNECTED"
        my_socket.close()
        pygame.quit()
        print "SOCKET AND PYGAME CLOSED"
        exit(0)
    # new_bad_guys = []
    players_rects = []
    id = 1
    for playerp in player_positions:
        if playerp is player_pos:
            if playerp is not None:
                # global player_rect
                position = pygame.mouse.get_pos()
                playerp[2] = math.atan2(position[1] - (playerp[1] + 31), position[0] - (playerp[0] + 20))
                playerrot = pygame.transform.rotate(player_img, 360 - playerp[2] * 57.29)
                playerpos1 = (playerp[0] - playerrot.get_rect().width / 2, playerp[1] - playerrot.get_rect().height / 2)
                screen.blit(playerrot, playerpos1)
                players_rects.append([screen.blit(playerrot, playerpos1), id])
                player_rect = screen.blit(playerrot, playerpos1)
                if position != mouse:
                    send_mouse(playerp[2])
                    mouse = position
                    point1 = (mouse[0], mouse[1])
                    point2 = (mouse[0], player_pos[1] + 12)
                    point3 = (player_pos[0] + 34 + 62 * (playerp[2])/math.pi, player_pos[1] + 12 + 41 * (playerp[2])/math.pi)
            else:
                players_rects.append([None, id])
            id += 1
        else:
            if playerp is not None:
                playerrot = pygame.transform.rotate(player_img, 360 - playerp[2] * 57.29)
                playerpos1 = (playerp[0] - playerrot.get_rect().width / 2, playerp[1] - playerrot.get_rect().height / 2)
                screen.blit(playerrot, playerpos1)
                players_rects.append([screen.blit(playerrot, playerpos1), id])
                # new_bad_guys.append([screen.blit(playerrot, playerpos1), id])
            else:
                # new_bad_guys.append(bad_guys[id - 2])
                players_rects.append([None, id])
            id += 1
    # bad_guys = new_bad_guys
    # ind = 0
    # for obstacle in obstacles:
    #     pygame.draw.rect(screen, (0, 0, 0), Rect(obstacle[0], obstacle[1], obstacle[2], obstacle[3]))
    #     pygame.display.flip()
    #     # screen.blit(obstacle, obstacles_coord[ind])
    #     ind += 1

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

    for message in messages:
        text = message[0]
        text_rect = message[1]
        message[2] -= 50
        if message[2] <= 0:
            messages.remove(message)
            if message[3] and not new:
                new = True
                new_round()
        else:
            # pygame.draw.rect(screen, (255, 255, 255), text_rect)
            screen.blit(text, text_rect)

    if dead:
        # print "SPECTATING"
        text, text_rect, time_to_fade, special = make_text("SPECTATING", width / 2, 700, (33, 33, 33))  # (255, 230, 153)
        # print text, text_rect
        screen.blit(text, text_rect)

    pygame.draw.rect(screen, (0, 255, 0), (20, 530, int(100 * (float(health) / max_health)), 20))
    pygame.draw.rect(screen, (255, 0, 0), (20 + int(100 * (float(health) / max_health)), 530, int(100 * (1 - (float(health) / max_health))), 20))
    pygame.draw.rect(screen, (0, 0, 0), (20, 530, 100, 20), 5)

    for i in xrange(5 - shot):
        screen.blit(ammo, (20 + i * 15, 560))

    # for badguy, player_id in bad_guys:
    #     for bullet in bullets:
    #         bullrect = pygame.Rect(bullet_img.get_rect())
    #         bullrect.left = bullet[2]
    #         bullrect.top = bullet[3]
    #         if badguy.colliderect(bullrect):
    #             # print "HIT"
    #             if int(player_id) != int(bullet[0]) and player_positions[player_id - 1] is not None:
    #                 players_health[player_id - 1] -= 1
    #                 enemy_hit(player_id)
    #                 if bullet in bullets:
    #                     bullets.remove(bullet)
    #                 shot -= 1 if shot > 0 else 0
    #                 delete_bullet(bullet)

    if debug:
        for players_rect, player_id in players_rects:
            if players_rect is not None:
                pygame.draw.rect(screen, (255, 0, 0), players_rect, 1)
        if player_pos is not None:
            # pygame.draw.line(screen, (0, 255, 0), (mouse[0], mouse[1]), (player_pos[0] + 34, player_pos[1] + 12))
            pygame.draw.line(screen, (0, 255, 0), point1, point3)
            pygame.draw.line(screen, (0, 255, 0), point1, point2)
            pygame.draw.line(screen, (0, 255, 0), point3, point2)
            # pygame.draw.polygon(screen, (0, 255, 0), [[mouse[0], mouse[1]], [player_pos[0], player_pos[1]], [[player_pos[0], mouse[1]]]], 1)

    for players_rect, player_id in players_rects:
        if players_rect is not None:
            for bullet in bullets:
                bullrect = pygame.Rect(bullet_img.get_rect())
                bullrect.left = bullet[2]
                bullrect.top = bullet[3]
                if players_rect.colliderect(bullrect):
                    # print "HIT"
                    if int(player_id) != int(bullet[0]) and player_positions[player_id - 1] is not None:
                        players_health[player_id - 1] -= 1
                        enemy_hit(player_id, bullet[0])
                        if bullet in bullets:
                            bullets.remove(bullet)
                        shot -= 1 if shot > 0 else 0
                        delete_bullet(bullet)

    # if dead:
    #     screen.blit(youdied_img, (0, 0))

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if debug:
                print "QUITTING"
                disconnect()
                print "DISCONNECTED"
                my_socket.close()
                pygame.quit()
                print "SOCKET AND PYGAME CLOSED"
                exit(0)
            else:
                disconnect()
                my_socket.close()
                pygame.quit()
                exit(0)
        if event.type == pygame.KEYDOWN:
            if not dead:
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
        if event.type == pygame.KEYUP and not dead:
            if event.key == K_w:
                keys[0] = False
            elif event.key == K_a:
                keys[1] = False
            elif event.key == K_s:
                keys[2] = False
            elif event.key == K_d:
                keys[3] = False
        if event.type == pygame.MOUSEBUTTONDOWN and not dead:
            position = pygame.mouse.get_pos()
            b = [pid,
                 math.atan2(position[1] - (player_pos[1] + 12), position[0] - (player_pos[0] + 34)),  # math.atan2(position[1] - (player_pos[1] + 31), position[0] - (player_pos[0] + 20)),
                 player_pos[0] + 34,
                 player_pos[1] + 12]
            bc = [bullet for bullet in bullets if bullet[0] == pid]
            if len(bc) <= 3:
                send_bullet(b)
                shot += 1

    moved = False
    direction = -1
    if keys[0]:
        player_pos[1] -= player_speed
        direction = 0
        moved = True
    elif keys[2]:
        player_pos[1] += player_speed
        direction = 2
        moved = True
    if keys[1]:
        player_pos[0] -= player_speed
        direction = 1
        moved = True
    elif keys[3]:
        player_pos[0] += player_speed
        direction = 3
        moved = True

    #
    # if keys[0]:
    #     player_pos[1] = player_pos[1] - player_speed if player_pos[1] - player_speed - player_rect.height / 2 > 0 else 0
    #     direction = 0
    #     moved = True
    # elif keys[2]:
    #     player_pos[1] = player_pos[1] + player_speed if player_pos[1] + player_speed + player_rect.height / 2 < height else height
    #     direction = 2
    #     moved = True
    # if keys[1]:
    #     player_pos[0] = player_pos[0] - player_speed if player_pos[0] - player_speed - player_rect.width / 2 > 0 else 0
    #     direction = 1
    #     moved = True
    # elif keys[3]:
    #     player_pos[0] = player_pos[0] + player_speed if player_pos[0] + player_speed + player_rect.width / 2 < width else width
    #     direction = 3
    #     moved = True

    # for obstacle in obstacles:
    #     if player_rect.colliderect(obstacle):
    #         print "COLLIDED", direction
    #         if direction == 0:
    #             player_pos[1] += player_speed
    #         elif direction == 1:
    #             player_pos[0] += player_speed
    #         elif direction == 2:
    #             player_pos[1] -= player_speed
    #         elif direction == 3:
    #             player_pos[0] += player_speed
    #         moved = False
    if moved:
        send_player_pos()
        point1 = (mouse[0], mouse[1])
        point2 = (mouse[0], player_pos[1] + 12)
        point3 = (player_pos[0] + 34, player_pos[1] + 12)
    clock.tick(30)
