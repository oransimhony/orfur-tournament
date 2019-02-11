# Version 1.0.2 by Oran Simhony

import math
import pickle
import random
import socket
import sys
import threading

import pygame
from pygame.locals import *

from classes import *

my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
if len(sys.argv) >= 2:
    print "Address: ", sys.argv[1]
    s_host = (sys.argv[1], 8888)
else:
    print "Address: 127.0.0.1"
    s_host = ("127.0.0.1", 8888)

# hostname = raw_input("Hostname: ")
# if "l" in hostname:
#     s_host = ("127.0.0.1", 8888)
# else:
#     s_host = (hostname, 8888)
#
# debug = raw_input("Debug Mode? (Y/N)")
# debug = True if "y" in debug.lower() else False
debug = False

mute = True

pid = 0
dead = False

p1 = Player(1)
p2 = Player(2)
p3 = Player(3)
p4 = Player(4)

my_player = None

# p1 = None  # [100, 100, 0.0]
# p2 = None  # [700, 100, 3.0]
# p3 = None  # [100, 500, 0.0]
# p4 = None  # [700, 500, 3.0]
player_positions = [p1, p2, p3, p4]

p1_health = 30
p2_health = 30
p3_health = 30
p4_health = 30
players_health = [p1_health, p2_health, p3_health, p4_health]

bullets = []
player_pos = None

mouse = [0, 0]

messages = []

player_won_id = -1

