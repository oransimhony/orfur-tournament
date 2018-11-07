import pygame
from pygame.locals import *
import subprocess


class SceneManager:
    def __init__(self):
        self.current_scene = Scene("MAIN", [make_text("Welcome to Orfur Tournament!", 400, 100, white)],
                                   [make_text("Start", 200, 400, highlighted, font=label_font),
                                    make_text("Help", 400, 400, white, font=label_font),
                                    make_text("Quit", 600, 400, white, font=label_font)],
                                   [("Start", 200, 400), ("Help", 400, 400), ("Quit", 600, 400)])

    def load_scene(self, scene_to_load):
        if scene_to_load.name == "START":
            srvs = get_servers()
            scene_to_load.servers = srvs
        self.current_scene = scene_to_load

    def get_scene(self):
        return self.current_scene


class Scene:
    def __init__(self, name, labels, buttons, buttons_data, servers=[]):
        self.name = name
        self.labels = labels
        self.buttons = buttons
        self.buttons_data = buttons_data
        self.highlighted_button_id = 0
        self.servers = servers
        self.highlighted_server_id = 0

    def draw(self):
        for label in self.labels:
            screen.blit(label[0], label[1])
        for button in self.buttons:
            screen.blit(button[0], button[1])
        for i in xrange(len(self.servers)):
            if i == self.highlighted_server_id:
                self.servers[i].draw(highlighted)
            else:
                self.servers[i].draw(white)

    def left(self):
        if self.highlighted_button_id > 0:
            self.buttons[self.highlighted_button_id] = make_text(self.buttons_data[self.highlighted_button_id][0],
                                                                 self.buttons_data[self.highlighted_button_id][1],
                                                                 self.buttons_data[self.highlighted_button_id][2],
                                                                 white, font=label_font)
            self.highlighted_button_id -= 1
            self.buttons[self.highlighted_button_id] = make_text(self.buttons_data[self.highlighted_button_id][0],
                                                                 self.buttons_data[self.highlighted_button_id][1],
                                                                 self.buttons_data[self.highlighted_button_id][2],
                                                                 highlighted, font=label_font)

    def right(self):
        if self.highlighted_button_id < len(self.buttons) - 1:
            self.buttons[self.highlighted_button_id] = make_text(self.buttons_data[self.highlighted_button_id][0],
                                                                 self.buttons_data[self.highlighted_button_id][1],
                                                                 self.buttons_data[self.highlighted_button_id][2],
                                                                 white, font=label_font)
            self.highlighted_button_id += 1
            self.buttons[self.highlighted_button_id] = make_text(self.buttons_data[self.highlighted_button_id][0],
                                                                 self.buttons_data[self.highlighted_button_id][1],
                                                                 self.buttons_data[self.highlighted_button_id][2],
                                                                 highlighted, font=label_font)

    def up(self):
        self.highlighted_server_id -= 1 if self.highlighted_server_id > 0 else 0

    def down(self):
        self.highlighted_server_id += 1 if self.highlighted_server_id < len(self.servers) - 1 else 0


