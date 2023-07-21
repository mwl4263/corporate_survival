import pygame
import random
import abilities
import upgrades
import bosses
import waves

from spritesheet import Spritesheet
pygame.init()

#adjustable variables
warning_bug_speed = 3
error_bug_speed = 2
speed_modifier = 10

# End adjustable variables




DISPLAY_W, DISPLAY_H = 1080, 570
canvas = pygame.Surface((DISPLAY_W,DISPLAY_H))
window = pygame.display.set_mode(((DISPLAY_W, DISPLAY_H)))
running = True
clock = pygame.time.Clock()

bug_frame = 0
bg = pygame.image.load("office-warground.bmp")
office_slave_sheet = Spritesheet("officeslave.png")
error_bug = Spritesheet("error_bug.png")
warning_bug = Spritesheet("warning_bug.png")
bullet_sheet = Spritesheet("push.png")


def createBugs(number_of_bugs, bug_type):
    global bug_frame
    bugs = []
    for i in range(number_of_bugs+1):
        starting_x, starting_y = random.choice([random.randint(-300, 0)
                                                , random.randint(DISPLAY_W, DISPLAY_W+300)]), random.choice([random.randint(-300, 0), random.randint(DISPLAY_H, DISPLAY_H+300)])
        bug = bug_type
        bugs.append({"bug_type": bug, "x": starting_x, "y": starting_y, frame: bug_frame})
    return bugs


error_bug_right = [(0, 82, 30, 34), (45, 82, 30, 34), (82,82,30,34), (113, 82,32,34), (157, 82,32,34) ]
error_bug_left = [(0, 114, 34, 34), (45, 114, 34, 34), (82,114,34,34), (113, 114,34,34), (157, 114,34,34) ]
warning_bug_right = error_bug_right
warning_bug_left = error_bug_left
office_slave_backwards = [(0,0,54,72), (65, 0, 54, 72), (120, 0, 54 ,72), (185,0,54,72), (250, 0, 54, 72), (320, 0, 54, 72),  (380, 0, 54, 72), (440, 0, 54, 72), (510,0,54,72)]
office_slave_forward= [(0,125,54,72), (65, 125, 54, 72), (125, 125, 54 ,72), (185,125,54,72), (250, 125, 54, 72), (315, 125, 54, 72),  (380, 125, 54, 72), (440, 125, 54, 72), (510,125,54,72)]
office_slave_right = [(0,190,54,72), (65, 190, 54, 72), (120, 190, 54 ,72), (185,190,54,72), (250, 190, 54, 72), (320, 190, 54, 72),  (380, 190, 54, 72), (440, 190, 54, 72), (510,190,54,72)]
office_slave_left = [(0, 65, 54, 72), (65, 65, 54, 72), (120, 65, 54, 72), (185, 65, 54, 72), (250, 65, 54, 72), (320, 65, 54, 72), (380, 65, 54, 72), (440, 65, 54, 72), (510, 65, 54, 72)]
frame = 0
push = bullet_sheet.get_sprite(0,0,144,48)
office_slave = office_slave_sheet.get_sprite(*office_slave_forward[2])
current_frame = office_slave_forward[0]
warning_bug_position_x, warning_bug_position_y = random.randint(DISPLAY_W, DISPLAY_W+300), random.randint(DISPLAY_H, DISPLAY_H+300)
error_bug_position_x, error_bug_position_y = random.randint(0,DISPLAY_W), random.randint(0,DISPLAY_H)
worker_position_x, worker_position_y = DISPLAY_W/2,DISPLAY_H/2

frame_count = 0
warning_bug_frames_to_use = warning_bug_right
error_bug_frames_to_use = error_bug_right

def create_bullet(upgrade_type):
    bullets = []
    bullet_x, bullet_y = worker_position_x, worker_position_y
    for x in range(abilities.Pycharm.get("amount")+1):
        if upgrade_type == "pycharm":
            size = abilities.Pycharm.get("size")
            speed =abilities.Pycharm.get("speed")
            dps = abilities.Pycharm.get("dps")
            bullets.append({"speed": speed, "dps": dps, "size": size, "x": bullet_x, "y": bullet_y,"direction": ""} )
    return bullets









warning_bugs = createBugs(10, warning_bug)
error_bugs = createBugs(5, error_bug)

default_bullet = create_bullet("pycharm")