collectible_timer = 5000
collectibles = []


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
    global collectibles
    global my_player

    messages = []

    p1 = Player(1)
    p2 = Player(2)
    p3 = Player(3)
    p4 = Player(4)

    # p1 = None
    # p2 = None
    # p3 = None
    # p4 = None

    player_positions = [p1, p2, p3, p4]
    player_pos = None
    my_player = None

    if pid == "1":
        my_player = p1
        # if p1 is not None:
        #     player_pos = [p1[0], p1[1], p1[2]]
        #     player_positions.remove(p1)
        #     player_positions.append(player_pos)
        # else:
        #     player_pos = None
        #     player_positions.remove(p1)
        #     player_positions.append(player_pos)
    elif pid == "2":
        my_player = p2
        # if p2 is not None:
        #     player_pos = [p2[0], p2[1], p2[2]]
        #     player_positions.remove(p2)
        #     player_positions.append(player_pos)
        # else:
        #     player_pos = None
        #     player_positions.remove(p2)
        #     player_positions.append(player_pos)
    elif pid == "3":
        my_player = p3
        # if p3 is not None:
        #     player_pos = [p3[0], p3[1], p3[2]]
        #     player_positions.remove(p3)
        #     player_positions.append(player_pos)
        # else:
        #     player_pos = None
        #     player_positions.remove(p3)
        #     player_positions.append(player_pos)
    elif pid == "4":
        my_player = p4
        # if p4 is not None:
        #     player_pos = [p4[0], p4[1], p4[2]]
        #     player_positions.remove(p4)
        #     player_positions.append(player_pos)
        # else:
        #     player_pos = None
        #     player_positions.remove(p4)
        #     player_positions.append(player_pos)

    p1_health = 30
    p2_health = 30
    p3_health = 30
    p4_health = 30
    health = 30
    shot = 0

    bullets = []
    collectibles = []

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
        global shot
        global bc

        if debug:
            print "Listening"
        while True:
            try:
                (data, addr) = my_socket.recvfrom(8192)
            except Exception as ex:
                template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                exception_message = template.format(type(ex).__name__, ex.args)
                print exception_message
                data, addr = "", ()
            if data != "":
                if debug:
                    print "[{}]".format(pid) + " The server sent: " + data
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
                        x = int(x)
                        y = int(data[3])
                        angle = float(data[4])
                        try:
                            if pid == p:
                                my_player.set_position((x, y, angle))
                            if p == "1":
                                p1.set_position((x, y, angle))
                                # if pid == p:
                                #     player_positions.remove(player_pos)
                                #     player_pos = [int(x), int(y), float(angle)]
                                #     player_positions.insert(int(p) - 1, player_pos)
                                # else:
                                #     player_positions.remove(p1)
                                #     p1 = [int(x), int(y), float(angle)]
                                #     player_positions.insert(int(p) - 1, p1)
                            elif p == "2":
                                p2.set_position((x, y, angle))
                                # if pid == p:
                                #     player_positions.remove(player_pos)
                                #     player_pos = [int(x), int(y), float(angle)]
                                #     player_positions.insert(int(p) - 1, player_pos)
                                # else:
                                #     player_positions.remove(p2)
                                #     p2 = [int(x), int(y), float(angle)]
                                #     player_positions.insert(int(p) - 1, p2)
                            elif p == "3":
                                p3.set_position((x, y, angle))
                                # if pid == p:
                                #     player_positions.remove(player_pos)
                                #     player_pos = [int(x), int(y), float(angle)]
                                #     player_positions.insert(int(p) - 1, player_pos)
                                # else:
                                #     player_positions.remove(p3)
                                #     p3 = [int(x), int(y), float(angle)]
                                #     player_positions.insert(int(p) - 1, p3)
                            elif p == "4":
                                p4.set_position((x, y, angle))
                                # if pid == p:
                                #     player_positions.remove(player_pos)
                                #     player_pos = [int(x), int(y), float(angle)]
                                #     player_positions.insert(int(p) - 1, player_pos)
                                # else:
                                #     player_positions.remove(p4)
                                #     p4 = [int(x), int(y), float(angle)]
                                #     player_positions.insert(int(p) - 1, p4)
                        except ValueError as e:
                            print e.message
                    else:
                        try:
                            if pid == p:
                                my_player.died()
                            if p == "1":
                                p1.died()
                                # if pid == p:
                                #     player_positions.remove(player_pos)
                                #     player_pos = [int(x), int(y), float(angle)]
                                #     player_positions.insert(int(p) - 1, player_pos)
                                # else:
                                #     player_positions.remove(p1)
                                #     p1 = [int(x), int(y), float(angle)]
                                #     player_positions.insert(int(p) - 1, p1)
                            elif p == "2":
                                p2.died()
                                # if pid == p:
                                #     player_positions.remove(player_pos)
                                #     player_pos = [int(x), int(y), float(angle)]
                                #     player_positions.insert(int(p) - 1, player_pos)
                                # else:
                                #     player_positions.remove(p2)
                                #     p2 = [int(x), int(y), float(angle)]
                                #     player_positions.insert(int(p) - 1, p2)
                            elif p == "3":
                                p3.died()
                                # if pid == p:
                                #     player_positions.remove(player_pos)
                                #     player_pos = [int(x), int(y), float(angle)]
                                #     player_positions.insert(int(p) - 1, player_pos)
                                # else:
                                #     player_positions.remove(p3)
                                #     p3 = [int(x), int(y), float(angle)]
                                #     player_positions.insert(int(p) - 1, p3)
                            elif p == "4":
                                p4.died()
                                # if pid == p:
                                #     player_positions.remove(player_pos)
                                #     player_pos = [int(x), int(y), float(angle)]
                                #     player_positions.insert(int(p) - 1, player_pos)
                                # else:
                                #     player_positions.remove(p4)
                                #     p4 = [int(x), int(y), float(angle)]
                                #     player_positions.insert(int(p) - 1, p4)
                        except ValueError as e:
                            print e.message
                        # if debug:
                        #     print player_pos, player_positions
                        # if p == "1":
                        #     if pid == p:
                        #         player_positions.remove(player_pos)
                        #         player_pos = None
                        #         player_positions.insert(int(p) - 1, player_pos)
                        #     else:
                        #         player_positions.remove(p1)
                        #         p1 = None
                        #         player_positions.insert(int(p) - 1, p1)
                        # elif p == "2":
                        #     if pid == p:
                        #         player_positions.remove(player_pos)
                        #         player_pos = None
                        #         player_positions.insert(int(p) - 1, player_pos)
                        #     else:
                        #         player_positions.remove(p2)
                        #         p2 = None
                        #         player_positions.insert(int(p) - 1, p2)
                        # elif p == "3":
                        #     if pid == p:
                        #         player_positions.remove(player_pos)
                        #         player_pos = None
                        #         player_positions.insert(int(p) - 1, player_pos)
                        #     else:
                        #         player_positions.remove(p3)
                        #         p3 = None
                        #         player_positions.insert(int(p) - 1, p3)
                        # elif p == "4":
                        #     if pid == p:
                        #         player_positions.remove(player_pos)
                        #         player_pos = None
                        #         player_positions.insert(int(p) - 1, player_pos)
                        #     else:
                        #         player_positions.remove(p4)
                        #         p4 = None
                        #         player_positions.insert(int(p) - 1, p4)
                elif code == "B":
                    global bullets
                    bullets = pickle.loads(data[1])
                    bc = [bull for bull in bullets if int(bull[0]) == int(pid)]
                    shot = len(bc)

                elif code == "T":
                    global messages
                    text_m = data[1]
                    x = int(data[2])
                    y = int(data[3])
                    messages.append(make_text(text_m, x, y, (33, 33, 33)))

                elif code == "hp":
                    global dead
                    global health
                    global player_won_id
                    p = int(data[1])
                    hp = int(data[2])
                    hitter = data[3]
                    if hp <= max_health:
                        if p == int(pid):
                            my_player.set_health(hp)
                            dead = my_player.is_alive()
                            if dead and not mute:
                                dead_sound.play()
                        alive = 0
                        if p == 1:
                            print p1.set_health(hp)
                            if p1.set_health(hp):
                                killed(hitter, str(p))
                        elif p == 2:
                            print p2.set_health(hp)
                            if p2.set_health(hp):
                                killed(hitter, str(p))
                        elif p == 3:
                            if p3.set_health(hp):
                                killed(hitter, str(p))
                        elif p == 4:
                            if p4.set_health(hp):
                                killed(hitter, str(p))

                        if p1.is_alive():
                            alive += 1
                            player_won_id = 1
                        if p2.is_alive():
                            alive += 1
                            player_won_id = 2
                        if p3.is_alive():
                            alive += 1
                            player_won_id = 3
                        if p4.is_alive():
                            alive += 1
                            player_won_id = 4
                        # players_health[p - 1] = hp
                        # if int(p) == int(pid):
                        #     health = hp
                        # if players_health[p - 1] <= 0:
                        #     player_positions[p - 1] = None
                        #     if int(p) == int(pid):
                        #         dead = True
                        #         if not mute:
                        #             dead_sound.play()
                        #     alive = 0
                        #     for pos in player_positions:
                        #         if pos is not None:
                        #             alive += 1
                        print alive, player_won_id
                        if alive == 1:
                            won(player_won_id)

                elif code == "cb":
                    global collectibles
                    collectibles = pickle.loads(data[1])