class AddScene(Scene):
    def __init__(self, name, labels, buttons, buttons_data):
        self.name = name
        self.labels = labels
        self.buttons = buttons
        self.buttons_data = buttons_data
        self.highlighted_button_id = 0
        self.server_name = ""
        self.server_address = ""
        self.highlighted_text_box_id = 0

    def draw(self):
        for label in self.labels:
            screen.blit(label[0], label[1])
        for button in self.buttons:
            screen.blit(button[0], button[1])
        title_text = make_text("Add a Server", 400, 40, white)
        name_text = make_text("Name: ", 50, 150, white, font=label_font)
        server_name_text = make_text(self.server_name, 120, 150, white, font=label_font)
        address_text = make_text("Address: ", 60, 220, white, font=label_font)
        server_address_text = make_text(self.server_address, 160, 220, white, font=label_font)
        name_text[1].left = 10
        address_text[1].left = 10
        server_name_text[1].left = 10 + name_text[1].w
        server_address_text[1].left = 10 + address_text[1].w
        writing = make_text("_", 60, 200, white, font=label_font)

        if self.highlighted_text_box_id == 0:
            if frames <= 15:
                writing[1].left = server_name_text[1].left + server_name_text[1].w
                writing[1].top = server_name_text[1].top
                screen.blit(writing[0], writing[1])
            pygame.draw.rect(screen, highlighted,
                             (5 + name_text[1].w, 137, 790 - (5 + name_text[1].w + name_text[1].left), 30), 2)
            pygame.draw.rect(screen, white,
                             (5 + address_text[1].w, 207, 790 - (5 + address_text[1].w + address_text[1].left), 30), 2)
        elif self.highlighted_text_box_id == 1:
            if frames <= 15:
                writing[1].left = server_address_text[1].left + server_address_text[1].w
                writing[1].top = server_address_text[1].top
                screen.blit(writing[0], writing[1])
            pygame.draw.rect(screen, white,
                             (5 + name_text[1].w, 137, 790 - (5 + name_text[1].w + name_text[1].left), 30), 2)
            pygame.draw.rect(screen, highlighted,
                             (5 + address_text[1].w, 207, 790 - (5 + address_text[1].w + address_text[1].left), 30), 2)
        else:
            pygame.draw.rect(screen, white,
                             (5 + name_text[1].w, 137, 790 - (5 + name_text[1].w + name_text[1].left), 30), 2)
            pygame.draw.rect(screen, white,
                             (5 + address_text[1].w, 207, 790 - (5 + address_text[1].w + address_text[1].left), 30), 2)
        screen.blit(title_text[0], title_text[1])
        screen.blit(name_text[0], name_text[1])
        screen.blit(server_name_text[0], server_name_text[1])
        screen.blit(address_text[0], address_text[1])
        screen.blit(server_address_text[0], server_address_text[1])

    def up(self):
        self.highlighted_text_box_id -= 1 if self.highlighted_text_box_id > 0 else 0

    def down(self):
        self.highlighted_text_box_id += 1 if self.highlighted_text_box_id < 1 else 0


class Server:
    def __init__(self, name="Localhost", address="127.0.0.1", x=20, y=200):
        self.name = name
        self.address = address
        self.x = x
        self.y = y

    def __str__(self):
        return "Name: %s, Address: %s" % (self.name, self.address)

    def draw(self, rect_color):
        pygame.draw.rect(screen, rect_color, (self.x, self.y, 760, 30), 2)
        name_text = make_text(self.name, self.x + 10, self.y + 2, white, font=instruction_font)
        address_text = make_text(self.address, self.x + 600, self.y + 2, white, font=instruction_font)
        address_text[1].left = self.x + 750 - address_text[1].w
        screen.blit(name_text[0], name_text[1])
        screen.blit(address_text[0], address_text[1])


pygame.init()

title_font = pygame.font.SysFont("8bitoperator Regular", 30)
label_font = pygame.font.SysFont("8bitoperator Regular", 22)
instruction_font = pygame.font.SysFont("8bitoperator Regular", 18)


def make_text(text_message, x, y, text_color, font=title_font):
    rendered_text = font.render(text_message, True, text_color)
    rendered_text_rect = rendered_text.get_rect()
    if font != instruction_font:
        rendered_text_rect.centerx = x
        rendered_text_rect.centery = y
    else:
        rendered_text_rect.left = x
        rendered_text_rect.top = y
    return rendered_text, rendered_text_rect


# def make_button(label_text, button_x, button_y, button_w, button_h):
#     button_label = make_label(label_text, button_x + button_w / 2, button_y + button_h / 2, (0, 0, 0))
#     button_rect = pygame.draw.rect(screen, (0, 0, 0), (button_x, button_y, button_w, button_h))
#     return button_rect, button_label

def save_server(name, address):
    if name != "" and address != "":
        print "SAVING %s %s" % (name, address)
        with open('servers.txt', 'a') as a_file:
            a_file.write("\n%s,%s" % (name, address))


def get_servers():
    servers = []
    with open('servers.txt', 'r') as opened_file:
        i = 0
        for line in opened_file:
            if line != "" and line != "\n" and len(servers) < 7:
                servers.append(
                    Server(line.replace('\n', '').split(',')[0], line.replace('\n', '').split(',')[1], 20,
                           180 + 40 * i))
                i += 1
    return servers


def delete_server(server):
    f = open("servers.txt", "r+")
    d = f.readlines()
    f.seek(0)
    for i in d:
        if "%s,%s" % (server.name, server.address) not in i and i != "" and i != "\n":
            f.write(i)
    f.truncate()
    f.close()


pygame.mixer.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Top Down Shooter")
flags = screen.get_flags()

clock = pygame.time.Clock()

white = (255, 255, 255)
highlighted = (255, 255, 0)

frames = 0

scene_manager = SceneManager()