bulletInMotion = False
while running:
    canvas.blit(bg, (0,0))
    if bulletInMotion == False:
        direction = ""

    # print("frame " + str(bug_frame))
    keys = pygame.key.get_pressed()
    if worker_position_x > DISPLAY_W-60:
        worker_position_x = worker_position_x - 10
    if worker_position_x < 0:
        worker_position_x = worker_position_x + 10
    if worker_position_y > DISPLAY_H-90:
        worker_position_y = worker_position_y - 10
    if worker_position_y < 0:
        worker_position_y = worker_position_y + 10
    if frame == len(office_slave_forward)-1:
        frame = 0
    if bug_frame == len(error_bug_right)-1:
        bug_frame = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if keys[pygame.K_a]:
        current_frame = office_slave_left[frame]
        worker_position_x  -= speed_modifier
    elif keys[pygame.K_d]:
        current_frame = office_slave_right[frame]
        worker_position_x += speed_modifier
    elif keys[pygame.K_w]:
        current_frame = office_slave_backwards[frame]
        worker_position_y -= speed_modifier
    elif keys[pygame.K_s]:
        current_frame = office_slave_forward[frame]
        worker_position_y += speed_modifier
    elif event.type == pygame.KEYDOWN:
        current_frame = office_slave_forward[0]
        frame = 0
        if bulletInMotion == False:
            if event.key == pygame.K_RIGHT:

                direction = "right"
                bulletInMotion = True
            elif event.key == pygame.K_LEFT:
                bulletInMotion = True
                direction = "left"
            elif event.key == pygame.K_UP:
                bulletInMotion = True
                direction = "up"
            elif event.key == pygame.K_DOWN:
                bulletInMotion = True
                direction = "down"
    frame += 1
    frame_count+=1
    bug_frame += 1
    bulletNum = 0

    for bullet in default_bullet:
        if direction == "up" and bulletInMotion == True:
            bullet["y"] -= bullet["speed"]
        elif direction == "down"  and bulletInMotion == True:
            bullet["y"] += bullet["speed"]
        elif direction == "left"  and bulletInMotion == True:
            bullet["x"] -= bullet["speed"]
        elif direction == "right"  and bulletInMotion == True:
            bullet["x"] += bullet["speed"]
        if bullet["x"] > DISPLAY_W:
            default_bullet.remove(bullet)
            bulletInMotion = False
        elif bullet["x"] < 0:
            default_bullet.remove(bullet)
            bulletInMotion = False
        elif bullet["y"] > DISPLAY_H:
            default_bullet.remove(bullet)
            bulletInMotion = False
        elif bullet["y"] < 0:
            default_bullet.remove(bullet)
            bulletInMotion = False
        if bulletNum == len(default_bullet):
            c_x = bullet["x"]
            c_y = bullet["y"]
            canvas.blit(push, (bullet["x"], bullet["y"]))
        bulletNum += 1
    print(bullet["x"], bullet["y"])




    # Error Bug PathFinding

# warning bug pathfinding




    office_slave = office_slave_sheet.get_sprite(*current_frame)
    for ebugs in error_bugs:
        offset = random.uniform(-1, 1)
        if (worker_position_x < ebugs.get("x")):
            error_bug_frames_to_use = error_bug_left
            ebugs["x"] -= error_bug_speed + offset
        if (worker_position_x > ebugs.get("x")):
            error_bug_frames_to_use = error_bug_right
            ebugs["x"] += error_bug_speed + offset
        if (worker_position_y < ebugs.get("y")):
            ebugs["y"] -= error_bug_speed + offset
        if (worker_position_y > ebugs.get("y")):
            ebugs["y"] += error_bug_speed + offset
        canvas.blit(ebugs.get("bug_type").get_sprite(*error_bug_frames_to_use[bug_frame]), (ebugs.get("x"), ebugs.get("y")))

    for wbugs in warning_bugs:
        wbugs["frame"] = bug_frame
        offset = random.uniform(-1,2)
        if (worker_position_x < wbugs.get("x")):
            #print("bug is to the right of the worker")
            warning_bug_frames_to_use = warning_bug_left
            wbugs["x"] -= warning_bug_speed + offset
        if (worker_position_x > wbugs.get("x")):
            #print("bug is to the left of the worker")
            warning_bug_frames_to_use = warning_bug_right
            wbugs["x"] += warning_bug_speed + offset
            # wbugs["bug_type"] = warning_bug_frames_to_use[bug_frame]
        if (worker_position_y < wbugs.get("y")):
            #print("bug is below the worker")
            wbugs["y"] -= error_bug_speed + offset
        if (worker_position_y > wbugs.get("y")):
            #print("bug is above the worker")
            wbugs["y"] += warning_bug_speed + offset
        canvas.blit(wbugs.get("bug_type").get_sprite(*warning_bug_frames_to_use[bug_frame]), (wbugs.get("x"), wbugs.get("y")))
    canvas.blit(office_slave, (worker_position_x, worker_position_y))

    window.blit(canvas, (0,0))
    pygame.display.update()
    clock.tick(20)
    canvas.fill((0,0,0))