lThread = ReceiveThread("1")


def initial_connect():
    global pid
    global lThread
    global my_player

    my_socket.sendto(pickle.dumps(Message("00", None)), s_host)
    # my_socket.sendto("00", s_host)
    (data, addr) = my_socket.recvfrom(1024)
    if debug:
        print "The server sent: " + data
    try:
        pid = data.split("#")[1]
        if pid == "1":
            my_player = p1
        elif pid == "2":
            my_player = p2
        elif pid == "3":
            my_player = p3
        elif pid == "4":
            my_player = p4
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
    # s = ""
    # for player_position in player_positions:
    #     if player_position is player_pos:
    #         for co in player_position:
    #             s += str(co) + ","
    my_socket.sendto(pickle.dumps(Message("1" + str(pid), my_player.get_string_position())), s_host)
    # my_socket.sendto(pickle.dumps(Message("1" + str(pid), s[:-1])), s_host)
    # my_socket.sendto("1" + str(pid) + s[:-1], s_host)


def send_player_keys():
    s = ""
    for key in keys:
        s += str(key) + ","
    my_socket.sendto("2" + str(pid) + s[:-1], s_host)


def send_bullet(bullet_info):
    my_socket.sendto(pickle.dumps(Message("40", pickle.dumps(bullet_info))), s_host)


def send_mouse(angle):
    my_socket.sendto(pickle.dumps(Message("6" + str(pid), str(angle))), s_host)


def delete_bullet(bullet_info):
    my_socket.sendto(pickle.dumps(Message("50", pickle.dumps(bullet_info))), s_host)


def disconnect():
    my_socket.sendto(pickle.dumps(Message("99", None)), s_host)


def enemy_hit(enemy_id, hitter):
    if int(hitter) == int(pid):
        if not mute:
            hit_sound.play()
        my_socket.sendto(pickle.dumps(Message("7" + str(enemy_id), str(pid))), s_host)


def got_collectible(acquired_collectible):
    my_socket.sendto(pickle.dumps(Message("8" + str(pid), None)), s_host)
    my_socket.sendto(pickle.dumps(Message("85", pickle.dumps(acquired_collectible))), s_host)


def send_collectible(created_collectible):
    my_socket.sendto(pickle.dumps(Message("80", None)), s_host)
    my_socket.sendto(pickle.dumps(Message(None, pickle.dumps(created_collectible))), s_host)


def killed(killer, killed_p):
    if int(killer) == int(pid):
        my_socket.sendto(pickle.dumps(Message("2" + str(killed_p), killer)), s_host)


def won(player_won):
    if int(player_won) == int(pid):
        if not mute:
            win_sound.play()
        my_socket.sendto(pickle.dumps(Message("20", "Player #" + str(player_won) + " won this round,5,400")), s_host)
        my_socket.sendto(pickle.dumps(Message("20", "Congratulations!,5,400")), s_host)


def new_round():
    if debug:
        print player_won_id, pid
    if int(player_won_id) == int(pid):
        if debug:
            print "NEW ROUND SENTTTTTTTTTTTTTT"
        my_socket.sendto(pickle.dumps(Message("90", str(player_won_id))), s_host)


def make_text(text_message, x, y, text_color):
    rendered_text = font.render(text_message, True, text_color, (255, 255, 255))
    rendered_text_rect = rendered_text.get_rect()
    rendered_text_rect.left = x
    rendered_text_rect.top = y
    if "SPECTATING" not in text_message:
        offset_messages()
    if "Congrat" in text_message or "won this round" in text_message:
        return [rendered_text, rendered_text_rect, time_to_fade * 2, 1]
    elif "won" in text_message and ("game" in text_message or "round(s)" in text_message):
        return [rendered_text, rendered_text_rect, time_to_fade * 3, 2]
    return [rendered_text, rendered_text_rect, time_to_fade, 0]