main_scene = Scene("MAIN", [make_text("Welcome to Orfur Tournament!", 400, 100, white)],
                   [make_text("Start", 200, 400, highlighted, font=label_font),
                    make_text("Help", 400, 400, white, font=label_font),
                    make_text("Quit", 600, 400, white, font=label_font)],
                   [("Start", 200, 400), ("Help", 400, 400), ("Quit", 600, 400)])

help_scene = Scene("HELP", [make_text("Instructions", 400, 40, white),
                            make_text("In this game your goal is to beat all the other players and",
                                      10, 100, white, font=instruction_font),
                            make_text(" remain the last one standing",
                                      10, 130, white, font=instruction_font),
                            make_text("You move your player using the WASD keys",
                                      10, 160, white, font=instruction_font),
                            make_text("You change your aim position using the mouse",
                                      10, 190, white, font=instruction_font),
                            make_text("You shoot using the left mouse button",
                                      10, 220, white, font=instruction_font),
                            make_text("You can shoot bursts using the scroll wheel",
                                      10, 250, white, font=instruction_font),
                            make_text("For each round you win, you get 1 point",
                                      10, 280, white, font=instruction_font),
                            make_text("The first player that reaches 3 point, wins",
                                      10, 310, white, font=instruction_font),
                            make_text("But most importantly...",
                                      10, 340, white, font=instruction_font),
                            make_text("ENJOY!", 400, 400, highlighted)
                            ], [
                       make_text("Return to Main Menu", 200, 500, white, font=label_font),
                       make_text("Quit", 600, 500, white, font=label_font)],
                   [("Return to Main Menu", 200, 500), ("Quit", 600, 500)])

start_scene = Scene("START", [make_text("Start Screen", 400, 40, white),
                              make_text("Change server using the up and down arrow keys",
                                        10, 60, white, font=instruction_font),
                              make_text("Choose the highlighted server using the S key",
                                        10, 85, white, font=instruction_font),
                              make_text("Delete the highlighted server using the D key",
                                        10, 110, white, font=instruction_font),
                              make_text("But don't delete localhost :)",
                                        10, 135, white, font=instruction_font)
                              ],
                    [make_text("Add a new server", 150, 500, highlighted, font=label_font),
                     make_text("Return to Main Menu", 450, 500, white, font=label_font),
                     make_text("Quit", 650, 500, white, font=label_font)],
                    [("Add a new server", 150, 500), ("Return to Main Menu", 450, 500), ("Quit", 650, 500)])

add_server_scene = AddScene("ADD", [], [make_text("Save server", 150, 500, highlighted, font=label_font),
                                        make_text("Return to Server List", 420, 500, white, font=label_font),
                                        make_text("Quit", 650, 500, white, font=label_font)],
                            [("Save Server", 150, 500), ("Return to Server List", 420, 500), ("Quit", 650, 500)])

start = True

button_color = (210, 20, 20)