def offset_messages():
    message_index = 0
    for t_message in messages:
        t_message_rect = t_message[1]
        t_message_rect.top -= text_space
        message_index += 1


pygame.init()
pygame.mixer.init()
pygame.mouse.set_visible(False)
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Top Down Shooter")
flags = screen.get_flags()
keys = [False, False, False, False]
bullet_speed = 12
player_speed = 6
bullet_damage = 1
clock = pygame.time.Clock()
frame = 0

player_img = pygame.image.load('player1.png')
player_img = pygame.transform.scale(player_img, (62, 41))
bullet_img = pygame.image.load('bullet.png').convert()
bullet_img.set_colorkey((255, 255, 255))
bullet_img = pygame.transform.scale(bullet_img, (13, 5))
bg = random.randint(1, 5)
background_img = pygame.image.load('bg1.jpg')
background_img = pygame.transform.scale(background_img, (width, height))
bad_guys = []

hit_sound = pygame.mixer.Sound('hit.wav')
shoot_sound = pygame.mixer.Sound('shoot.wav')
win_sound = pygame.mixer.Sound('win.wav')
dead_sound = pygame.mixer.Sound('dead.wav')

ammo = pygame.transform.rotate(bullet_img, 90)
ammo = pygame.transform.scale2x(ammo)
shot = 0

font = pygame.font.SysFont(None, 22)
text_space = 25
time_to_fade = 3000

health = 30
max_health = 30

initial_connect()

x_offset = 34
y_offset = 12
offset = pygame.math.Vector2()
offset.x = x_offset
offset.y = y_offset

if pid == "1":
    my_player = p1
    # if p1 is not None:
    #     player_pos = [p1[0], p1[1], p1[2]]
    #     player_positions.remove(p1)
    #     player_positions.insert(int(pid) - 1, player_pos)
elif pid == "2":
    my_player = p2
    # if p2 is not None:
    #     player_pos = [p2[0], p2[1], p2[2]]
    #     player_positions.remove(p2)
    #     player_positions.insert(int(pid) - 1, player_pos)
elif pid == "3":
    my_player = p3
    # if p3 is not None:
    #     player_pos = [p3[0], p3[1], p3[2]]
    #     player_positions.remove(p3)
    #     player_positions.insert(int(pid) - 1, player_pos)
elif pid == "4":
    my_player = p4
    # if p4 is not None:
    #     player_pos = [p4[0], p4[1], p4[2]]
    #     player_positions.remove(p4)
    #     player_positions.insert(int(pid) - 1, player_pos)

new = False

point1 = (0, 0)
point2 = (0, 0)
point3 = (0, 0)


def draw_player(player, is_mine=False):
    global players_rects
    global player_rect

    player_position = player.get_position()
    if player_position is not None and player.is_alive():
        playerrot = pygame.transform.rotate(player_img, 360 - player_position[2] * 57.29)
        playerpos1 = (player_position[0] - playerrot.get_rect().width / 2,
                      player_position[1] - playerrot.get_rect().height / 2)
        screen.blit(playerrot, playerpos1)
        players_rects.append([screen.blit(playerrot, playerpos1), player])
        if is_mine:
            player_rect = screen.blit(playerrot, playerpos1)
    else:
        players_rects.append([None, player])
        if is_mine:
            player_rect = None


def draw_players():
    if pid != "1":
        draw_player(p1)
    if pid != "2":
        draw_player(p2)
    if pid != "3":
        draw_player(p3)
    if pid != "4":
        draw_player(p4)


def draw_my_player(new_angle):
    my_player.set_angle(new_angle)
    draw_player(my_player, is_mine=True)


def new_mouse_position(new_angle, new_position):
    global mouse
    global point1
    global point2
    global point3

    send_mouse(new_angle)
    mouse = new_position
    my_player_pos = my_player.get_position()
    if my_player_pos is not None:
        point1 = (mouse[0], mouse[1])
        point3 = (my_player_pos[0] + offset.rotate(-(360 - my_player_pos[2] * 57.29) % 360).x,
                  my_player_pos[1] + offset.rotate(-(360 - my_player_pos[2] * 57.29) % 360).y)
        point2 = (point1[0], point3[1])


def update_bullets():
    global bullets
    global shot

    for _bullet in bullets:
        if _bullet[0] == pid:
            delete_bullet(_bullet)
            velocity_x = math.cos(_bullet[1]) * bullet_speed
            velocity_y = math.sin(_bullet[1]) * bullet_speed
            _bullet[2] += int(velocity_x)
            _bullet[3] += int(velocity_y)
            if _bullet[2] < -64 or _bullet[2] > width or _bullet[3] < -64 or _bullet[3] > height:
                try:
                    if _bullet in bullets:
                        bullets.remove(_bullet)
                    if not mute:
                        hit_sound.play()
                    shot -= 1 if shot > 0 else 0
                except IndexError as e:
                    print e
            else:
                send_bullet(_bullet)


def draw_bullets():
    global bullets

    for _bullet in bullets:
        bullet1 = pygame.transform.rotate(bullet_img, 360 - _bullet[1] * 57.29)
        screen.blit(bullet1, (_bullet[2], _bullet[3]))


def draw_collectibles():
    global collectibles

    for collectible in collectibles:
        collectible = int(collectible[0]), int(collectible[1]),\
                      pygame.draw.circle(screen, (0, 100, 0), (int(collectible[0]), int(collectible[1])), 10)
        pygame.draw.circle(screen, (0, 100, 0), (collectible[0], collectible[1]), 10)
        pygame.draw.circle(screen, (0, 255, 0), (collectible[0], collectible[1]), 8)
        pygame.draw.line(screen, (0, 0, 0), (collectible[0] - 5, collectible[1] - 1),
                         (collectible[0] + 5, collectible[1] - 1), 2)
        pygame.draw.line(screen, (0, 0, 0), (collectible[0] - 1, collectible[1] - 5),
                         (collectible[0] - 1, collectible[1] + 5), 2)
        if player_rect is not None:
            if collectible[2].colliderect(player_rect):
                collectibles.remove(collectible)
                got_collectible(collectible)


def display_messages():
    global messages
    global new

    for message in messages:
        text = message[0]
        text_rect = message[1]
        message[2] -= 50
        if message[2] <= 0:
            if message in messages:
                messages.remove(message)
            if message[3] == 1 and not new:
                new = True
                new_round()
            if message[3] == 2:
                print "QUITTING"
                disconnect()
                print "DISCONNECTED"
                my_socket.close()
                pygame.quit()
                print "SOCKET AND PYGAME CLOSED"
                exit(0)
        else:
            screen.blit(text, text_rect)


def draw_healthbar():
    global max_health
    global screen

    _health = my_player.get_health()

    pygame.draw.rect(screen, (0, 255, 0), (20, 530, int(100 * (float(_health) / max_health)), 20))
    pygame.draw.rect(screen, (255, 0, 0),
                     (20 + int(100 * (float(_health) / max_health)), 530,
                      int(100 * (1 - (float(_health) / max_health))), 20))
    pygame.draw.rect(screen, (0, 0, 0), (20, 530, 100, 20), 5)


def draw_crosshair():
    global mouse
    global screen

    pygame.draw.line(screen, (0, 0, 0), (mouse[0] - 17, mouse[1]), (mouse[0] - 3, mouse[1]), 5)
    pygame.draw.line(screen, (0, 0, 0), (mouse[0] + 17, mouse[1]), (mouse[0] + 3, mouse[1]), 5)
    pygame.draw.line(screen, (0, 0, 0), (mouse[0], mouse[1] + 17), (mouse[0], mouse[1] + 3), 5)
    pygame.draw.line(screen, (0, 0, 0), (mouse[0], mouse[1] - 17), (mouse[0], mouse[1] - 3), 5)

    pygame.draw.line(screen, (0, 255, 0), (mouse[0] - 15, mouse[1]), (mouse[0] - 5, mouse[1]), 2)
    pygame.draw.line(screen, (0, 255, 0), (mouse[0] + 15, mouse[1]), (mouse[0] + 5, mouse[1]), 2)
    pygame.draw.line(screen, (0, 255, 0), (mouse[0], mouse[1] + 15), (mouse[0], mouse[1] + 5), 2)
    pygame.draw.line(screen, (0, 255, 0), (mouse[0], mouse[1] - 15), (mouse[0], mouse[1] - 5), 2)


def draw_ammo():
    global screen

    for i in xrange(5 - shot):
        screen.blit(ammo, (20 + i * 15, 560))


def draw_hitboxes():
    global players_rects
    global screen

    for _players_rect, _player in players_rects:
        if _players_rect is not None:
            pygame.draw.rect(screen, (255, 0, 0), _players_rect, 1)


def draw_aimline():
    global screen
    global point1
    global point2
    global point3

    _player_pos = my_player.get_position()
    if _player_pos is not None:
        pygame.draw.line(screen, (0, 255, 0), point1, point3)
        pygame.draw.line(screen, (0, 255, 0), point1, point2)
        pygame.draw.line(screen, (0, 255, 0), point3, point2)
        pygame.draw.circle(screen, (0, 0, 255), (_player_pos[0], _player_pos[1]), 1)
        pygame.draw.circle(screen, (0, 0, 255), (int(point3[0]), int(point3[1])), 1)


def check_for_collisions():
    global players_rects
    global bullets
    global bullet_damage
    global shot

    for players_rect, player in players_rects:
        if players_rect is not None:
            for _bullet in bullets:
                bullrect = pygame.Rect(bullet_img.get_rect())
                bullrect.left = _bullet[2]
                bullrect.top = _bullet[3]
                if players_rect.colliderect(bullrect):
                    if int(player.get_p_id()) != int(_bullet[0]) and player.get_position() is not None:
                        player.set_health(player.get_health() - bullet_damage)
                        enemy_hit(player.get_p_id(), _bullet[0])
                        if _bullet in bullets:
                            bullets.remove(_bullet)
                        shot -= 1 if shot > 0 else 0
                        delete_bullet(_bullet)