while start:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        elif event.type == KEYDOWN:
            if scene_manager.get_scene().name == "ADD":
                frames = 0
                if event.key == K_LEFT:
                    scene_manager.get_scene().left()
                elif event.key == K_RIGHT:
                    scene_manager.get_scene().right()
                elif event.key == K_UP:
                    scene_manager.get_scene().up()
                elif event.key == K_DOWN:
                    scene_manager.get_scene().down()
                elif event.key == K_RETURN:
                    if scene_manager.get_scene().highlighted_button_id == 0:
                        save_server(scene_manager.get_scene().server_name, scene_manager.get_scene().server_address)
                        scene_manager.get_scene().server_name = ""
                        scene_manager.get_scene().server_address = ""
                        scene_manager.get_scene().highlighted_text_box_id = 0
                        scene_manager.load_scene(start_scene)
                    elif scene_manager.get_scene().highlighted_button_id == 1:
                        scene_manager.load_scene(start_scene)
                    elif scene_manager.get_scene().highlighted_button_id == 2:
                        scene_manager.load_scene(None)
                        pygame.quit()
                        exit()

                elif scene_manager.get_scene().highlighted_text_box_id == 0:
                    if event.key == K_BACKSPACE:
                        scene_manager.get_scene().server_name = scene_manager.get_scene().server_name[:-1]
                    elif event.key == K_KP0:
                        scene_manager.get_scene().server_name += '0'
                    elif event.key == K_KP1:
                        scene_manager.get_scene().server_name += '1'
                    elif event.key == K_KP2:
                        scene_manager.get_scene().server_name += '2'
                    elif event.key == K_KP3:
                        scene_manager.get_scene().server_name += '3'
                    elif event.key == K_KP4:
                        scene_manager.get_scene().server_name += '4'
                    elif event.key == K_KP5:
                        scene_manager.get_scene().server_name += '5'
                    elif event.key == K_KP6:
                        scene_manager.get_scene().server_name += '6'
                    elif event.key == K_KP7:
                        scene_manager.get_scene().server_name += '7'
                    elif event.key == K_KP8:
                        scene_manager.get_scene().server_name += '8'
                    elif event.key == K_KP9:
                        scene_manager.get_scene().server_name += '9'
                    elif event.key == K_KP_PERIOD:
                        scene_manager.get_scene().server_name += '.'
                    elif event.key == K_TAB:
                        scene_manager.get_scene().down()
                    else:
                        scene_manager.get_scene().server_name += chr(event.key) if 31 < event.key < 128 else ""

                elif scene_manager.get_scene().highlighted_text_box_id == 1:
                    if event.key == K_BACKSPACE:
                        scene_manager.get_scene().server_address = scene_manager.get_scene().server_address[:-1]
                    elif event.key == K_KP0:
                        scene_manager.get_scene().server_address += '0'
                    elif event.key == K_KP1:
                        scene_manager.get_scene().server_address += '1'
                    elif event.key == K_KP2:
                        scene_manager.get_scene().server_address += '2'
                    elif event.key == K_KP3:
                        scene_manager.get_scene().server_address += '3'
                    elif event.key == K_KP4:
                        scene_manager.get_scene().server_address += '4'
                    elif event.key == K_KP5:
                        scene_manager.get_scene().server_address += '5'
                    elif event.key == K_KP6:
                        scene_manager.get_scene().server_address += '6'
                    elif event.key == K_KP7:
                        scene_manager.get_scene().server_address += '7'
                    elif event.key == K_KP8:
                        scene_manager.get_scene().server_address += '8'
                    elif event.key == K_KP9:
                        scene_manager.get_scene().server_address += '9'
                    elif event.key == K_KP_PERIOD:
                        scene_manager.get_scene().server_address += '.'
                    elif event.key == K_TAB:
                        scene_manager.get_scene().up()
                    else:
                        scene_manager.get_scene().server_address += chr(event.key) if 31 < event.key < 128 else ""

            else:
                if event.key == K_LEFT:
                    scene_manager.get_scene().left()
                elif event.key == K_RIGHT:
                    scene_manager.get_scene().right()
                elif event.key == K_UP:
                    scene_manager.get_scene().up()
                elif event.key == K_DOWN:
                    scene_manager.get_scene().down()
                elif event.key == K_RETURN:
                    if scene_manager.get_scene().name == "MAIN":
                        if scene_manager.get_scene().highlighted_button_id == 0:
                            scene_manager.load_scene(start_scene)
                        elif scene_manager.get_scene().highlighted_button_id == 1:
                            scene_manager.load_scene(help_scene)
                        elif scene_manager.get_scene().highlighted_button_id == 2:
                            scene_manager.load_scene(None)
                            pygame.quit()
                            exit()
                    elif scene_manager.get_scene().name == "START":
                        if scene_manager.get_scene().highlighted_button_id == 0:
                            scene_manager.load_scene(add_server_scene)
                        elif scene_manager.get_scene().highlighted_button_id == 1:
                            scene_manager.load_scene(main_scene)
                        elif scene_manager.get_scene().highlighted_button_id == 2:
                            scene_manager.load_scene(None)
                            pygame.quit()
                            exit()
                    elif scene_manager.get_scene().name == "HELP":
                        if scene_manager.get_scene().highlighted_button_id == 0:
                            scene_manager.load_scene(main_scene)
                        elif scene_manager.get_scene().highlighted_button_id == 1:
                            scene_manager.load_scene(None)
                            pygame.quit()
                            exit()
                elif event.key == K_s and scene_manager.get_scene().name == "START":
                    address = scene_manager.get_scene().servers[scene_manager.get_scene().highlighted_server_id].address
                    command = "python game.py %s" % (address)
                    subprocess.Popen(command)

                elif event.key == K_d and scene_manager.get_scene().name == "START":
                    if scene_manager.get_scene().servers[
                        scene_manager.get_scene().highlighted_server_id].address != "127.0.0.1":
                        delete_server(
                            scene_manager.get_scene().servers[scene_manager.get_scene().highlighted_server_id])
                        scene_manager.get_scene().servers = get_servers()

    screen.fill((0, 0, 0))
    scene_manager.get_scene().draw()
    pygame.display.update()
    clock.tick(30)
    if scene_manager.get_scene().name == "ADD":
        frames += 1
        if frames % 30 == 0:
            frames = 0