running = 1
exitcode = 0
while running:
    player_rect = screen.blit(screen, (0, 0))
    screen.blit(background_img, (0, 0))
    players_rects = []
    p_id = 1

    draw_players()
    position = pygame.mouse.get_pos()
    angle = math.atan2(position[1] - point3[1], position[0] - point3[0])
    draw_my_player(angle)
    if position != mouse:
        new_mouse_position(angle, position)
    update_bullets()
    draw_bullets()
    draw_collectibles()
    display_messages()
    draw_healthbar()
    draw_crosshair()
    draw_ammo()
    if debug:
        draw_hitboxes()
        draw_aimline()
    check_for_collisions()

    # for playerp in player_positions:
    #     if playerp is player_pos:
    #         if playerp is not None:
    #             position = pygame.mouse.get_pos()
    #             playerp[2] = math.atan2(position[1] - point3[1], position[0] - point3[0])
    #             playerrot = pygame.transform.rotate(player_img, 360 - playerp[2] * 57.29)
    #             playerpos1 = (playerp[0] - playerrot.get_rect().width / 2, playerp[1] - playerrot.get_rect().height / 2)
    #             screen.blit(playerrot, playerpos1)
    #             players_rects.append([screen.blit(playerrot, playerpos1), p_id])
    #             player_rect = screen.blit(playerrot, playerpos1)
    #             if position != mouse:
    #                 send_mouse(playerp[2])
    #                 mouse = position
    #                 point1 = (mouse[0], mouse[1])
    #                 point3 = (player_pos[0] + offset.rotate(-(360 - playerp[2] * 57.29) % 360).x,
    #                           player_pos[1] + offset.rotate(-(360 - playerp[2] * 57.29) % 360).y)
    #                 point2 = (point1[0], point3[1])
    #         else:
    #             players_rects.append([None, p_id])
    #         p_id += 1
    #     else:
    #         if playerp is not None:
    #             playerrot = pygame.transform.rotate(player_img, 360 - playerp[2] * 57.29)
    #             playerpos1 = (playerp[0] - playerrot.get_rect().width / 2, playerp[1] - playerrot.get_rect().height / 2)
    #             screen.blit(playerrot, playerpos1)
    #             players_rects.append([screen.blit(playerrot, playerpos1), p_id])
    #         else:
    #             players_rects.append([None, p_id])
    #         p_id += 1

    # for bullet in bullets:
    #     if bullet[0] == pid:
    #         delete_bullet(bullet)
    #         index = 0
    #         velx = math.cos(bullet[1]) * bullet_speed
    #         vely = math.sin(bullet[1]) * bullet_speed
    #         bullet[2] += int(velx)
    #         bullet[3] += int(vely)
    #         if bullet[2] < -64 or bullet[2] > width or bullet[3] < -64 or bullet[3] > height:
    #             try:
    #                 bullets.pop(index)
    #                 if not mute:
    #                     hit_sound.play()
    #                 shot -= 1 if shot > 0 else 0
    #             except IndexError as e:
    #                 print e
    #         else:
    #             send_bullet(bullet)
    #         index += 1
    # for projectile in bullets:
    #     bullet1 = pygame.transform.rotate(bullet_img, 360 - projectile[1] * 57.29)
    #     screen.blit(bullet1, (projectile[2], projectile[3]))

    # for collectible in collectibles:
    #     pygame.draw.circle(screen, (0, 100, 0), (collectible[0], collectible[1]), 10)
    #     pygame.draw.circle(screen, (0, 255, 0), (collectible[0], collectible[1]), 8)
    #     pygame.draw.line(screen, (0, 0, 0), (collectible[0] - 5, collectible[1] - 1),
    #                      (collectible[0] + 5, collectible[1] - 1), 2)
    #     pygame.draw.line(screen, (0, 0, 0), (collectible[0] - 1, collectible[1] - 5),
    #                      (collectible[0] - 1, collectible[1] + 5), 2)
    #     if collectible[2].colliderect(player_rect):
    #         collectibles.remove(collectible)
    #         got_collectible(collectible)

    ############ TUNNEL VISION #############

    # # points.append(())
    # # print math.degrees(player_pos[2])
    # # print (360 - player_pos[2] * 57.29) % 360
    # m = math.tan(-(2 * math.pi - player_pos[2]))
    # # print m
    # b = player_pos[1] - m * player_pos[0]
    # print 'y = {} * x + {}'.format(m, b)
    # if m != 0:
    #     top = (0 - b) / m
    #     bot = (height - b) / m
    # else:
    #     top = 0  # player_rect.top
    #     bot = width  # player_rect.top + player_rect.height
    # print 'top = ({}, 0), bot = ({}, {})'.format(top, bot, height)
    #
    # if top != 0:
    #     points = [(0, 0),
    #               (top - player_rect.width / 2, 0),
    #               # (player_rect.left, 0),
    #               (player_rect.left, player_rect.top),
    #               (player_rect.left, player_rect.top + player_rect.height),
    #               (player_rect.left + player_rect.width, player_rect.top + player_rect.height),
    #               (player_rect.left + player_rect.width, player_rect.top),
    #               # (player_rect.left + player_rect.width, 0),
    #               (top + player_rect.width / 2, 0),
    #               (width, 0),
    #               (width, height),
    #               (bot + player_rect.width / 2, height),
    #               (bot - player_rect.width / 2, height),
    #               (0, height),
    #               ]
    #     pygame.draw.polygon(screen, (0, 0, 0), points)
    # else:
    #     points1 = [(0, 0),
    #               (0, player_rect.top),
    #               (width, player_rect.top),
    #               (width, 0)
    #               ]
    #
    #     points2 = [(0, height),
    #                (0, player_rect.top + player_rect.height),
    #                (width, player_rect.top + player_rect.height),
    #                (width, height),
    #                ]
    #     pygame.draw.polygon(screen, (0, 0, 0), points1)
    #     pygame.draw.polygon(screen, (0, 0, 0), points2)
    #
    # x0 = 40
    # x1 = 40
    # x2 = 40
    # x3 = 40
    # top1 = (top - 20, 0)
    # top2 = (top + 20, 0)
    # bot1 = (bot - 20, height)
    # bot2 = (bot + 20, height)
    # i = 0
    # # if 0 < x0 < width and top1 not in points:
    # #     points.insert(i + 1, top1)
    # #     i += 1
    # # if 0 < x1 < width and top2 not in points:
    # #     points.insert(i + 5, top2)
    # #     i += 1
    # # if 0 < x2 < width and bot1 not in points:
    # #     points.insert(i + 7, bot1)
    # #     i += 1
    # # if 0 < x3 < width and bot2 not in points:
    # #     points.insert(i + 7, bot2)
    # #     i += 1
    #
    #
    # # print points
    #
    # # pygame.draw.polygon(screen, (0, 0, 0),
    # #                     [(width, 0),
    # #                      (player_rect.left + player_rect.width, 0),
    # #                      (player_rect.left + player_rect.width, player_rect.top),
    # #                      (player_rect.left + player_rect.width, player_rect.top + player_rect.height),
    # #                      (player_rect.left, player_rect.top + player_rect.height),
    # #                      (0, height),
    # #                      (width, height)],
    # #                     )
    # #########################################
    # # pygame.draw.line(screen, (0, 255, 0), (point1[0], point1[1] - 30), (point3[0], point3[1] - 30))
    # # pygame.draw.line(screen, (0, 255, 0), (point1[0], point1[1] + 10), (point3[0], point3[1] + 10))

    # for message in messages:
    #     text = message[0]
    #     text_rect = message[1]
    #     message[2] -= 50
    #     if message[2] <= 0:
    #         if message in messages:
    #             messages.remove(message)
    #         if message[3] == 1 and not new:
    #             new = True
    #             new_round()
    #         if message[3] == 2:
    #             print "QUITTING"
    #             disconnect()
    #             print "DISCONNECTED"
    #             my_socket.close()
    #             pygame.quit()
    #             print "SOCKET AND PYGAME CLOSED"
    #             exit(0)
    #     else:
    #         screen.blit(text, text_rect)

    # pygame.draw.rect(screen, (0, 255, 0), (20, 530, int(100 * (float(health) / max_health)), 20))
    # pygame.draw.rect(screen, (255, 0, 0),
    #                  (20 + int(100 * (float(health) / max_health)), 530,
    #                   int(100 * (1 - (float(health) / max_health))), 20))
    # pygame.draw.rect(screen, (0, 0, 0), (20, 530, 100, 20), 5)

    # pygame.draw.line(screen, (0, 0, 0), (mouse[0] - 17, mouse[1]), (mouse[0] - 3, mouse[1]), 5)
    # pygame.draw.line(screen, (0, 0, 0), (mouse[0] + 17, mouse[1]), (mouse[0] + 3, mouse[1]), 5)
    # pygame.draw.line(screen, (0, 0, 0), (mouse[0], mouse[1] + 17), (mouse[0], mouse[1] + 3), 5)
    # pygame.draw.line(screen, (0, 0, 0), (mouse[0], mouse[1] - 17), (mouse[0], mouse[1] - 3), 5)
    #
    # pygame.draw.line(screen, (0, 255, 0), (mouse[0] - 15, mouse[1]), (mouse[0] - 5, mouse[1]), 2)
    # pygame.draw.line(screen, (0, 255, 0), (mouse[0] + 15, mouse[1]), (mouse[0] + 5, mouse[1]), 2)
    # pygame.draw.line(screen, (0, 255, 0), (mouse[0], mouse[1] + 15), (mouse[0], mouse[1] + 5), 2)
    # pygame.draw.line(screen, (0, 255, 0), (mouse[0], mouse[1] - 15), (mouse[0], mouse[1] - 5), 2)

    # for i in xrange(5 - shot):
    #     screen.blit(ammo, (20 + i * 15, 560))

    # if debug:
    #     for _players_rect, _player_id in players_rects:
    #         if _players_rect is not None:
    #             pygame.draw.rect(screen, (255, 0, 0), _players_rect, 1)
    #     if player_pos is not None:
    #         pygame.draw.line(screen, (0, 255, 0), point1, point3)
    #         pygame.draw.line(screen, (0, 255, 0), point1, point2)
    #         pygame.draw.line(screen, (0, 255, 0), point3, point2)
    #         pygame.draw.circle(screen, (0, 0, 255), (player_pos[0], player_pos[1]), 1)
    #         pygame.draw.circle(screen, (0, 0, 255), (int(point3[0]), int(point3[1])), 1)

    # for players_rect, player_id in players_rects:
    #     if players_rect is not None:
    #         for bullet in bullets:
    #             bullrect = pygame.Rect(bullet_img.get_rect())
    #             bullrect.left = bullet[2]
    #             bullrect.top = bullet[3]
    #             if players_rect.colliderect(bullrect):
    #                 if int(player_id) != int(bullet[0]) and player_positions[player_id - 1] is not None:
    #                     players_health[player_id - 1] -= 1
    #                     enemy_hit(player_id, bullet[0])
    #                     if bullet in bullets:
    #                         bullets.remove(bullet)
    #                     shot -= 1 if shot > 0 else 0
    #                     delete_bullet(bullet)

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
            if my_player.is_alive():
                if event.key == K_w:
                    keys[0] = True
                elif event.key == K_a:
                    keys[1] = True
                elif event.key == K_s:
                    keys[2] = True
                elif event.key == K_d:
                    keys[3] = True
            if event.key == K_f:
                flags ^= FULLSCREEN
                pygame.display.set_mode((width, height), flags)
            elif event.key == K_p:
                bc = [bullet for bullet in bullets if int(bullet[0]) == int(pid)]
                print bullets, shot, len(bc)
        if event.type == pygame.KEYUP and my_player.is_alive():
            if event.key == K_w:
                keys[0] = False
            elif event.key == K_a:
                keys[1] = False
            elif event.key == K_s:
                keys[2] = False
            elif event.key == K_d:
                keys[3] = False
        if event.type == pygame.MOUSEBUTTONDOWN and my_player.is_alive():
            if not mute:
                shoot_sound.play()
            bc = [bullet for bullet in bullets if int(bullet[0]) == int(pid)]
            shot = len(bc)
            position = pygame.mouse.get_pos()
            _player_pos = my_player.get_position()
            if _player_pos is not None:
                ang = math.atan2(position[1] - (_player_pos[1] + y_offset), position[0] - (_player_pos[0] + x_offset))
                if position[1] > _player_pos[1] and _player_pos[0] < position[0]:
                    ang = -ang
                b = [pid,
                     _player_pos[2],
                     int(point3[0]),
                     int(point3[1])]
                if shot < 5:
                    send_bullet(b)
                    shot += 1

    moved = False
    direction = -1
    try:
        if keys[0] and player_rect.top - player_speed > 0:
            # player_pos[1] -= player_speed
            my_player.delta_y(-player_speed)
            direction = 0
            moved = True
        elif keys[2] and player_rect.top + player_rect.height + player_speed < height:
            # player_pos[1] += player_speed
            my_player.delta_y(+player_speed)
            direction = 2
            moved = True
        if keys[1] and player_rect.left - player_speed > 0:
            # player_pos[0] -= player_speed
            my_player.delta_x(-player_speed)
            direction = 1
            moved = True
        elif keys[3] and player_rect.left + player_rect.width + player_speed < width:
            # player_pos[0] += player_speed
            my_player.delta_x(+player_speed)
            direction = 3
            moved = True
    except AttributeError as e:
        print e.message

    if moved:
        _player_pos = my_player.get_position()
        send_player_pos()
        point1 = (mouse[0], mouse[1])
        point3 = (_player_pos[0] + offset.rotate(-(360 - _player_pos[2] * 57.29) % 360).x,
                  _player_pos[1] + offset.rotate(-(360 - _player_pos[2] * 57.29) % 360).y)
        point2 = (point1[0], point3[1])

    clock.tick(30)
    collectible_timer -= 50
    if collectible_timer <= 50:
        collectible_timer = 5000
        x = random.randint(100, width - 100)
        y = random.randint(100, height - 100)
        collectibles.append((x, y, pygame.draw.circle(screen, (0, 100, 0), (x, y), 10)))
        send_collectible((x, y, pygame.draw.circle(screen, (0, 100, 0), (x, y), 10)))
